# Validation Plan: HippoVolume.AI

## Intended Use

HippoVolume.AI is a decision-support tool intended to assist radiologists and
neurologists in quantifying hippocampal volume from T2 MRI brain studies, as
part of the workup and longitudinal monitoring of patients with suspected or
diagnosed Alzheimer's disease (AD) and other conditions associated with
hippocampal atrophy (e.g. temporal lobe epilepsy, other dementias).

The algorithm is intended to run automatically on studies that have already
been pre-processed by a "HippoCrop" tool, which isolates a small rectangular
volume of interest around the right hippocampus from a full-head T2 MRI
series. It segments the anterior and posterior portions of the hippocampus on
each axial slice of the cropped volume, computes their voxel volumes, and
returns a DICOM Secondary Capture report to the ordering PACS for viewing
alongside the original study.

The tool is **not** intended to be used as a sole diagnostic device. It is
intended for use only on adult patients (18+) whose studies were correctly
routed through HippoCrop, and its output must always be reviewed and
confirmed by a qualified radiologist before being used for clinical
decision-making. It is not validated for pediatric populations, non-T2
sequences, other imaging modalities (CT, PET), left hippocampus measurement,
or general whole-brain segmentation tasks.

## Training Data

The model was trained and validated using the "Hippocampus" dataset from the
[Medical Segmentation Decathlon](http://medicaldecathlon.com/). The source
images are T2-weighted full-brain MRI volumes, from which a rectangular
region of interest around the hippocampus was cropped, reducing the imaging
field of view and the overall size and complexity of the training data. The
scans were acquired at multiple clinical sites and represent a mix of
patients with normal hippocampal anatomy and patients with anatomical
findings requiring image-guided radiotherapy planning, providing some
variability in shape, size, and image quality.

Because the dataset is de-identified and released publicly for research and
competition use, no direct patient demographic information (age, sex, scanner
vendor, field strength) is available in this project.  This is a materially
limiting factor for this validation and is called out further below.

## Labeling of Training Data

Ground truth segmentation masks were provided as part of the Medical
Segmentation Decathlon and represent expert-annotated (radiologist/expert
rater) voxel-wise labels of the anterior and posterior portions of the
hippocampus for each volume, distributed alongside the original imaging data.
No additional manual re-labeling was performed as part of this project;
masks were consumed as-is. Class labels used were: `0` = background, `1` =
anterior hippocampus, `2` = posterior hippocampus.

## Training Performance and Estimating Real-World Performance

The training performance of the segmentation model was measured using the
**Dice similarity coefficient** and the **Jaccard (IoU) index**, computed
per-volume against the held-out expert-labeled masks in the Decathlon test
split (a subset of the labeled data not used during training). Across the
held-out test volumes, the model achieved:

* Mean Dice coefficient: **0.858**
* Mean Jaccard index: **0.760**

These metrics were chosen because they are the standard for evaluating
volumetric medical image segmentation and directly reflect how closely the
predicted mask overlaps with the expert-defined ground truth, which in turn
determines the accuracy of the derived volume measurement that is the
clinical output of this tool.

Estimating real-world performance requires a validation study that goes
beyond this retrospective, single-source dataset. The recommended approach
is:

1. **Prospective/held-out multi-site validation** — collect a new,
   independent cohort of MRI studies (ideally from multiple institutions,
   scanner vendors, and field strengths) that were *not* part of the
   Decathlon dataset, along with expert (ideally multi-rater consensus)
   segmentations, to check that the reported Dice/Jaccard performance
   generalizes outside of the original data distribution.
2. **Clinical concordance study** — compare the algorithm's volume
   measurements against manual volumetric measurements performed by
   radiologists on the same studies, using a Bland-Altman analysis to
   establish the bias and limits of agreement between AI-derived and
   human-derived volumes, and comparing measurement variability to
   established inter-rater variability among human experts.
3. **Longitudinal consistency check** — since the clinical use case is
   tracking hippocampal volume *change* over time, evaluate test-retest and
   scan-rescan reliability of the algorithm's measurements to ensure that
   observed volume changes reflect true biological change rather than model
   noise.
4. **Population normative comparison** — cross-reference algorithm output
   against published normative volume ranges (e.g. HippoFit calculators)
   stratified by age, sex, and hemisphere, to sanity-check that outputs fall
   within physiologically plausible ranges.

## Expected Data Performance Envelope

**The algorithm is expected to perform well on:**

* T2-weighted MRI volumes that have been correctly cropped by the HippoCrop
  tool to isolate the region around the right hippocampus, with similar
  field-of-view, resolution, and voxel spacing to the training data.
* Adult patients with anatomy broadly similar to the training cohort
  (typical of an outpatient neurology/memory-clinic population undergoing
  routine dementia workup).
* Cases where hippocampal atrophy/shape variation falls within the range
  represented in the Decathlon training data (mild-to-moderate atrophy,
  typical AD-pattern volume loss).

**The algorithm is not expected to perform well, and should not be relied
upon, for:**

* Series that were not run through HippoCrop, are not T2-weighted, or that
  represent the full head/brain rather than the cropped hippocampal region
  — the model was never trained on such inputs and its output would be
  meaningless.
* Pediatric patients, since the training data source population skews adult
  and pediatric hippocampal anatomy differs substantially.
* Studies with severe motion artifact, unusual scan angulation, prior
  surgical resection, large space-occupying lesions, or other gross
  anatomical distortion near the hippocampus, since these deviate strongly
  from the training distribution.
* Scanners/sites/protocols very different from those represented in the
  Decathlon dataset (e.g. very low field strength, non-standard sequences),
  since no data from such sources was available for training and no
  systematic evaluation of scanner-related domain shift has been performed.
* Left hippocampus volume — the current pipeline and report are scoped to
  the right hippocampus only, consistent with the training data.

Given the limited demographic metadata available in the training set, a key
recommendation of this validation plan is that any real-world deployment be
paired with active post-market surveillance (spot-checking a sample of
AI-generated reports against radiologist measurements) until the prospective
multi-site validation described above has been completed.

# Others

This is a project associated to course 2 of Udacity's AI for Healthcare Nanodegree: "Applying AI to 3D Medical Imaging Data".
