from extensions import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # The user_id of the person who created the post
    user_id = db.Column(db.Integer, nullable=False) 
    # Use a dummy integer for now until you integrate a proper User model foreign key
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Returns a dictionary representation of the post."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
            # Add relationships (likes/replies) here when you implement them
        }

    def __repr__(self):
        return f'<Post {self.id}: {self.title}>'
