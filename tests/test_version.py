import unittest
from version import Version


class VersionTestCase(unittest.TestCase):
    def test_version_single_digit(self):
        v = Version(version="1")

        self.assertEqual(v.parsed_version, (1,))
        self.assertEqual(v.version, "1")

    def test_version_multiple_digits(self):
        v = Version(version="1.2")

        self.assertEqual(v.parsed_version, (1, 2))
        self.assertEqual(v.version, "1.2")

        v = Version(version="1.2.3")

        self.assertEqual(v.parsed_version, (1, 2, 3))
        self.assertEqual(v.version, "1.2.3")

    def test_version_with_alpha(self):
        v = Version(version="1.2.3a")

        self.assertEqual(v.parsed_version, (1, 2, 3, 'a'))
        self.assertEqual(v.version, "1.2.3a")

    def test_version_with_tag(self):
        v = Version(version="1.2.3.devel")

        self.assertEqual(v.parsed_version, (1, 2, 3, 'devel'))
        self.assertEqual(v.version, "1.2.3.devel")

        v2 = Version(version="1.2.3.beta1.2.release")

        self.assertEqual(v2.parsed_version, (1, 2, 3, 'beta', 1, 2, 'release'))
        self.assertEqual(v2.version, "1.2.3.beta1.2.release")

    def test_version_multiple_delimiters(self):
        v = Version(version='1.0-1', delimiters=('.', '-'))
        self.assertEqual(v.parsed_version, (1, 0, 1))
        self.assertEqual(v.version, "1.0-1")

    def test_version_with_no_numbers(self):
        v = Version(version='a-a', delimiters=('.', '-'))

        self.assertEqual(v.parsed_version, ('a','a'))

    def test_version_with_no_alpha_or_digits(self):
        v = Version(version='-.', delimiters=('.', '-'))

        self.assertEqual(v.parsed_version, tuple())

    def test_version_uninitialized(self):
        v = Version()

        self.assertEqual(v.parsed_version, None)
        self.assertEqual(v.version, None)

    def test_split_version_string(self):
        r1 = Version.split("1.2.3", '.')
        self.assertEqual(r1, ['1', '.', '2', '.', '3'])

        r2 = Version.split("1.2.3-tst", '.', '-')
        self.assertEqual(r2, ['1', '.', '2', '.', '3', '-', 't', 's', 't'])

    def test_hash(self):
        v1 = Version("1.0")
        v2 = Version("2.0")
        v3 = Version("2.0")

        self.assertNotEqual(v1.__hash__(), v2.__hash__())
        self.assertEqual(v2.__hash__(), v3.__hash__())
        self.assertEqual(len({v1, v2, v3}), 2)

    def test_version_equality(self):
        v1 = Version("1.0")
        v2 = Version("1.0")
        v3 = Version("2.0")
        v4 = "4.0"
        v5 = "1.0.0.0"

        self.assertTrue(v1 == v2)
        self.assertTrue(v1 == v5)
        self.assertFalse(v1 == v3)
        self.assertFalse(v1 == v4)

    def test_version_equality_case_sensitivity(self):
        v1 = Version("1.0a", case_sensitive=False)
        v2 = Version("1.0A", case_sensitive=False)
        v3 = Version("1.0A", case_sensitive=True)
        v4 = Version("1.0B", case_sensitive=True)
        v5 = Version("1.01", case_sensitive=False)

        self.assertTrue(v1 == v2)
        self.assertFalse(v3 == v1)
        self.assertTrue(v1 == v3)
        self.assertFalse(v1 == v4)
        self.assertFalse(v5 == v4)

    def test_version_inequality(self):
        v1 = Version("1.0")
        v2 = Version("2.0")
        v3 = "2.0"
        v4 = "1.0"

        self.assertTrue(v1 != v2)
        self.assertTrue(v1 != v3)
        self.assertFalse(v1 != v4)

    def test_version_inequality_case_sensitivity(self):
        v1 = Version("1.0a", case_sensitive=False)
        v2 = Version("1.0A", case_sensitive=False)
        v3 = Version("1.0A", case_sensitive=True)

        self.assertTrue(v3 != v1)
        self.assertFalse(v2 != v3)

    def test_greater_than(self):
        v1 = Version("1.0")
        v2 = Version("2.0")
        v3 = "2.0"

        self.assertTrue(v2 > v1)
        self.assertFalse(v1 > v3)
        self.assertFalse(v1 > v1)

    def test_greater_than_case_sensitivity(self):
        v1 = Version("1.0a", case_sensitive=False)
        v2 = Version("1.0A", case_sensitive=False)
        v3 = Version("2.0A", case_sensitive=True)

        self.assertFalse(v1 > v3)
        self.assertTrue(v3 > v1)
        self.assertFalse(v2 > v1)
    @unittest.skip
    def test_greater_or_equal(self):
        v1 = Version("1.0")
        v2 = Version("2.0")
        v3 = Version("2.0")

        self.assertGreaterEqual(v2, v1)
        self.assertGreaterEqual(v2, v3)
    @unittest.skip
    def test_greater_or_equal_case_sensitivity(self):
        v1 = Version("1.0a", case_sensitive=False)
        v2 = Version("1.0A", case_sensitive=False)
        v3 = Version("1.0A", case_sensitive=True)

        self.assertTrue(v1 >= v3)
        self.assertTrue(v2 >= v1)
        self.assertFalse(v3 >= v1)

    def test_less_than(self):
        v1 = Version("1.0")
        v2 = Version("2.0")

        self.assertTrue(v1 < v2)
        self.assertFalse(v2 < v1)

    def test_less_than_case_sensitivity(self):
        v1 = Version("1.0a", case_sensitive=False)
        v2 = Version("1.0A", case_sensitive=False)
        v3 = Version("2.0A", case_sensitive=True)

        self.assertTrue(v1 < v3)
        self.assertFalse(v2 < v1)
        self.assertFalse(v3 < v1)

    def test_less_or_equal(self):
        v1 = Version("1.0")
        v2 = Version("2.0")
        v3 = Version("1.0")

        self.assertLessEqual(v1, v2)
        self.assertLessEqual(v1, v3)

    def test_less_or_equal_case_sensitivity(self):
        v1 = Version("1.0a", case_sensitive=False)
        v2 = Version("1.0A", case_sensitive=False)
        v3 = Version("1.0A", case_sensitive=True)

        self.assertTrue(v3 <= v1)
        self.assertTrue(v1 <= v2)
        self.assertTrue(v2 <= v1)

    def test_comparisons_from_string(self):
        v1 = Version("3.0")
        v2 = "2.0"
        v3 = "3.0"
        v4 = "4.0"
        vA = Version("3.0a")
        vB = "3.0b"
        vC = "3.0a"
        vD = Version("3.0d")

        self.assertTrue(vA == vC)
        self.assertFalse(vA == vB)

        self.assertTrue(vA != vB)
        self.assertFalse(vA != vC)

        self.assertTrue(vD > vA)
        self.assertFalse(vA > vC)

        self.assertTrue(vD >= vA)
        self.assertFalse(vA >= vD)

        self.assertTrue(vA < vB)
        self.assertFalse(vB < vA)

        self.assertTrue(vA <= vC)
        self.assertFalse(vB <= vA)

    def test_comparison_of_equal_but_shorter_versions(self):
        v1 = Version('2.0')
        v2 = Version('2.0.0')
        v3 = Version('3.0.0.0')
        v4 = Version('2.0.1.0')

        self.assertTrue(v1 == v2)
        self.assertTrue(v2 == v1)
        self.assertFalse(v1 == v3)
        self.assertFalse(v3 == v1)
        self.assertFalse(v1 == v4)
        self.assertFalse(v4 == v1)

        self.assertTrue(v1 != v3)
        self.assertTrue(v3 != v1)
        self.assertFalse(v1 != v2)
        self.assertFalse(v2 != v1)

        self.assertTrue(v1 < v3)
        self.assertFalse(v3 < v1)
        self.assertFalse(v1 < v2)
        self.assertFalse(v2 < v1)

        self.assertTrue(v1 <= v3)
        self.assertTrue(v1 <= v2)
        self.assertFalse(v3 <= v1)
        self.assertTrue(v2 <= v1)

        self.assertFalse(v1 > v3)
        self.assertTrue(v3 > v1)
        self.assertFalse(v1 > v2)
        self.assertFalse(v2 > v1)

        self.assertFalse(v1 >= v3)
        self.assertTrue(v1 >= v2)
        self.assertTrue(v3 >= v1)
        self.assertTrue(v2 >= v1)

    def test_creating_from_int(self):
        v1 = Version(1)
        self.assertEqual(v1.parsed_version, (1,))
        self.assertEqual(v1.version, 1)

    def test_creating_from_float(self):
        v1 = Version(float(1.0))
        self.assertEqual(v1.parsed_version, (1,0))
        self.assertEqual(v1.version, 1.0)

    def test_repr(self):
        v = Version("1.0-a", ('.', '-'))
        self.assertEqual(repr(v), "<Version 1.0-a>")

    def test_str(self):
        v = Version("1.0-a")
        self.assertEqual(str(v), "1.0-a")

    def test_comparison_of_differing_versions(self):
        v1 = Version('a')
        v2 = Version('0')

        self.assertFalse(v1 < v2)
        self.assertFalse(v1 == v2)
        self.assertTrue(v1 != v2)
        self.assertFalse(v1 > v2)

        self.assertFalse(v2 < v1)
        self.assertFalse(v2 == v1)
        self.assertTrue(v2 != v1)
        self.assertFalse(v2 > v1)

    def test_uninitialized_comparison(self):
        v1 = Version()
        v2 = Version('0.0.0.0')

        self.assertFalse(v1 < v2)
        self.assertFalse(v1 == v2)
        self.assertTrue(v1 != v2)
        self.assertFalse(v1 > v2)

        self.assertFalse(v2 < v1)
        self.assertFalse(v2 == v1)
        self.assertTrue(v2 != v1)
        self.assertFalse(v2 > v1)

    def test_guessing_delimiters(self):
        self.assertEqual(Version.guess_delimiters("1.0"), {'.'})
        self.assertEqual(Version.guess_delimiters("1.0-1"), {'.', '-'})
        self.assertEqual(Version.guess_delimiters("1.0-abc_1#a"), {'-', '_','.', '#'})

if __name__ == '__main__':
    unittest.main()
