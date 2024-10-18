# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for defining the model classes that are used to wrap the mmocr framework.
"""

import logging
from typing import Dict, List, Optional, Union

from mlcvzoo_base.api.data.annotation_class_mapper import AnnotationClassMapper
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.data.segmentation import Segmentation
from mlcvzoo_base.api.data.types import PolygonTypeNP
from mlcvzoo_base.api.model import SegmentationModel
from mlcvzoo_base.api.structs import Runtime
from mlcvzoo_mmdetection.model import MMDetectionModel
from mmocr.apis.inferencers import TextDetInferencer
from mmocr.structures.textdet_data_sample import TextDetDataSample
from nptyping import Int, NDArray, Shape

from mlcvzoo_mmocr.configuration import MMOCRConfig
from mlcvzoo_mmocr.model import MMOCRModel

logger = logging.getLogger(__name__)

ImageType = NDArray[Shape["Height, Width, Any"], Int]


class MMOCRTextDetectionModel(
    MMOCRModel[Segmentation, TextDetInferencer, TextDetDataSample],
    SegmentationModel[MMOCRConfig, Union[str, ImageType]],
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
            inferencer_type=TextDetInferencer,
        )
        SegmentationModel.__init__(
            self,
            configuration=self.configuration,
            init_for_inference=init_for_inference,
            mapper=AnnotationClassMapper(
                class_mapping=self.configuration.class_mapping,
            ),
            runtime=runtime,
        )

    @property
    def num_classes(self) -> int:
        return self.mapper.num_classes

    def get_classes_id_dict(self) -> Dict[int, str]:
        return self.mapper.annotation_class_id_to_model_class_name_map

    def _decode_mmocr_result(self, prediction: TextDetDataSample) -> List[Segmentation]:
        segmentations: List[Segmentation] = []
        for polygons, score in zip(
            prediction.pred_instances.polygons, prediction.pred_instances.scores
        ):
            float_score = float(score)
            if float_score < self.configuration.inference_config.score_threshold:
                continue

            # Reshape the received polygon from mmocr to match the datatype of the MLCVZoo
            # The format of mmocr is [x1, y1, ..., xn, yn] (n>=3)
            # the MLCVZoo expects [[x1, y1], ..., [xn, yn]] (n>=3)
            polygon_np: PolygonTypeNP = polygons.reshape(-1, 2)
            if self.configuration.inference_config.to_rect_polygon:
                polygon_np = Segmentation.polygon_to_rect_polygon(polygon=polygon_np)

            new_segmentations = self.build_segmentations(
                class_identifiers=[
                    ClassIdentifier(
                        class_id=MMOCRConfig.__text_class_id__,
                        class_name=MMOCRConfig.__text_class_name__,
                    )
                ],
                score=score,
                polygon=polygon_np,
            )

            segmentations.extend(new_segmentations)

        return segmentations


if __name__ == "__main__":
    MMDetectionModel.run(MMOCRTextDetectionModel)
