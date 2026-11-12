"""Reproducible per-class dataset splits into fresh destinations."""
import argparse
from pathlib import Path
import random
import shutil


def split_data(source, train_dest, test_dest, split_ratio=0.8, seed=42):
    if not 0 < split_ratio < 1:
        raise ValueError('split_ratio must be strictly between 0 and 1')
    source, train_dest, test_dest = [Path(p).resolve() for p in (source, train_dest, test_dest)]
    paths = (source, train_dest, test_dest)
    for i, a in enumerate(paths):
        for b in paths[i + 1:]:
            if a == b or a in b.parents or b in a.parents:
                raise ValueError('Source, train and test paths must not overlap')
    if not source.is_dir():
        raise ValueError('Source must be an existing directory')
    for dest in (train_dest, test_dest):
        if dest.exists() and (not dest.is_dir() or any(dest.iterdir())):
            raise ValueError('Destinations must be absent or empty; use fresh output paths')
    rng = random.Random(seed)
    plan, counts = [], {}
    for folder in sorted(source.iterdir()):
        if folder.is_symlink():
            raise ValueError('Symbolic links are not supported')
        if not folder.is_dir():
            continue
        images = sorted(folder.iterdir())
        if any(p.is_symlink() or not p.is_file() for p in images):
            raise ValueError('Class folders must contain regular files only')
        if len(images) < 2:
            raise ValueError('Each class must contain at least two files')
        rng.shuffle(images)
        index = max(1, min(len(images) - 1, int(len(images) * split_ratio)))
        counts[folder.name] = {'train': index, 'test': len(images) - index}
        for dest, subset in ((train_dest, images[:index]), (test_dest, images[index:])):
            plan.extend((p, dest / folder.name / p.name) for p in subset)
    if not plan:
        raise ValueError('Source must contain nonempty class directories')
    # Validate all classes before writing output.
    for image, dest in plan:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(image, dest)
    return counts


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=root / 'data-rescaled')
    parser.add_argument('--train-dest', type=Path, default=root / 'data' / 'train')
    parser.add_argument('--test-dest', type=Path, default=root / 'data' / 'test')
    parser.add_argument('--split-ratio', type=float, default=0.8)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    try:
        counts = split_data(args.source, args.train_dest, args.test_dest, args.split_ratio, args.seed)
    except (ValueError, OSError) as error:
        parser.exit(2, f'Split failed: {error}\n')
    for label, count in counts.items():
        print(f'{label}: {count}')


if __name__ == '__main__':
    main()
