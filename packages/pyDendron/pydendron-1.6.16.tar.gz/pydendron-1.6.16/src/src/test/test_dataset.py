import unittest
from pyDendron.dataset import Dataset

#  test unitaire de la classe Dataset
class TestDataset(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset()

    def test_is_empty(self):
        self.assertTrue(self.dataset.is_empty())

    def test_new_dataset(self):
        new_dataset = Dataset.new_dataset()
        self.assertIsInstance(new_dataset, Dataset)

    def test_new_root(self):
        self.dataset.new_root()
        self.assertEqual(len(self.dataset.get_roots()), 1)

    def test_new_trash(self):
        self.dataset.new_trash()
        self.assertEqual(len(self.dataset.get_roots()), 1)

    def test_new_clipboard(self):
        self.dataset.new_clipboard()
        self.assertEqual(len(self.dataset.get_roots()), 1)

    def test_new(self):
        self.dataset.new('keycode', 'category', 0)
        self.assertEqual(len(self.dataset.get_roots()), 1)

    def test_copy(self):
        triplets = [(0, 0, 0)]
        dest_path = [0]
        result = self.dataset.copy(triplets, dest_path)
        self.assertEqual(result, 'Success')

    def test_cut(self):
        triplets = [(0, 0, 0)]
        dest_path = [0]
        result = self.dataset.move(triplets, dest_path)
        self.assertEqual(result, 'Success')

    def test_drop(self):
        triplets = [(0, 0, 0)]
        result = self.dataset.drop(triplets)
        self.assertEqual(result, 'Success')

    def test_soft_drop(self):
        pairs = [(0, 0)]
        result = self.dataset.soft_drop(pairs)
        self.assertEqual(result, 'Success')

    def test_clean(self):
        self.dataset.clean()
        self.assertTrue(self.dataset.is_empty())

    def test_append(self):
        dataset2 = Dataset()
        self.dataset.append(dataset2)
        self.assertEqual(len(self.dataset.get_roots()), 0)

    def test_reindex(self):
        self.dataset.reindex()
        self.assertEqual(len(self.dataset.get_roots()), 0)

    def test_get_roots(self):
        roots = self.dataset.get_roots()
        self.assertEqual(len(roots), 0)

    def test_get_leafs(self):
        leafs = self.dataset.get_leafs()
        self.assertEqual(len(leafs), 0)

    def test_get_sequences(self):
        sequences = self.dataset.get_sequences(0)
        self.assertEqual(len(sequences), 0)

    def test_get_components(self):
        components = self.dataset.get_components()
        self.assertEqual(len(components), 0)

    def test_package_keys(self):
        keys = self.dataset.package_keys()
        self.assertEqual(len(keys), 0)

    def test_set_package(self):
        self.dataset.set_package('key', [(0, 0)])
        self.assertEqual(len(self.dataset.get_package('key')), 1)

    def test_delete_package(self):
        self.dataset.set_package('key', [(0, 0)])
        self.dataset.delete_package('key')
        self.assertEqual(len(self.dataset.package_keys()), 0)

if __name__ == '__main__':
    unittest.main()
