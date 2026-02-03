from flask import Blueprint, request, jsonify
from models.task import Task
from utils.auth_helper import token_required
from utils.validators import validate_task_data
import logging

logger = logging.getLogger(__name__)

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    title = data.get('title', '')
    description = data.get('description', '')
    
    # Validate
    is_valid, error_msg = validate_task_data(title, description)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    # Create task
    task_id = Task.create(title, description, current_user['user_id'])
    
    return jsonify({
        'message': 'Task created successfully',
        'task_id': task_id
    }), 201

@tasks_bp.route('', methods=['GET'])
@token_required
def get_tasks(current_user):
    # Admin can see all tasks, users see only their own
    if current_user['role'] == 'admin':
        tasks = Task.get_all()
    else:
        tasks = Task.get_by_user(current_user['user_id'])
    
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'id': task['id'],
            'title': task['title'],
            'description': task['description'],
            'user_id': task['user_id']
        })
    
    return jsonify({'tasks': tasks_list}), 200

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    task = Task.get_by_id(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Check ownership (admin can edit any task)
    if current_user['role'] != 'admin' and task['user_id'] != current_user['user_id']:
        return jsonify({'error': 'You cannot modify this task'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    title = data.get('title', task['title'])
    description = data.get('description', task['description'])
    
    # Validate
    is_valid, error_msg = validate_task_data(title, description)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    Task.update(task_id, title, description)
    
    return jsonify({'message': 'Task updated successfully'}), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    task = Task.get_by_id(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Check ownership (admin can delete any task)
    if current_user['role'] != 'admin' and task['user_id'] != current_user['user_id']:
        return jsonify({'error': 'You cannot delete this task'}), 403
    
    Task.delete(task_id)
    
    return jsonify({'message': 'Task deleted successfully'}), 200