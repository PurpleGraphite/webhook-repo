

from flask import Blueprint, json, jsonify, request
from app.utils.convertTimestampToUTC import convertTimestampToUTC
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

def create_and_insert_event(event_data):
    # Common insertion to avoid repetition across event types
    try:
        result = mongo.db.github_events.insert_one(event_data)
        return {'status': 'success', 'inserted_id': str(result.inserted_id)}, 200
    except Exception as e:
        return {'error': 'Database insertion failed'}, 500

def process_push_event(data):
    # Push events have consistent structure, extract required fields
    try:
        event = {
            'request_id': str(data['after']),
            'author': data['sender']['login'],
            'action': 'PUSH',
            'from_branch': None,
            'to_branch': data['ref'].split('/')[2],  # Extract branch name from refs/heads/branch_name
            'timestamp': convertTimestampToUTC(data['head_commit']['timestamp'])
        }
        return create_and_insert_event(event)
    except (KeyError, IndexError) as e:
        return {'error': 'Invalid push event payload'}, 400

def process_pull_request_event(data):
    # Pull requests can be opened, closed, or merged - handle different states
    try:
        action = data['action']
        pull_request = data['pull_request']
        is_merged = pull_request['merged']
        
        # Skip closed PRs that weren't merged
        if action != 'opened' and not is_merged:
            return {'status': 'ignored', 'message': 'Closed pull request without merge'}, 200
        
        # Extract common fields for both merged and opened PRs
        request_id = str(pull_request['id'])
        from_branch = pull_request['head']['ref']
        to_branch = pull_request['base']['ref']
        
        # Merged vs opened PRs have different data sources
        if is_merged:
            event = {
                'request_id': request_id,
                'author': pull_request['merged_by']['login'],
                'action': 'MERGE',
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': convertTimestampToUTC(pull_request['merged_at'])
            }
        else:
            event = {
                'request_id': request_id,
                'author': pull_request['user']['login'],
                'action': 'PULL_REQUEST',
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': convertTimestampToUTC(pull_request['created_at'])
            }
        
        return create_and_insert_event(event)
    except (KeyError, IndexError) as e:
        return {'error': 'Invalid pull request event payload'}, 400

def validate_webhook_request():
    # Validate incoming request has required headers and JSON data
    if not request.is_json:
        return {'error': 'Content-Type must be application/json'}, 400
    
    event_type = request.headers.get('X-Github-Event')
    if not event_type:
        return {'error': 'Missing X-Github-Event header'}, 400
    
    data = request.get_json()
    if not data:
        return {'error': 'Empty request body'}, 400
    
    # No error, validation passed
    return None 

@webhook.route('/receiver', methods=["POST"])
def receiver():
    # Main webhook receiver - validate request then route to appropriate handler
    validation_error = validate_webhook_request()
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]
    
    # Extract validated data
    event_type = request.headers.get('X-Github-Event')
    data = request.get_json()
    
    # Route to appropriate handler based on event type
    if event_type == 'push':
        result, status_code = process_push_event(data)
    elif event_type == 'pull_request':
        result, status_code = process_pull_request_event(data)
    else:
        # Handle unsupported event types gracefully
        result = {'message': f'Event type "{event_type}" not supported'}
        status_code = 200
    
    return jsonify(result), status_code