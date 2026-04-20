Here's the complete `models.py` file for a Flask-based To-Do List application using SQLAlchemy:

```python
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class Task(db.Model):
    """
    Task model representing a to-do item in the application.
    """
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, title, description=None):
        """
        Initialize a new Task instance.
        
        Args:
            title (str): The title of the task
            description (str, optional): Description of the task. Defaults to None.
        """
        self.title = title
        self.description = description

    def to_dict(self):
        """
        Convert the Task object to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the task
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_completed': self.is_completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    def mark_complete(self):
        """
        Mark the task as completed and set the completion timestamp.
        """
        self.is_completed = True
        self.completed_at = datetime.utcnow()

    def mark_incomplete(self):
        """
        Mark the task as incomplete and clear the completion timestamp.
        """
        self.is_completed = False
        self.completed_at = None

    def __repr__(self):
        """
        String representation of the Task object.
        """
        return f'<Task {self.id}: {self.title}>'
```

This models.py file includes:

1. All necessary imports (SQLAlchemy and datetime)
2. A Task model with all required fields:
   - id (primary key)
   - title (required)
   - description (optional)
   - created_at (auto-set on creation)
   - updated_at (auto-updated on changes)
   - is_completed (boolean flag)
   - completed_at (timestamp when marked complete)

3. Helper methods:
   - to_dict() for JSON serialization
   - mark_complete() and mark_incomplete() to change task status
   - __repr__ for debugging

4. Comprehensive docstrings explaining each component

The model follows best practices for Flask-SQLAlchemy applications and provides all the functionality needed for the To-Do List application. You'll need to initialize this model with your Flask app in your application factory or main file.