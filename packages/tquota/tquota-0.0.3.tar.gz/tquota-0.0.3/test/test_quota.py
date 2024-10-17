import unittest
import time
from tquota import Quota

class TestQuota(unittest.TestCase):

    def test_initialization_valid(self):
        """Test that valid initialization works properly."""
        quota = Quota('1h', '5m')
        self.assertEqual(quota.quota_time, 3600)
        self.assertEqual(quota.gap_time, 300)

    def test_initialization_invalid_time_format(self):
        """Test that invalid time formats raise a ValueError."""
        with self.assertRaises(ValueError):
            Quota('invalid', '5m')

    def test_to_seconds(self):
        """Test conversion from time format to seconds."""
        quota = Quota('1h')
        self.assertEqual(quota._to_seconds('30s'), 30)
        self.assertEqual(quota._to_seconds('5m'), 300)
        self.assertEqual(quota._to_seconds('2h'), 7200)
        self.assertEqual(quota._to_seconds('1d'), 86400)

    def test_hastime_before_gap(self):
        """Test hastime returns True before gap time is reached."""
        quota = Quota('1m', '10s')
        time.sleep(2)  # Sleep for a few seconds to simulate execution
        self.assertTrue(quota.hastime())

    def test_time_up_after_quota(self):
        """Test time_up returns True after quota time is reached."""
        quota = Quota('3s', '1s')
        time.sleep(4)  # Sleep to exceed quota time
        self.assertTrue(quota.time_up())

    def test_dynamic_gap_time_auto(self):
        """Test automatic gap time adjustment based on execution times."""
        quota = Quota('10s', 'auto')  # Set gap time to auto
        for _ in range(5):  # Simulate loop execution
            time.sleep(0.5)  # Each iteration takes ~0.5s
            quota.hastime()  # This will update the gap time
        self.assertGreater(quota.gap_time, 0.4)  # Check if gap time was adjusted

    def test_format_time(self):
        """Test that the time formatting function works as expected."""
        quota = Quota('1h')
        formatted_time = quota._format_time(3661)
        self.assertEqual(formatted_time, '1h:1m:1s')

    def test_remaining_time(self):
        """Test remaining time calculation."""
        quota = Quota('10s')
        time.sleep(3)
        remaining = quota._remaining_time()
        self.assertLessEqual(remaining, 7)

    def test_gap_time_greater_than_quota(self):
        """Test that setting gap time greater than quota raises an error."""
        with self.assertRaises(ValueError):
            Quota('5m', '10m')

    def test_logging_enabled(self):
        """Test that logging can be enabled without errors."""
        quota = Quota('10s', enable_logging=True)
        self.assertTrue(quota.enable_logging)

if __name__ == '__main__':
    unittest.main()
