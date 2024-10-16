#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

__all__ = ["StatefulRecurrent", "QuantizedStatefulRecurrent", "reset_states",
           "StatefulProjection", "QuantizedStatefulProjection"]

import keras
import tensorflow as tf

from .recorders import NonTrackVariable, TensorRecorder, NonTrackFixedPointVariable
from .layers_base import (register_quantize_target, tensor_inputs, apply_buffer_bitwidth,
                          register_aligned_inputs, QuantizedLayer, neural_layer_init,
                          rescale_outputs)
from .quantizers import WeightQuantizer, OutputQuantizer
from ..tensors import FixedPoint, QTensor
from ..debugging import assert_equal, assert_less


@keras.saving.register_keras_serializable()
class StatefulRecurrent(keras.layers.Layer):
    """ A recurrent layer with an internal state.

    Args:
        subsample_ratio (float, optional): subsampling ratio that defines rate at which outputs are
            produced (zero otherwise). Defaults to 1.
    """

    def __init__(self, *args, subsample_ratio=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.subsample_ratio = subsample_ratio
        self._counter = NonTrackVariable("counter")
        self._internal_state_real = NonTrackVariable("internal_state_real")
        self._internal_state_imag = NonTrackVariable("internal_state_imag")

    @property
    def counter(self):
        return self._counter.var

    @property
    def internal_state_real(self):
        return self._internal_state_real.var

    @property
    def internal_state_imag(self):
        return self._internal_state_imag.var

    def build(self, input_shape):
        with tf.name_scope(self.name + '/'):
            super().build(input_shape)
            # 'A' weight is a complex64 tensor stored as two float32 tensor to ease quantization
            self.A_real = self.add_weight(name='A_real', shape=(input_shape[-1],))
            self.A_imag = self.add_weight(name='A_imag', shape=(input_shape[-1],))

    def update_counter(self):
        """Function that increments a 'counter' variable. If the variable doesn't exist, it
            will be created in the layer graph and tracked.
        """
        self._counter.init_var(0, True)
        self._counter.var.assign_add(1)

    def call(self, inputs):
        """ This call method only takes in a single input step.

        For every input step, the internal state is updated using the inputs which should be the
        updated state from the previous layer.
        """

        # Update or initialize (if it's the first call) the counter variable
        self.update_counter()

        # Initialize (only during the first call) the internal state variables
        self._internal_state_real.init_var(inputs)
        self._internal_state_imag.init_var(inputs)

        # Since the above variables will be added to the graph during the layer graph initialization
        # the batch size is unknown and set to None. Such behavior won't allow the next
        # operations due to a conflict in the brodcastable shape. As a workaround, we set again in
        # the variables a tf.zeros tensor but this time with the batch_size known since it's in the
        # call, when counter == 1 (first passage or after a reset, when the batch_size changes for
        # example).
        if self.counter == 1:
            self._internal_state_real.set_var(tf.zeros_like(inputs))
            self._internal_state_imag.set_var(tf.zeros_like(inputs))

        # Path for skipping computations
        if self.subsample_ratio and tf.math.floormod(self.counter, self.subsample_ratio) != 0:
            return tf.zeros_like(tf.stack([self.internal_state_real, self.internal_state_imag],
                                          -1))

        # Update internal state: compute real and imaginary part separately
        updated_real = self.internal_state_real * self.A_real - \
            self.internal_state_imag * self.A_imag + inputs
        internal_state_imag = self.A_imag * self.internal_state_real + \
            self.A_real * self.internal_state_imag
        self._internal_state_imag.set_var(internal_state_imag)
        # Update real part in a second time so that it does not impact imaginary part computation
        self._internal_state_real.set_var(updated_real)

        return tf.stack([self.internal_state_real, self.internal_state_imag], -1)

    def get_config(self):
        config = super().get_config()
        config.update({
            'subsample_ratio': self.subsample_ratio
        })
        return config

    def reset_layer_states(self):
        for var in [self._counter, self._internal_state_real, self._internal_state_imag]:
            var.reset_var()


@register_quantize_target([StatefulRecurrent])
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedStatefulRecurrent(QuantizedLayer, StatefulRecurrent):
    """ A quantized version of the StatefulRecurrent layer that operates on quantized inputs,
    weights and internal state.

    Note that internal state is quantized to 16-bits for accuracy reasons, inputs and outputs of
    this layer are then also 16-bits.

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """

    def __init__(self, *args, quant_config=None, **kwargs):
        super().__init__(*args, quant_config=quant_config, **kwargs)

        self._internal_state_real = NonTrackFixedPointVariable("internal_state_real")
        self._internal_state_imag = NonTrackFixedPointVariable("internal_state_imag")

        # Build weight quantizer for A_real and A_imag (sharing the same quantizer)
        if "a_quantizer" not in self.quant_config:
            # Forcing to:
            #   - per-tensor to ensure alignement in the call operations
            #   - 16-bits for accuracy reasons
            #   - FixedPoint quantization to prevent scale_out operations on internal_state
            self.quant_config["a_quantizer"] = {"bitwidth": 16, "axis": None, "fp_quantizer": True}
        a_quantizer_cfg = self.quant_config["a_quantizer"]
        self.a_quantizer = WeightQuantizer(name="a_quantizer", **a_quantizer_cfg)

        # Finalize output quantizer, add one with default configuration if there is None in the
        # config as state must be quantized
        if "output_quantizer" not in self.quant_config:
            self.quant_config["output_quantizer"] = {"bitwidth": 16, "axis": "per-tensor"}
        out_quant_cfg = self.quant_config["output_quantizer"]
        self.out_quantizer = OutputQuantizer(name="output_quantizer", **out_quant_cfg)
        self.buffer_bitwidth = apply_buffer_bitwidth(self.quant_config, signed=True)

        # Prepare the variable that should be recorded
        self.input_add_shift = TensorRecorder(name=self.name + "/input_add_shift")

    @tensor_inputs([FixedPoint])
    def call(self, inputs):
        # Update or initialize (if it's the first call) the counter variable
        self.update_counter()

        # Initialize (only during the first call) the internal state variables
        self._internal_state_real.init_var(inputs)
        self._internal_state_imag.init_var(inputs)

        # Set again the variables with a fully defined shape (batch_size is known)
        if self.counter == 1:
            self._internal_state_real.set_var(tf.zeros_like(inputs))
            self._internal_state_imag.set_var(tf.zeros_like(inputs))

        # Promote internal_state
        internal_state_real = self._internal_state_real.promote(self.buffer_bitwidth)
        internal_state_imag = self._internal_state_imag.promote(self.buffer_bitwidth)

        if self.subsample_ratio and tf.math.floormod(self.counter, self.subsample_ratio) != 0:
            # Path for skipping computations
            return self.out_quantizer(tf.zeros_like(tf.stack([internal_state_real,
                                                              internal_state_imag], -1)))

        # Quantize A matrices
        A_real = self.a_quantizer(self.A_real)
        A_imag = self.a_quantizer(self.A_imag)

        # The op below is possible because internal_state is quantized per-tensor on the real/imag
        # concatenated tensor, thus internal_state_real and internal_state_imag are aligned.
        assert_equal(internal_state_real.frac_bits, internal_state_imag.frac_bits)

        # Update internal state: compute real and imaginary part separately
        updated_real = tf.multiply(internal_state_real, A_real) - \
            tf.multiply(internal_state_imag, A_imag)

        # Align inputs with intermediate result before addition
        # By construction, A_real² + A_imag² < 1 will ensure that A matrices are between 0 and 1
        # and thus their FixedPoint representation is all fractional part and this will also be True
        # for updated_state. So the higher frac_bits are on the state (input_proj being 16-bits,
        # frac_bits it at most 15).
        assert_less(inputs.frac_bits, updated_real.frac_bits), f"Input resolution is to high \
            {inputs.frac_bits} must be below {updated_real.frac_bits}."
        inputs, input_add_shift = inputs.align(updated_real, self.buffer_bitwidth)
        self.input_add_shift(input_add_shift)

        # At this point addition is possible
        updated_real = updated_real + inputs

        # Same for imaginary part
        updated_imag = tf.multiply(internal_state_real, A_imag) + \
            tf.multiply(internal_state_imag, A_real)

        # Concatenate updated_real and updated_imag
        concatenated_internal_state = tf.stack([updated_real, updated_imag], -1)

        # Quantize down the internal state
        output = self.out_quantizer(concatenated_internal_state)

        # Update internal state members, storying float state
        self._internal_state_real.set_var(tf.gather(output, 0, axis=-1))
        self._internal_state_imag.set_var(tf.gather(output, 1, axis=-1))
        return output


def reset_states(model):
    """ Resets all StatefulRecurrent layers internal states in the model.
    Args:
        model (keras.Model): the model to reset
    """
    for layer in model.layers:
        if isinstance(layer, StatefulRecurrent):
            layer.reset_layer_states()


@keras.saving.register_keras_serializable()
class StatefulProjection(keras.layers.Dense):
    """ Same as a Dense layer but with optional reshaping operation.

    Reshaping can happen both on the inputs and the outputs.

    Args:
        downshape (tuple, optional): target shape for downshape operation that happens before the
            dense. Defaults to None.
        upshape (tuple, optional): target shape for upshape operation that happens after the dense.
            Defaults to None.
    """

    def __init__(self, *args, downshape=None, upshape=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.downshape = tuple(downshape) if downshape else None
        self.upshape = tuple(upshape) if upshape else None

    def build(self, input_shape):
        with tf.name_scope(self.name + '/'):
            if self.downshape is None:
                super().build(input_shape)
            else:
                # When downshape is enabled, build the layer with the target shape so that variables
                # are build properly
                super().build(self.downshape)
                # Edit the input_spec so that from a graph point of view, this layer sees the
                # original input shape
                last_dim = tf.TensorShape(input_shape)[-1]
                self.input_spec = tf.keras.layers.InputSpec(min_ndim=2, axes={-1: last_dim})

    def call(self, inputs):
        # Apply the optional input downshape
        if self.downshape is not None:
            inputs = tf.reshape(inputs, (tf.shape(inputs)[0],) + self.downshape)

        # Standard Dense operation
        outputs = super().call(inputs)

        # Apply the optional output upshape
        if self.upshape is not None:
            outputs = tf.reshape(outputs, (tf.shape(outputs)[0],) + self.upshape)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["downshape"] = self.downshape
        config["upshape"] = self.upshape
        return config


@register_quantize_target([StatefulProjection])
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedStatefulProjection(QuantizedLayer, StatefulProjection):
    """ A quantized version of the StatefulProjection layer that operates on quantized inputs.
    """
    @neural_layer_init(False)
    def __init__(self, *args, **kwargs):
        # Limit buffer bitwidth to 27 for HW constraint
        self.quant_config['buffer_bitwidth'] = min(28, self.quant_config['buffer_bitwidth'])
        self.buffer_bitwidth = self.quant_config['buffer_bitwidth'] - 1

        # Weight quantizer must be per-tensor to allow upshaping, override it when necessary
        if self.upshape is not None:
            self.quant_config["weight_quantizer"]["axis"] = None
            weight_quantizer_cfg = self.quant_config["weight_quantizer"]
            self.weight_quantizer = WeightQuantizer(name="weight_quantizer",
                                                    **weight_quantizer_cfg)

    @tensor_inputs([QTensor, tf.Tensor])
    @rescale_outputs
    def call(self, inputs):
        if self.downshape is not None:
            inputs = tf.reshape(inputs, (tf.shape(inputs)[0],) + self.downshape)

        # Quantize the weights
        kernel = self.weight_quantizer(self.kernel)

        outputs = tf.matmul(inputs, kernel)

        if self.use_bias:
            # Quantize and align biases
            bias = self.bias_quantizer(self.bias, outputs)
            outputs = tf.add(outputs, bias)

        if self.upshape is not None:
            outputs = tf.reshape(outputs, (tf.shape(outputs)[0],) + self.upshape)
        return outputs
