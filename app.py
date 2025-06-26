
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key


week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
todo_dict = {day: [] for day in week}

@app.route('/')
def index():
    return render_template('index.html', todo_dict=todo_dict, week=week)

@app.route('/add_task', methods=['POST'])
def add_task():
    day = request.form.get('day')
    task = request.form.get('task')
    
    if day and task and day in week:
        todo_dict[day].append(task)
        flash(f'Task added to {day} successfully!', 'success')
    else:
        flash('Please fill in all fields correctly.', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_task/<day>/<int:task_index>')
def delete_task(day, task_index):
    if day in week and 0 <= task_index < len(todo_dict[day]):
        deleted_task = todo_dict[day].pop(task_index)
        flash(f'Task "{deleted_task}" deleted from {day}!', 'success')
    else:
        flash('Task not found.', 'error')
    
    return redirect(url_for('index'))

@app.route('/clear_day/<day>')
def clear_day(day):
    if day in week:
        todo_dict[day] = []
        flash(f'All tasks cleared from {day}!', 'success')
    else:
        flash('Invalid day.', 'error')
    
    return redirect(url_for('index'))

@app.route('/clear_all')
def clear_all():
    for day in week:
        todo_dict[day] = []
    flash('All tasks cleared from all days!', 'success')
    return redirect(url_for('index'))

@app.route('/initialize')
def initialize():
    return render_template('initialize.html', week=week)

@app.route('/initialize_tasks', methods=['POST'])
def initialize_tasks():
    # Clear existing tasks
    for day in week:
        todo_dict[day] = []
    
    # Add new tasks from form
    for day in week:
        tasks = request.form.getlist(f'{day}_tasks')
        todo_dict[day] = [task.strip() for task in tasks if task.strip()]
    
    flash('Todo list initialized successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



