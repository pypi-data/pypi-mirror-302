# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for defining the model classes that are used to wrap the mmocr framework.
"""

import logging
from statistics import mean
from typing import Dict, List, Optional, Union

from mlcvzoo_base.api.data.ocr_perception import OCRPerception
from mlcvzoo_base.api.model import OCRModel
from mlcvzoo_base.api.structs import Runtime
from mlcvzoo_mmdetection.model import MMDetectionModel
from mmocr.apis.inferencers import TextRecInferencer
from mmocr.structures.textrecog_data_sample import TextRecogDataSample
from nptyping import Int, NDArray, Shape

from mlcvzoo_mmocr.configuration import MMOCRConfig
from mlcvzoo_mmocr.model import MMOCRModel

logger = logging.getLogger(__name__)

ImageType = NDArray[Shape["Height, Width, Any"], Int]


class MMOCRTextRecognitionModel(
    MMOCRModel[OCRPerception, TextRecInferencer, TextRecogDataSample],
    OCRModel[MMOCRConfig, Union[str, ImageType]],
):
    def __init__(
        self,
        from_yaml: Optional[str] = None,
        configuration: Optional[MMOCRConfig] = None,
        string_replacement_map: Optional[Dict[str, str]] = None,
        init_for_inference: bool = False,
        is_multi_gpu_instance: bool = False,
        runtime: str = Runtime.DEFAULT,
    ) -> None:
        MMOCRModel.__init__(
            self,
            from_yaml=from_yaml,
            configuration=configuration,
            string_replacement_map=string_replacement_map,
            init_for_inference=init_for_inference,
            is_multi_gpu_instance=is_multi_gpu_instance,
            runtime=runtime,
            inferencer_type=TextRecInferencer,
        )
        OCRModel.__init__(
            self,
            configuration=self.configuration,
            init_for_inference=init_for_inference,
            runtime=runtime,
        )

    @staticmethod
    def __filter_result_score_by_mean(
        prediction: TextRecogDataSample, score_threshold: float
    ) -> Optional[float]:
        """
        Take the result of the mmocr prediction and determine the
        score of the word

        Args:
            prediction: The result of the inference
            score_threshold: The threshold for the score that has to be fulfilled

        Returns:
            The determined score
        """

        score: Optional[float] = None
        if len(prediction.pred_text.score) > 0:
            score = float(mean(prediction.pred_text.score))

            if score < score_threshold:
                score = None

        return score

    def _decode_mmocr_result(
        self, prediction: TextRecogDataSample
    ) -> List[OCRPerception]:
        ocr_texts: List[OCRPerception] = []

        score = self.__filter_result_score_by_mean(
            prediction=prediction,
            score_threshold=self.configuration.inference_config.score_threshold,
        )
        if score is not None:
            ocr_texts.append(
                OCRPerception(content=prediction.pred_text.item, score=score)
            )

        return ocr_texts


if __name__ == "__main__":
    MMDetectionModel.run(MMOCRTextRecognitionModel)
