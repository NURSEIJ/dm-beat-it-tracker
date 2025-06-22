import json
from datetime import datetime, timedelta
from typing import List, Dict

class Periodicity:
    """
    Defines constants for habit periodicity: daily, weekly, or monthly.
    """
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

class Habit:
    """
    Represents a habit with a name, periodicity, task specification, creation date, and completion records.
    """

    def __init__(self, name: str, periodicity: str, task_spec: str, created_at: str = None):
        """
        Initialize a new Habit.

        Args:
            name (str): The name of the habit.
            periodicity (str): How often the habit should be completed (daily, weekly, monthly).
            task_spec (str): Description of the habit task.
            created_at (str, optional): The creation date/time as a string. Defaults to now.
        """
        self.name = name
        self.periodicity = periodicity
        self.task_spec = task_spec
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.completions: List[Dict] = []

    def add_completion(self, date: datetime = None):
        """
        Mark the habit as completed at the given date/time.

        Args:
            date (datetime, optional): The date and time of completion. Defaults to now.
        """
        if date is None:
            date = datetime.now()
        self.completions.append({'date': date.strftime('%Y-%m-%d')})

class HabitManager:
    """
    Manages a collection of habits, allowing creation, deletion, and retrieval.
    """

    def __init__(self):
        """
        Initialize the HabitManager with an empty list of habits.
        """
        self.habits: List[Habit] = []

    def create_habit(self, name: str, periodicity: str, task_spec: str):
        """
        Create and add a new habit.

        Args:
            name (str): The name of the habit.
            periodicity (str): The periodicity of the habit.
            task_spec (str): The task description.
        """
        habit = Habit(name, periodicity, task_spec)
        self.habits.append(habit)

    def delete_habit(self, name: str):
        """
        Delete a habit by name.

        Args:
            name (str): The name of the habit to delete.
        """
        self.habits = [h for h in self.habits if h.name != name]

    def get_habit(self, name: str):
        """
        Retrieve a habit by name.

        Args:
            name (str): The name of the habit to retrieve.

        Returns:
            Habit or None: The habit if found, else None.
        """
        for habit in self.habits:
            if habit.name == name:
                return habit
        return None

class StreakCalculator:
    """
    Provides methods to calculate habit streaks.
    """

    @staticmethod
    def calculate_streak(habit: Habit) -> int:
        """
        Calculate the longest streak for a given habit.

        Args:
            habit (Habit): The habit to analyze.

        Returns:
            int: The longest streak.
        """
        if not habit.completions:
            return 0
        dates = sorted([datetime.strptime(c['date'], '%Y-%m-%d') for c in habit.completions])
        streak = 1
        max_streak = 1
        for i in range(1, len(dates)):
            delta = (dates[i] - dates[i-1]).days
            if habit.periodicity == Periodicity.DAILY and delta == 1:
                streak += 1
            elif habit.periodicity == Periodicity.WEEKLY and delta <= 7:
                streak += 1
            elif habit.periodicity == Periodicity.MONTHLY and delta <= 31:
                streak += 1
            else:
                streak = 1
            max_streak = max(max_streak, streak)
        return max_streak

class JSONStorage:
    """
    Handles saving and loading habits to and from a JSON file.
    """

    @staticmethod
    def save_habits(habits: List[Habit], filename: str):
        """
        Save the list of habits to a JSON file.

        Args:
            habits (List[Habit]): The list of habits to save.
            filename (str): The filename to save to.
        """
        data = []
        for habit in habits:
            data.append({
                'name': habit.name,
                'periodicity': habit.periodicity,
                'task_spec': habit.task_spec,
                'created_at': habit.created_at,
                'completions': habit.completions
            })
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load_habits(filename: str) -> List[Habit]:
        """
        Load habits from a JSON file.

        Args:
            filename (str): The filename to load from.

        Returns:
            List[Habit]: The list of loaded habits.
        """
        habits = []
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                for h in data:
                    habit = Habit(
                        h['name'],
                        h['periodicity'],
                        h['task_spec'],
                        h.get('created_at')
                    )
                    habit.completions = h['completions']
                    habits.append(habit)
        except FileNotFoundError:
            pass
        return habits

