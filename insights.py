# insights.py
import datetime
from database import select_all_tasks

import datetime

def calculate_average_task_completion_time(tasks):
    total_time = 0
    completed_tasks = 0
    for task in tasks:
        if task[6] == 1:  # Task is completed
            start_date = datetime.datetime.strptime(task[5], '%m/%d/%Y')
            completion_date = datetime.datetime.today()  # Assuming no separate completion date
            completion_time = completion_date - start_date
            total_time += completion_time.days
            completed_tasks += 1
    return total_time / completed_tasks if completed_tasks > 0 else 0

def calculate_priority_based_time_distribution(tasks):
    priority_time = {"high": 0, "medium": 0, "low": 0}
    for task in tasks:
        if task[6] == 1:  # Task is completed
            deadline = datetime.datetime.strptime(task[5], '%m/%d/%Y')
            completion_date = datetime.datetime.today()  # Assuming no separate completion date
            completion_time = completion_date - deadline
            priority_time[task[4].lower()] += completion_time.days  # Priority is task[4]
    return priority_time

def calculate_weekly_monthly_trends(tasks):
    tasks_per_week = {}
    tasks_per_month = {}
    for task in tasks:
        if task[6] == 1:  # Task is completed
            completion_date = datetime.datetime.today()  # Assuming today's date for testing
            week_number = completion_date.isocalendar()[1]
            month = completion_date.strftime('%Y-%m')
            tasks_per_week[week_number] = tasks_per_week.get(week_number, 0) + 1
            tasks_per_month[month] = tasks_per_month.get(month, 0) + 1
    return tasks_per_week, tasks_per_month

