# performance_insights_tab.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel
)
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet
from insights import calculate_average_task_completion_time, calculate_priority_based_time_distribution, calculate_weekly_monthly_trends

def performance_insights_tab(gui_instance):
    insights_widget = QWidget()
    insights_layout = QVBoxLayout()
    insights_widget.setLayout(insights_layout)

    # Average Task Completion Time
    average_time = calculate_average_task_completion_time(gui_instance.tasks)
    average_time_label = QLabel(f"Average Task Completion Time: {average_time} days")
    insights_layout.addWidget(average_time_label)

    # Priority-Based Time Distribution
    priority_time = calculate_priority_based_time_distribution(gui_instance.tasks)
    priority_pie_series = QPieSeries()
    priority_pie_series.append("High", priority_time["high"])
    priority_pie_series.append("Medium", priority_time["medium"])
    priority_pie_series.append("Low", priority_time["low"])
    priority_chart = QChart()
    priority_chart.legend().hide()
    priority_chart.addSeries(priority_pie_series)
    priority_chart.createDefaultAxes()
    priority_chart.setTitle("Priority-Based Time Distribution")
    priority_chart_view = QChartView(priority_chart)
    insights_layout.addWidget(priority_chart_view)

    # Weekly/Monthly Trends
    tasks_per_week, tasks_per_month = calculate_weekly_monthly_trends(gui_instance.tasks)
    week_bar_set = QBarSet("Tasks per Week")
    for week, count in tasks_per_week.items():
        week_bar_set.append(count)
    month_bar_set = QBarSet("Tasks per Month")
    for month, count in tasks_per_month.items():
        month_bar_set.append(count)
    trends_bar_series = QBarSeries()
    trends_bar_series.append(week_bar_set)
    trends_bar_series.append(month_bar_set)
    trends_chart = QChart()
    trends_chart.addSeries(trends_bar_series)
    trends_chart.setTitle("Weekly and Monthly Trends")
    trends_chart_view = QChartView(trends_chart)
    insights_layout.addWidget(trends_chart_view)

    if not gui_instance.tasks:
        no_data_label = QLabel("No sufficient data to provide time management insights.")
        insights_layout.addWidget(no_data_label)

    return insights_widget
