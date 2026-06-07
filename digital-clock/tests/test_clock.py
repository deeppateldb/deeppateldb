"""Unit tests for digital clock application"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli_clock import MultiTimezoneClock
import pytz
from datetime import datetime

class TestMultiTimezoneClock(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.clock = MultiTimezoneClock(['UTC', 'America/New_York', 'Europe/London'])
    
    def test_initialization(self):
        """Test clock initialization"""
        self.assertEqual(len(self.clock.timezones), 3)
        self.assertIn('UTC', self.clock.timezones)
    
    def test_add_timezone(self):
        """Test adding a timezone"""
        initial_count = len(self.clock.timezones)
        self.clock.add_timezone('Asia/Tokyo')
        self.assertEqual(len(self.clock.timezones), initial_count + 1)
        self.assertIn('Asia/Tokyo', self.clock.timezones)
    
    def test_add_duplicate_timezone(self):
        """Test that duplicate timezones are not added"""
        initial_count = len(self.clock.timezones)
        self.clock.add_timezone('UTC')
        self.assertEqual(len(self.clock.timezones), initial_count)
    
    def test_remove_timezone(self):
        """Test removing a timezone"""
        self.clock.remove_timezone('UTC')
        self.assertNotIn('UTC', self.clock.timezones)
    
    def test_get_time(self):
        """Test getting time in a timezone"""
        time_utc = self.clock.get_time('UTC')
        self.assertIsNotNone(time_utc)
        self.assertIsInstance(time_utc, datetime)
    
    def test_get_time_invalid_timezone(self):
        """Test getting time with invalid timezone"""
        result = self.clock.get_time('Invalid/Timezone')
        self.assertIsNone(result)
    
    def test_get_all_times(self):
        """Test getting times from all timezones"""
        times = self.clock.get_all_times()
        self.assertEqual(len(times), len(self.clock.timezones))
        
        for tz, time in times.items():
            self.assertIn(tz, self.clock.timezones)
            self.assertIsInstance(time, datetime)
    
    def test_timezone_offset(self):
        """Test timezone offset calculation"""
        time_ny = self.clock.get_time('America/New_York')
        time_london = self.clock.get_time('Europe/London')
        time_utc = self.clock.get_time('UTC')
        
        # All times should be the same moment in time
        self.assertEqual(
            int(time_ny.timestamp()),
            int(time_london.timestamp())
        )
    
    def test_display_method(self):
        """Test that display method runs without error"""
        try:
            # Just ensure it doesn't raise an exception
            # We can't easily test the output since it's printed
            self.clock.display(format_24h=True)
            self.clock.display(format_24h=False)
        except Exception as e:
            self.fail(f"display() raised {type(e).__name__} unexpectedly")

class TestTimezoneValidity(unittest.TestCase):
    
    def test_valid_timezones(self):
        """Test that common timezones are valid"""
        common_tzs = [
            'UTC', 'America/New_York', 'Europe/London',
            'Asia/Tokyo', 'Australia/Sydney', 'America/Los_Angeles'
        ]
        for tz in common_tzs:
            try:
                pytz.timezone(tz)
            except Exception as e:
                self.fail(f"Timezone {tz} is not valid: {e}")

if __name__ == '__main__':
    unittest.main()