# Import analytics functions (no circular import issue)
from analytics import (
    list_all_habits,
    list_habits_by_periodicity,
    longest_streak_all,
    longest_streak_for_habit
)

def print_menu():
    """
    Print the main menu options for the CLI.
    """
    print("\nDiabetes Habit Tracker")
    print("1. List all habits")
    print("2. List habits by periodicity")
    print("3. Create a new habit")
    print("4. Complete a habit")
    print("5. Delete a habit")
    print("6. Show longest streak (all habits)")
    print("7. Show longest streak for a habit")
    print("8. Save habits")
    print("9. Load habits")
    print("0. Exit")

def main():
    """
    Main loop for the CLI interface.
    Predefines 5 habits and adds completion data for 4 weeks for each.
    """
    manager = HabitManager()
    filename = "habits.json"

    # --- Predefined habits and completion data for 4 weeks ---
    predefined_habits = [
        ("Check blood sugar", Periodicity.DAILY, "Check and record blood sugar level"),
        ("Exercise", Periodicity.WEEKLY, "30 minutes of exercise"),
        ("Take medication", Periodicity.DAILY, "Take prescribed diabetes medication"),
        ("Log meals", Periodicity.DAILY, "Record all meals"),
        ("Walk 10,000 steps", Periodicity.WEEKLY, "Walk at least 10,000 steps in a week"),
    ]

    # Create habits
    for name, periodicity, task_spec in predefined_habits:
        manager.create_habit(name, periodicity, task_spec)

    # Add completion data for 4 weeks (simulate)
    today = datetime.now()
    for habit in manager.habits:
        if habit.periodicity == Periodicity.DAILY:
            # Add 28 daily completions (4 weeks)
            for days_ago in range(27, -1, -1):
                habit.add_completion(today - timedelta(days=days_ago))
        elif habit.periodicity == Periodicity.WEEKLY:
            # Add 4 weekly completions (1 per week)
            for weeks_ago in range(3, -1, -1):
                habit.add_completion(today - timedelta(weeks=weeks_ago))
    # --- End of predefined data ---

    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            print("All habits:")
            for habit in manager.habits:
                print(f"- {habit.name} (Created: {habit.created_at}, Periodicity: {habit.periodicity})")
        elif choice == "2":
            period = input("Enter periodicity (daily/weekly/monthly): ").lower()
            filtered = list_habits_by_periodicity(manager.habits, period)
            print(f"Habits with periodicity '{period}': {filtered}")
        elif choice == "3":
            name = input("Enter habit name: ")
            periodicity = input("Enter periodicity (daily/weekly/monthly): ").lower()
            task_spec = input("Enter task description: ")
            manager.create_habit(name, periodicity, task_spec)
            print("Habit created.")
        elif choice == "4":
            name = input("Enter habit name to complete: ")
            habit = manager.get_habit(name)
            if habit:
                habit.add_completion()
                print("Habit marked as completed.")
            else:
                print("Habit not found.")
        elif choice == "5":
            name = input("Enter habit name to delete: ")
            manager.delete_habit(name)
            print("Habit deleted (if it existed).")
        elif choice == "6":
            print("Longest streak (all habits):", longest_streak_all(manager.habits))
        elif choice == "7":
            name = input("Enter habit name: ")
            habit = manager.get_habit(name)
            if habit:
                print(f"Longest streak for '{name}':", longest_streak_for_habit(habit))
            else:
                print("Habit not found.")
        elif choice == "8":
            JSONStorage.save_habits(manager.habits, filename)
            print("Habits saved.")
        elif choice == "9":
            manager.habits = JSONStorage.load_habits(filename)
            print("Habits loaded.")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()