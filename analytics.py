def list_all_habits(habits):
    """
    Return the names of all tracked habits.

    Args:
        habits (list): The list of habits.

    Returns:
        list: The names of all habits.
    """
    return [habit.name for habit in habits]

def list_habits_by_periodicity(habits, periodicity):
    """
    Return the names of all habits with the given periodicity.

    Args:
        habits (list): The list of habits.
        periodicity (str): The periodicity to filter by.

    Returns:
        list: The names of matching habits.
    """
    return [habit.name for habit in habits if habit.periodicity == periodicity]

def longest_streak_all(habits):
    """
    Return the longest streak among all habits.

    Args:
        habits (list): The list of habits.

    Returns:
        int: The longest streak found.
    """
    from DiabetesTracker import StreakCalculator  # Import inside the function
    return max((StreakCalculator.calculate_streak(h) for h in habits), default=0)

def longest_streak_for_habit(habit):
    """
    Return the longest streak for a specific habit.

    Args:
        habit: The habit to analyze.

    Returns:
        int: The longest streak for the habit.
    """
    from DiabetesTracker import StreakCalculator  # Import inside the function
    return StreakCalculator.calculate_streak(habit)