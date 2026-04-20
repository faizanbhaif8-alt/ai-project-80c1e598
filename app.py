from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'

# Create database tables
with app.app_context():
    db.create_all()

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Add new task
        task_content = request.form['content']
        if task_content.strip():  # Check if content is not empty
            new_task = Task(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'
    
    # Get all tasks ordered by creation date
    tasks = Task.query.order_by(Task.date_created).all()
    return render_template('index.html', tasks=tasks)

# Route to mark task as completed
@app.route('/complete/<int:id>')
def complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed  # Toggle completion status
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue updating your task'

# Route to delete a task
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting your task'

# Route to view active tasks
@app.route('/active')
def active_tasks():
    active_tasks = Task.query.filter_by(completed=False).order_by(Task.date_created).all()
    return render_template('index.html', tasks=active_tasks)

# Route to view completed tasks
@app.route('/completed')
def completed_tasks():
    completed_tasks = Task.query.filter_by(completed=True).order_by(Task.date_created).all()
    return render_template('index.html', tasks=completed_tasks)

# API endpoint to get all tasks (for potential future extensions)
@app.route('/api/tasks')
def get_tasks():
    tasks = Task.query.order_by(Task.date_created).all()
    task_list = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'content': task.content,
            'completed': task.completed,
            'date_created': task.date_created.strftime('%Y-%m-%d %H:%M:%S')
        }
        task_list.append(task_data)
    return jsonify(task_list)

if __name__ == '__main__':
    app.run(debug=True)