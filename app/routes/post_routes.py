from flask import Blueprint, request, jsonify
from extensions import db
from app.models.post import Post

post_bp = Blueprint('post', __name__)

# ✅ FIX: Changed route from '/' to '' (empty string) to prevent the redirect
@post_bp.route('', methods=['GET']) ## get all post 
def get_posts():
    posts = Post.query.all() ##fetch from DB
    return jsonify([post.to_dict()for post in posts]), 200

# ✅ FIX: Changed route from '/' to '' (empty string) to prevent the redirect
@post_bp.route('', methods=['POST'])
def add_post():
    data = request.get_json()
    new_post = Post(
        title=data.get('title'),
        content=data.get('content'),
        user_id=data.get('user_id')
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201

@post_bp.route('/<int:id>', methods=['PATCH'])
def update_status(id):
    post = Post.query.get_or_404(id)
    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    post.image_url = data.get('image_url', post.image_url)
    db.session.commit()
    return jsonify(post.to_dict()), 200

@post_bp.route('/<int:id>', methods=['DELETE']) ## deleting a route
def delete_item(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post) ## delete 
    db.session.commit()
    return jsonify({'message': 'Item deleted'}), 200