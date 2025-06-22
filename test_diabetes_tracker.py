import unittest
import os
from datetime import datetime, timedelta

from DiabetesTracker import (
    HabitManager, Habit, Periodicity, JSONStorage, StreakCalculator
)
from analytics import (
    list_all_habits,
    list_habits_by_periodicity,
    longest_streak_all,
    longest_streak_for_habit
)

class TestDiabetesHabitTracker(unittest.TestCase):

    def setUp(self):
        self.manager = HabitManager()
        self.manager.create_habit("Test Daily", Periodicity.DAILY, "Test daily habit")
        self.manager.create_habit("Test Weekly", Periodicity.WEEKLY, "Test weekly habit")

    def test_habit_creation(self):
        self.assertEqual(len(self.manager.habits), 2)
        self.assertEqual(self.manager.habits[0].name, "Test Daily")
        self.assertEqual(self.manager.habits[1].periodicity, Periodicity.WEEKLY)

    def test_habit_completion(self):
        habit = self.manager.get_habit("Test Daily")
        habit.add_completion()
        self.assertEqual(len(habit.completions), 1)

    def test_analytics(self):
        # Add completions for streaks
        habit = self.manager.get_habit("Test Daily")
        today = datetime.now()
        for i in range(3):
            habit.add_completion(today - timedelta(days=i))
        self.assertEqual(longest_streak_for_habit(habit), 3)
        self.assertIn("Test Daily", list_all_habits(self.manager.habits))
        self.assertIn("Test Daily", list_habits_by_periodicity(self.manager.habits, Periodicity.DAILY))
        self.assertEqual(longest_streak_all(self.manager.habits), 3)

    def test_persistence(self):
        filename = "test_habits.json"
        JSONStorage.save_habits(self.manager.habits, filename)
        loaded = JSONStorage.load_habits(filename)
        self.assertEqual(len(loaded), 2)
        os.remove(filename)  # Clean up

if __name__ == "__main__":
    unittest.main()