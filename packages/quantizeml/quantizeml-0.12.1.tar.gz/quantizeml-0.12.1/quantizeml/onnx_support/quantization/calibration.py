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
import tempfile
from pathlib import Path

import onnx
from onnxruntime.quantization import create_calibrator, CalibrationMethod

from .register_patterns import PATTERNS_MAP, CUSTOM_PATTERNS_MAP
from .data_reader import CalibrationDataReader


def _get_op_types_to_calibrate():
    # This function computes the set of operation types whose outputs need to be calibrated.
    # These operation types are the last operations in each pattern from
    # PATTERNS_MAP and CUSTOM_PATTERNS_MAP.
    return {pattern.pattern[-1] for pattern in PATTERNS_MAP + CUSTOM_PATTERNS_MAP}


def calibrate(model,
              samples=None,
              num_samples=None,
              batch_size=None,
              symmetric=False,
              average=False,
              per_tensor_activations=True):
    """Calibrates the ONNX model using the provided samples.

    When no samples are provided, random samples are generated.

    Args:
        model (ModelProto): onnx model to calibrate
        samples (np.array, optional): calibration samples. When no samples are provided,
            random samples are generated. Defaults to None.
        num_samples (int, optional): number of samples to generate. Defaults to None.
        batch_size (int, optional): the batch size. Defaults to None.
        symmetric (bool, optional): whether the final range of tensor during calibration
            will be explicitly set to symmetric to central point "0". Defaults to False.
        average (bool, optional): whether average of the minimum and maximum values
            will be computed. Defaults to False.
        per_tensor_activations (bool, optional): wheter to compute activation ranges per tensor.
            Defaults to True.

    Returns:
        dict: tensor names with calibration ranges.
    """
    # Create a calibration data reader from given samples.
    calibration_data_reader = CalibrationDataReader(model, samples, num_samples, batch_size)

    with tempfile.TemporaryDirectory(prefix="ort.quant.") as quant_tmp_dir:
        tmp_dir = Path(quant_tmp_dir)

        # Temporary save the model to create the calibrator
        model_path = tmp_dir.joinpath("model.onnx")
        onnx.save(model, model_path)

        # Declare MinMax calibrator from model path
        calibrator = create_calibrator(
            model_path,
            op_types_to_calibrate=_get_op_types_to_calibrate(),
            augmented_model_path=tmp_dir.joinpath("augmented_model.onnx"),
            calibrate_method=CalibrationMethod.MinMax,
            use_external_data_format=False,
            extra_options={"symmetric": symmetric,
                           "moving_average": average,
                           "per_channel": not per_tensor_activations})

        # Collect output tensors with calibration data and compute range
        calibrator.collect_data(calibration_data_reader)
        tensors_range = calibrator.compute_data()
        del calibrator
    return tensors_range
