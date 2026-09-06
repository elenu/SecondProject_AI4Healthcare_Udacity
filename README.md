# HippoVolume.AI

HippoVolume.AI is a decision-support tool that helps quantify hippocampal volume from T2-weighted MRI brain studies. It was developed as part of Udacity’s AI for Healthcare Nanodegree and is intended to support radiologists and neurologists in the assessment and monitoring of conditions associated with hippocampal atrophy, such as Alzheimer’s disease.

## Project Overview

The pipeline is designed to work on MRI studies that have already been pre-processed by **HippoCrop**, which isolates a region of interest around the right hippocampus. The model segments the anterior and posterior hippocampus on each axial slice, computes their voxel volumes, and generates a DICOM Secondary Capture report for review in PACS.

## Intended Use

This tool is intended for adult patients (18+) and should be used only as a clinical support aid. It is **not** intended to be used as a standalone diagnostic device. Final interpretation must always be performed by a qualified radiologist.

The model is not validated for:
- pediatric patients
- non-T2 sequences
- CT, PET, or other imaging modalities
- left hippocampus measurement
- full-brain segmentation tasks

## Training Data

The model was trained and validated using the **Hippocampus** dataset from the [Medical Segmentation Decathlon](http://medicaldecathlon.com/). The dataset contains de-identified, publicly available T2-weighted MRI volumes with expert-annotated segmentation masks.

## Labeling

Ground truth labels were provided as part of the dataset and represent expert-annotated voxel-wise masks of:
- `0` = background
- `1` = anterior hippocampus
- `2` = posterior hippocampus

No additional manual relabeling was performed.

## Results

Model performance was evaluated using standard medical image segmentation metrics:

| Metric | Score |
|--------|-------|
| Dice coefficient | 0.858 |
| Jaccard index | 0.760 |

These results were measured on the held-out test split from the dataset.

## Validation Considerations

To assess real-world performance, further validation would be needed through:
- prospective multi-site testing
- clinical concordance studies against manual measurements
- longitudinal reliability analysis
- comparison with normative hippocampal volume ranges

## Expected Performance

The model is expected to perform best on:
- T2-weighted MRI volumes correctly cropped by HippoCrop
- adult patients with anatomy similar to the training data
- cases within the range of hippocampal variation represented in the dataset

The model may perform poorly on:
- uncropped or non-T2 studies
- pediatric cases
- scans with severe motion artifact or unusual anatomy
- scanners or protocols very different from the training data

## Notes

This project was completed as part of Udacity’s AI for Healthcare Nanodegree, course 2: **Applying AI to 3D Medical Imaging Data**.
