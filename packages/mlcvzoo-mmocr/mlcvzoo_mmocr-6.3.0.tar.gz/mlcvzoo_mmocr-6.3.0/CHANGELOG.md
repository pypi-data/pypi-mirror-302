# MLCVZoo mlcvzoo_mmocr module Versions:

6.3.0 (2024-07-10):
------------------
Integrate MMDeploy for ONNX Runtime and TensorRT
- Add runtime attribute to MMOCRModel, MMOCRTextDetectionModel and MMOCRTextRecognitionModel
- Extend existing functions so that they take the runtime attribute into account and are backwards compatible

6.2.0 (2024-06-21):
------------------
Update to latest changes in mlcvzoo packages:
- Implement and use API changes introduced by mlcvzoo-base version 6.0.0
- Compatibility with mlcvzoo-mmdetection
  - Version 6.5.0 and 6.6.0: mmdeploy integration
  - Version 6.7.0: mlcvzoo-base 6.0.0 adaptation

6.1.2 (2024-06-12):
------------------
Adapt python package management:
- Replace poetry by uv as dependency resolver and installer
- Replace poetry by the python native build package for building the python package
- Optimize dependency installation

6.1.1 (2024-02-07):
------------------
Updated links in pyproject.toml

6.1.0 (2023-08-21):
----------------
Fix configuration:
- Adapt to changes from mlcvzoo-mmdetection 6.1.1
- Add MLCVZooMMOCRDataset to ensure that OCR annotations get parsed correctly

6.0.0 (2023-06-14):
----------------
mlcvzoo-mmdetection 6.0.0, MMOCR 1 and relicense to OLFL-1.3 which succeeds the previous license

5.0.1 (2023-05-11):
----------------
Python 3.10 compatibility

5.0.0 (2023-02-10):
----------------
Implement API changes introduced by mlcvzoo-base version 5.0.0 and
mlcvzoo-mmdetetection version 5.0.0:
- Remove detector-config and use the feature of the single ModelConfiguration
- Remove duplicate attributes

4.1.0 (2022-11-18):
------------------
Make the "from_yaml" of the MMOCRModel, MMOCRTextDetectionModel and MMOCRTextRecognitionModel constructor Optional

4.0.2 (2022-09-09):
------------------
Ensure ConfigBuilder version 7 compatibility

4.0.1 (2022-08-11):
------------------
Fix processing of result in predict many function

4.0.0 (2022-08-09):
------------------
- Adapt to mlcvzoo-base 4.0.0 and mlcvzoo-mmdetection 4.0.0
- Refactor and enhance mlcvzoo_mmocr
  - The MMOCRModel inherits from MMDetectionModel which is the base of all models of open-mmlab
  - Remove the SegmentationDataset and replace it with the MLCVZooMMOcrDataset

3.1.1 (2022-07-14):
------------------
Prepare package for PyPi

3.1.0 (2022-07-13):
------------------
Add feature: Implement API feature "predict on many data-items" respectively "batch-inference"
for the MMOCRTextDetectionModel and MMOCRTextRecognitionModel

3.0.0 (2022-05-17):
------------------
Use new features from AnnotationClassMapper that have been added with mlcvzoo_base v3.0.0

2.0.1 (2022-05-16)
------------------
Changed python executable for distributed training
- It can happen that the system python and python for running code are not the same. When starting distributed training, the system python was called.
- Now the python executable that runs the code is also executed when starting distributed (multi gpu) training.

2.0.0 (2022-04-05)
------------------
- initial release of the package
