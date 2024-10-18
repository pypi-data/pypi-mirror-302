# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for defining the model classes that are used to wrap the mmocr framework.
"""

import logging
from abc import ABC
from typing import Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union, cast

from mlcvzoo_base.api.model import PredictionType
from mlcvzoo_base.api.structs import Runtime
from mlcvzoo_base.configuration.utils import (
    create_configuration as create_basis_configuration,
)
from mlcvzoo_mmdetection.configuration import MMDetectionMMDeployConfig
from mlcvzoo_mmdetection.mlcvzoo_mmdet_dataset import MLCVZooMMDetDataset
from mlcvzoo_mmdetection.model import MMDetectionModel
from mmengine.structures import BaseDataElement
from mmocr.apis.inferencers import TextDetInferencer, TextRecInferencer
from mmocr.apis.inferencers.base_mmocr_inferencer import BaseMMOCRInferencer
from mmocr.registry import DATASETS
from nptyping import Int, NDArray, Shape

from mlcvzoo_mmocr.configuration import MMOCRConfig, MMOCRInferenceConfig
from mlcvzoo_mmocr.mlcvzoo_mmocr_dataset import MLCVZooMMOCRDataset

logger = logging.getLogger(__name__)

ImageType = NDArray[Shape["Height, Width, Any"], Int]

try:
    from mlcvzoo_mmdetection.mlcvzoo_mmdeploy.inferencer import MMDeployInferencer
except ModuleNotFoundError as error:
    MMDeployInferencer = None  # type: ignore # pylint: disable=invalid-name

InferencerType = TypeVar(
    "InferencerType",
    bound=BaseMMOCRInferencer,
)

MMOCRPredictionType = TypeVar(
    "MMOCRPredictionType",
    bound=BaseDataElement,
)


class MMOCRModel(
    MMDetectionModel[MMOCRInferenceConfig],
    ABC,
    Generic[PredictionType, InferencerType, MMOCRPredictionType],
):
    def __init__(
        self,
        from_yaml: Optional[str] = None,
        configuration: Optional[MMOCRConfig] = None,
        string_replacement_map: Optional[Dict[str, str]] = None,
        init_for_inference: bool = False,
        is_multi_gpu_instance: bool = False,
        runtime: str = Runtime.DEFAULT,
        inferencer_type: Optional[
            Union[Type[TextDetInferencer], Type[TextRecInferencer]]
        ] = None,
    ) -> None:
        self.inferencer: Optional[InferencerType] = None
        self.inferencer_type: Optional[
            Union[Type[TextDetInferencer], Type[TextRecInferencer]]
        ] = inferencer_type
        self.mmdeploy_inferencer: Optional[MMDeployInferencer] = None

        MMDetectionModel.__init__(
            self,
            from_yaml=from_yaml,
            configuration=configuration,
            string_replacement_map=string_replacement_map,
            init_for_inference=init_for_inference,
            is_multi_gpu_instance=is_multi_gpu_instance,
            runtime=runtime,
        )
        self.configuration: MMOCRConfig = cast(  # type: ignore[redundant-cast]
            MMOCRConfig, self.configuration
        )

    @staticmethod
    def create_configuration(
        from_yaml: Optional[str] = None,
        configuration: Optional[MMOCRConfig] = None,
        string_replacement_map: Optional[Dict[str, str]] = None,
    ) -> MMOCRConfig:
        return cast(
            MMOCRConfig,
            create_basis_configuration(
                configuration_class=MMOCRConfig,
                from_yaml=from_yaml,
                input_configuration=configuration,
                string_replacement_map=string_replacement_map,
            ),
        )

    def _init_inference_model(self) -> None:
        if self.runtime == Runtime.DEFAULT:
            if self.net is None and self.inferencer_type is not None:
                self.inferencer = self.inferencer_type(self.cfg, None)

                if self.inferencer is not None:
                    self.net = self.inferencer.model

                if self.configuration.inference_config.checkpoint_path != "":
                    self.restore(
                        checkpoint_path=self.configuration.inference_config.checkpoint_path
                    )
        elif self.runtime in (
            Runtime.ONNXRUNTIME,
            Runtime.ONNXRUNTIME_FLOAT16,
            Runtime.TENSORRT,
        ):
            # Return value of _get__mmdeploy_config will not be None
            mmdeploy_config = cast(
                MMDetectionMMDeployConfig, self._get_mmdeploy_config()
            )

            if MMDeployInferencer is None:
                raise RuntimeError(
                    "Extra 'mmdeploy' must be installed to run a model which is deployed with "
                    "MMDeploy."
                )

            self.mmdeploy_inferencer = MMDeployInferencer(
                model_config=self.cfg,
                mmdeploy_config=mmdeploy_config,
            )
        else:
            raise ValueError(
                f"Initialization for inference is not supported for runtime '{self.runtime}'."
            )

    @staticmethod
    def _register_dataset() -> None:
        """
        Register the custom dataset of the MLCVZoo in the registry of mmcv

        Returns:
            None
        """
        DATASETS.register_module(
            MLCVZooMMDetDataset.__name__, module=MLCVZooMMDetDataset, force=True
        )
        DATASETS.register_module(
            MLCVZooMMOCRDataset.__name__, module=MLCVZooMMOCRDataset, force=True
        )

    @staticmethod
    def _get_dataset_type() -> str:
        return "MLCVZooMMOCRDataset"

    def _decode_mmocr_result(
        self, prediction: MMOCRPredictionType
    ) -> List[PredictionType]:
        raise NotImplementedError(
            "_decode_mmocr_result needs to be implemented by sub-classes"
        )

    def predict(
        self, data_item: Union[str, ImageType]
    ) -> Tuple[Union[str, ImageType], List[PredictionType]]:
        """Run a prediction on a single input.

        Args:
            data_item (Union[str, ImageType]): The input to run the inference on.

        Raises:
            ValueError: If the net attribute is not initialized and the runtime is 'DEFAULT'.
            ValueError: If the inferencer attribute is not initialized.
            RuntimeError: If the model is deployed with MMDeploy and the mmdeploy module can not be
                imported.
            ValueError: If the runtime is not supported.

        Returns:
            Tuple[Union[str, ImageType], List[Segmentation]]: The input and the predicted
                segmentations.
        """
        no_inferencer_error = ValueError(
            "The 'inferencer' attribute is not initialized, make sure to instantiate with "
            "init_for_inference=True"
        )

        if self.runtime == Runtime.DEFAULT:
            if self.net is None:
                raise ValueError(
                    "The 'net' attribute is not initialized, "
                    "make sure to instantiate with init_for_inference=True"
                )
            if self.inferencer is None:
                raise no_inferencer_error

            # For a single data_item we only have one prediction
            return data_item, self._decode_mmocr_result(
                self.inferencer(
                    data_item, return_datasamples=True, batch_size=1, progress_bar=False
                )["predictions"][0]
            )
        if self.runtime in (
            Runtime.ONNXRUNTIME,
            Runtime.ONNXRUNTIME_FLOAT16,
            Runtime.TENSORRT,
        ):
            if self.mmdeploy_inferencer is None:
                raise no_inferencer_error

            if MMDeployInferencer is None:
                raise RuntimeError(
                    "Extra 'mmdeploy' must be installed to run a model which is deployed with "
                    "MMDeploy."
                )

            return data_item, self._decode_mmocr_result(
                prediction=self.mmdeploy_inferencer(data_item)[0]
            )

        raise ValueError(f"Prediction is not supported for runtime '{self.runtime}'.")

    def predict_many(
        self, data_items: List[Union[str, ImageType]]
    ) -> List[Tuple[Union[str, ImageType], List[PredictionType]]]:
        """Run a prediction on a batch of inputs.

        Args:
            data_items (List[Union[str, ImageType]]): The inputs to run the inference on.

        Raises:
            ValueError: If the net attribute is not initialized and the runtime is 'DEFAULT'.
            ValueError: If the inferencer attribute is not initialized.
            RuntimeError: If the model is deployed with MMDeploy and the mmdeploy module can not be
                imported.
            ValueError: If the runtime is not supported.

        Returns:
            List[Tuple[Union[str, ImageType], List[Segmentation]]]: A list of inputs and the
                predicted segmentations.
        """
        no_inferencer_error = ValueError(
            "The 'inferencer' attribute is not initialized, make sure to instantiate with "
            "init_for_inference=True"
        )

        prediction_list: List[Tuple[Union[str, ImageType], List[PredictionType]]] = []

        if self.runtime == Runtime.DEFAULT:
            if self.net is None:
                raise ValueError(
                    "The 'net' attribute is not initialized, "
                    "make sure to instantiate with init_for_inference=True"
                )
            if self.inferencer is None:
                raise no_inferencer_error

            predictions = self.inferencer(
                data_items,
                return_datasamples=True,
                batch_size=len(data_items),
                progress_bar=False,
            )["predictions"]
        elif self.runtime in (
            Runtime.ONNXRUNTIME,
            Runtime.ONNXRUNTIME_FLOAT16,
            Runtime.TENSORRT,
        ):
            if self.mmdeploy_inferencer is None:
                raise no_inferencer_error

            if MMDeployInferencer is None:
                raise RuntimeError(
                    "Extra 'mmdeploy' must be installed to run a model which is deployed with "
                    "MMDeploy."
                )

            # TODO: evaluate batch inference for MMDeploy
            predictions = [
                self.mmdeploy_inferencer(inputs=data_item)[0]
                for data_item in data_items
            ]
        else:
            raise ValueError(
                f"Multi-prediction is not supported for runtime '{self.runtime}'."
            )

        for data_item, prediction in zip(data_items, predictions):
            # TODO: The prediction score is per character
            #       => Add this to the OCRPerception
            decoded_predictions = self._decode_mmocr_result(prediction=prediction)

            prediction_list.append(
                (
                    data_item,
                    decoded_predictions,
                )
            )

        return prediction_list
