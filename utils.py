from datetime import datetime, timedelta

def get_priority():
    while True:
        priority = input("Enter priority (high, medium, low): ").lower()
        if priority in ['high', 'edium', 'low']:
            return priority
        print("Invalid priority. Please try again.")

def get_deadline():
    while True:
        deadline = input("Enter deadline (YYYY-MM-DD): ")
        try:
            datetime.strptime(deadline, '%Y-%m-%d')
            return deadline
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")

def check_overdue(deadline):
    deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
    return deadline_date < datetime.now()

def notify(task):
    print(f"Notification: {task['title']} is due on {task['deadline']}")
    if check_overdue(task['deadline']):
        print("Task is OVERDUE")