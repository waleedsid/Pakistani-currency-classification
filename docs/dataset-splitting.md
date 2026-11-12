# Reproducible dataset splitting

Run from the repository root using Python 3.8 or later; no extra packages needed:

```sh
python src/split_data.py --source data-rescaled --train-dest splits/run-42/train --test-dest splits/run-42/test --seed 42
python -m unittest discover -s tests -v
```

Input layout: `source/class_name/file.jpg`. Every regular file inside a class
folder is copied, so keep metadata outside class folders. Each class needs at
least two files. The training fraction defaults to 0.8, floored and clamped to
keep at least one file in both subsets. Source files are preserved.

Sorted filenames and a local seeded generator give repeatable membership for
the same input and Python runtime. Destinations must be absent or empty. Use
fresh paths for each run: this tool never deletes previous datasets. Overlapping
paths, nested class directories, symbolic links and invalid ratios are rejected.
A copy failure may leave partial output; resolve the error and use fresh paths.

Previously, rerunning the shuffled copy could leave an image in both train and
test, inflating evaluation scores. Rejecting populated output directories
prevents this stale-file leakage.

This is a filename-level split. Duplicates under different names, augmentations,
or photos of the same banknote may still cross subsets. These require
deduplication or grouping by banknote identity before augmentation. This change
does not train a model or establish its accuracy. Tests use synthetic file
contents to verify splitting and copying, not image decoding.

