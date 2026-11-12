import random
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from src.split_data import split_data


class SplitDataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        for label in ('10_front', '20_front'):
            folder = self.source / label
            folder.mkdir(parents=True)
            for i in range(10):
                (folder / f'{i}.jpg').write_bytes(f'{label}:{i}'.encode())
        self.train, self.test = self.root / 'train', self.root / 'test'

    def files(self, folder):
        return {str(p.relative_to(folder)): p.read_bytes()
                for p in folder.rglob('*') if p.is_file()}

    def test_partition_and_contents(self):
        counts = split_data(self.source, self.train, self.test)
        train, test = self.files(self.train), self.files(self.test)
        self.assertFalse(train.keys() & test.keys())
        self.assertEqual({**train, **test}, self.files(self.source))
        self.assertEqual(counts['10_front'], {'train': 8, 'test': 2})

    def test_reproducible_and_global_rng_unchanged(self):
        state = random.getstate()
        split_data(self.source, self.train, self.test)
        train2, test2 = self.root / 'train2', self.root / 'test2'
        split_data(self.source, train2, test2)
        self.assertEqual(self.files(self.train), self.files(train2))
        self.assertEqual(self.files(self.test), self.files(test2))
        self.assertEqual(state, random.getstate())

    def test_rerun_rejected_without_modification(self):
        split_data(self.source, self.train, self.test)
        before = self.files(self.train), self.files(self.test)
        with self.assertRaises(ValueError):
            split_data(self.source, self.train, self.test, seed=99)
        self.assertEqual(before, (self.files(self.train), self.files(self.test)))

    def test_invalid_ratios(self):
        for ratio in (0, 1, -1, 2, float('nan')):
            with self.subTest(ratio=ratio), self.assertRaises(ValueError):
                split_data(self.source, self.train, self.test, ratio)
        self.assertFalse(self.train.exists())

    def test_overlapping_paths(self):
        for train, test in ((self.source, self.test), (self.source / 'train', self.test),
                            (self.train, self.train / 'test'), (self.train, self.train)):
            with self.subTest(train=train, test=test), self.assertRaises(ValueError):
                split_data(self.source, train, test)

    def test_small_class_validated_before_copy(self):
        (self.source / 'z_empty').mkdir()
        with self.assertRaises(ValueError):
            split_data(self.source, self.train, self.test)
        self.assertFalse(self.train.exists())

    def test_extreme_ratio_keeps_both_subsets(self):
        counts = split_data(self.source, self.train, self.test, 0.01)
        self.assertEqual(counts['10_front'], {'train': 1, 'test': 9})

    def test_cli_and_rerun_error(self):
        script = Path(__file__).resolve().parents[1] / 'src' / 'split_data.py'
        command = [sys.executable, str(script), '--source', str(self.source),
                   '--train-dest', str(self.train), '--test-dest', str(self.test)]
        result = subprocess.run(command, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('10_front:', result.stdout)
        result = subprocess.run(command, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('fresh output paths', result.stderr)


if __name__ == '__main__':
    unittest.main()

