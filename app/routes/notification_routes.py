from flask import Blueprint, request, jsonify
from extensions import db
from app.models.notification import Notification

notification_bp = Blueprint('notification', __name__) ##tell flask where to find 

