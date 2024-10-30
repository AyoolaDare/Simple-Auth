import json
import boto3
from botocore.exceptions import ClientError

# Utility functions
def create_response(status_code, body):
    """Create standardized API response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }

def validate_user_data(user_data):
    """Validate required user fields"""
    required_fields = ['username', 'email', 'password']
    return all(field in user_data for field in required_fields)

def parse_body(body):
    """Safely parse JSON body"""
    try:
        return json.loads(body)
    except (TypeError, json.JSONDecodeError) as e:
        print(f"Error parsing JSON body: {e}")
        return None

# Database operations class
class DynamoDBOperations:
    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)
    
    def get_user(self, username):
        """Retrieve user from DynamoDB"""
        try:
            response = self.table.get_item(Key={'username': username})
            return response.get('Item')
        except ClientError as e:
            print(f"DynamoDB ClientError in get_user: {e}")
            raise
    
    def register_user(self, user_data):
        """Register new user in DynamoDB"""
        try:
            # Ensure only validated fields are stored
            clean_user_data = {
                'username': user_data['username'],
                'email': user_data['email'],
                'password': user_data['password']  # In production, this should be hashed
            }
            self.table.put_item(
                Item=clean_user_data,
                ConditionExpression='attribute_not_exists(username)'
            )
        except ClientError as e:
            print(f"DynamoDB ClientError in register_user: {e}")
            raise

# Initialize database operations
db = DynamoDBOperations('Users')

# Handler functions
def handle_register(event):
    """Handle user registration"""
    body = parse_body(event.get('body'))
    if not body:
        return create_response(400, 'Invalid JSON in request body')
    
    if not validate_user_data(body):
        return create_response(400, 'Missing required fields: username, email, password')
    
    try:
        db.register_user(body)
        print("User registered:", body['username'])
        return create_response(201, {'message': 'User registered successfully'})
    except ClientError as e:
        print(f"DynamoDB ClientError in register: {e}")
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return create_response(400, {'error': 'Username already exists'})
        return create_response(500, {'error': 'Internal Server Error'})
    except Exception as e:
        print(f"Unexpected error in register: {e}")
        return create_response(500, {'error': 'Internal Server Error'})

def handle_login(event):
    """Handle user login"""
    body = parse_body(event.get('body'))
    if not body:
        return create_response(400, {'error': 'Invalid JSON in request body'})
    
    if 'username' not in body or 'password' not in body:
        return create_response(400, {'error': 'Missing username or password'})
    
    try:
        user = db.get_user(body['username'])
        if user and user['password'] == body['password']:
            print("Login successful for user:", body['username'])
            return create_response(200, {'message': 'Login successful'})
        print("Invalid login attempt for user:", body['username'])
        return create_response(401, {'error': 'Invalid credentials'})
    except Exception as e:
        print(f"Unexpected error in login: {e}")
        return create_response(500, {'error': 'Internal Server Error'})

def handle_dashboard(event):
    """Handle dashboard data retrieval"""
    query_params = event.get('queryStringParameters', {})
    if not query_params or 'username' not in query_params:
        return create_response(400, {'error': 'Missing username parameter'})
    
    try:
        user = db.get_user(query_params['username'])
        if user:
            print("Dashboard access for user:", query_params['username'])
            return create_response(200, {
                'username': user['username'],
                'email': user['email']
            })
        print("User not found:", query_params['username'])
        return create_response(404, {'error': 'User not found'})
    except Exception as e:
        print(f"Unexpected error in dashboard: {e}")
        return create_response(500, {'error': 'Internal Server Error'})

def lambda_handler(event, context):
    """Main Lambda handler that routes requests to appropriate handlers"""
    try:
        print("Received event:", json.dumps(event))  # Log the incoming event
        
        http_method = event.get('httpMethod')
        path = event.get('path')
        
        # Route the request to the appropriate handler
        if http_method == 'POST' and path == '/register':
            return handle_register(event)
        elif http_method == 'POST' and path == '/login':
            return handle_login(event)
        elif http_method == 'GET' and path == '/dashboard':
            return handle_dashboard(event)
        else:
            return create_response(404, {'error': 'Not Found'})
                
    except Exception as e:
        print(f"Unexpected error in lambda_handler: {e}")
        return create_response(500, {'error': 'Internal Server Error'})