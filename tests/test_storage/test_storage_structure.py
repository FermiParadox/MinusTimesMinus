from unittest import TestCase


class Test_StorageStructure(TestCase):

    def test_structure(self):
        from main import _store
        # Must be a dict of dicts, with 2nd-level values not being containers.
        for k1, d in _store._data.items():
            self.assertIsInstance(d, dict)

            for k2, v2 in d.items():
                self.assertNotIsInstance(v2, dict)
                self.assertNotIsInstance(v2, tuple)
                self.assertNotIsInstance(v2, list)
                self.assertNotIsInstance(v2, set)


