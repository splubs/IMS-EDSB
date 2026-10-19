"""Data integrity tests for the course-provided Telco workbooks."""
import unittest
from src.data import load_tables, validate_tables, load_customers, load_core_population
from src.features import FEATURES, FORBIDDEN, make_xy


class DataChecks(unittest.TestCase):
    def test_expected_source_grain(self):
        t=load_tables()
        validate_tables(t)
        self.assertEqual(len(t['demographics']),7043)
        self.assertEqual(len(t['population']),1671)

    def test_join_and_target(self):
        all_customers=load_customers()
        self.assertEqual(len(all_customers),7043)
        self.assertTrue(all_customers['Customer ID'].is_unique)
        core=load_core_population()
        self.assertEqual(len(core),6589)
        x,y=make_xy(core)
        self.assertEqual(int(y.sum()),1869)
        self.assertEqual(len(x),len(y))
        self.assertFalse(set(FEATURES)&FORBIDDEN)

    def test_literal_none_categories_preserved(self):
        s=load_tables()['services']
        self.assertEqual(int((s['Offer']=='None').sum()),3877)
        self.assertEqual(int((s['Internet Type']=='None').sum()),1526)


if __name__ == '__main__':
    unittest.main()
