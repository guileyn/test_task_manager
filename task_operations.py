# task_operations.py
def update_task_list(tasks):
    task_titles = [f"{task[1]} {task[2]} {task[3]} {task[4]} {task[5]}" for task in tasks]  # task[1]: title, task[4]: priority
    tasks_model.setStringList(task_titles)

def add_task(gui_instance):
    title = gui_instance.title_edit.text()
    description = gui_instance.description_edit.text()
    category = gui_instance.category_edit.text()
    priority = gui_instance.priority_dropdown.currentText()
    deadline = gui_instance.deadline_edit.text()
    if title and priority and deadline:
        task = (title, description, category, priority, deadline)
        insert_task(gui_instance.conn, task)
        gui_instance.update_task_list()
        gui_instance.status_label.setText("Task added successfully")
        gui_instance.clear_input_fields()
    else:
        gui_instance.status_label.setText("Please fill in title, priority, and deadline")

def delete_task(gui_instance):
    # Get the selected task from the list view
    selected_index = gui_instance.tasks_list_view.currentIndex()
    if not selected_index.isValid():
        gui_instance.status_label.setText("Please select a task to delete.")
        return

    # Retrieve the selected task's title (e.g., "Task Title - High")
    selected_task_title = gui_instance.tasks_model.data(selected_index, 0).split(" ")[0]

    # Find the task ID corresponding to the selected title
    task_id = None
    for task in gui_instance.tasks:
        if task[1] == selected_task_title:
            task_id = task[0]
            break

    if task_id:
        # Delete the task from the database
        delete_task(gui_instance.conn, task_id)
        gui_instance.update_task_list()
        gui_instance.status_label.setText("Task deleted successfully.")
    else:
        gui_instance.status_label.setText("Task not found in the database.")
