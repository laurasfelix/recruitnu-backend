#database --> dynamodb
#scraping northwestern's majors page https://catalogs.northwestern.edu/undergraduate/programs-az/
#authentication via jwt_token
#lookup images in google and return company logo
#matching majors to fields automatically
#rates job's compatibility with user based on skills, gpa and major

from flask import Flask, request, jsonify, redirect, url_for, session
import boto3, uuid, requests, jwt, os, logging
from boto3.dynamodb.conditions import Attr
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from flask_cors import CORS
from datetime import datetime, timezone
from functools import wraps
from company_lookup import lookup
from major_match import match
from major_scrape import scrape
from scoring import scoring
from decimal import Decimal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) 
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')
bcrypt = Bcrypt(app)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
table = dynamodb.Table('recruitnu-data')
users = dynamodb.Table('recruitnu-users')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        logger.info(token)
        if not token:
            return jsonify({'error': 'token missing'}), 401
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user_id = decoded_token['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/login', methods=['post'])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({'error': 'missing required fields'}), 400

        response = users.scan(FilterExpression=Attr("email").eq(email))
        if not response['Items']:
            return jsonify({'error': 'user not found'}), 404
        
        user = response['Items'][0]

        if not bcrypt.check_password_hash(user['password'], password):
            return jsonify({'error': 'invalid credentials'}), 401

        token = jwt.encode({
            'user_id': user['user_id'],
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'message': 'login successful', 'token': token}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_user', methods=['post'])
def add_user():
    try:
        data = request.get_json()
        email = data.get("email")
        given_name = data.get("given_name")
        last_name = data.get("last_name")
        phone_number = data.get("phone_number")
        password = data.get("password")
        major = data.get("major")
        year = data.get("year")
        skills = data.get("skills")
        gpa = data.get("gpa")
       
        if not given_name or not email or not last_name or not phone_number or not password:
            return jsonify({'error': 'missing required fields'}), 400
        
        if "@northwestern" not in email and "@u.northwestern" not in email:
            return jsonify({'error': 'non-northwestern email'}), 400
        
        user_id = str(uuid.uuid4())

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        field = match([major])

        users.put_item(
                Item={
                    'user_id': user_id,
                    'given_name': given_name,
                    'last_name': last_name,
                    'phone_number': phone_number,
                    'email': email,
                    'password': hashed_password,
                    'jobs_applied': [],
                    'jobs_created': [],
                    'major': major, 
                    'field': field[major],
                    'year': year, 
                    'gpa': Decimal(str(gpa)), 
                    'skills': skills, 
                }
            )
        
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'message': 'User added successfully', 'token': token,'userId': user_id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/get_user', methods=['get'])
def get_user():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({'error': 'missing required fields'}), 400

        response = users.query(
    KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
)
        
        if 'Items' not in response or len(response['Items']) == 0:
            return jsonify({'error': 'user not found'}), 404
        

        return jsonify({'message': 'User retrieved successfully', 'user': response['Items'][0]}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_job', methods=['post'])  
@token_required
def add_job():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        location = data.get("location")
        job_type = data.get("job_type")
        description = data.get("description")
        company_name = data.get("company_name")
        job_link = data.get("job_link")

        if not description or not location or not job_type or not company_name or not job_link:
            logger.info("error data:", data)
            return jsonify({'error': 'missing required fields'}), 400
        
        job_id = str(uuid.uuid4())

        job_image = lookup(company_name)

        timestamp = datetime.now(timezone.utc).isoformat()

        table.put_item(
                Item={
                    'user_id': user_id,
                    'job_id': job_id,
                    'location': location,
                    'job_type': job_type,
                    'description': description,
                    'company_name': company_name,
                    'timestamp': timestamp,
                    'job_image': job_image,
                    'job_link': job_link,
                    'fields': []
                }
            )
        

        user = users.get_item(Key={'user_id': user_id}).get('Item')

        jobs_created = user.get('jobs_created', [])  
        jobs_created.append(job_id)
        
        users.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET jobs_created = :val",
            ExpressionAttributeValues={':val': jobs_created}
        )
        
        return jsonify({'message': 'job added successfully', 'userId': user_id, 'job_type': job_type}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/apply_job', methods=['post'])  
@token_required
def apply_job():
    try:
        data = request.get_json()
        job_id = data.get('job_id')
        user_id = data.get('user_id')

        if not job_id:
            logger.info("error data:", data)
            return jsonify({'error': 'missing required fields'}), 400

        user = users.get_item(Key={'user_id': user_id}).get('Item')

        jobs_applied = user.get('jobs_applied', [])

        jobs_applied.append(job_id)
        
        users.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET jobs_applied = :val",
            ExpressionAttributeValues={':val': jobs_applied}
        )
        
        return jsonify({'message': 'job applied successfully', 'userId': user_id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_user_jobs', methods=['get'])
@token_required
def get_user_jobs():
    try:
        user_id = request.args.get("user_id") 
        if not user_id:
            return jsonify({'error': 'missing user_id'}), 400

   
        response = users.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id))

        if 'Items' not in response or len(response['Items']) == 0:
            return jsonify({'error': 'No users found'}), 404

        user = response['Items'][0]


        applied_list = user.get('jobs_applied', None)
        created_list = user.get('jobs_created', None)

        applied_jobs_with_scores = []
        for job_id in applied_list:
            job_response = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('job_id').eq(job_id))
            if 'Items' in job_response and len(job_response['Items']) > 0:
                job = job_response['Items'][0]
                score = scoring(user, job['description'])  
                job['compatibility_score'] = score
                applied_jobs_with_scores.append(job)
       
        return jsonify({
            'message': 'User jobs fetched successfully',
            'applied': applied_jobs_with_scores,
            'created': created_list,
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@app.route('/api/get_jobs_field', methods=['get'])
@token_required
def get_user_field():
    try:
        user_id = request.args.get("user_id")
      
        if not user_id:
            return jsonify({'error': 'missing user_id'}), 400

        response = users.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id))

        if 'Items' not in response or len(response['Items']) == 0:
            return jsonify({'error': 'No users found'}), 404

        user = response['Items'][0]

        field = user.get('field', '')

        jobs = table.scan(FilterExpression=Attr("fields").contains(field))['Items']
     
        return jsonify({
            'message': 'Jobs in user s fields fetched successfully',
            'jobs': jobs,
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/major_scrape', methods=['get'])
def scrape_major():
    try:
        majors = scrape()
       
        return jsonify({
            'message': 'majors fetched successfully',
            'majors': majors,
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/user_score', methods=['get'])
def user_score():
    try:
        user_id = request.args.get("user_id") 
        if not user_id:
            return jsonify({'error': 'missing user_id'}), 400

        job_id = request.args.get("job_id") 
        if not job_id:
            return jsonify({'error': 'missing job_id'}), 400
   
        user = users.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id))['Items'][0]
        job = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('job_id').eq(job_id))['Items'][0]

        score = scoring(user, job.get('description'))
       
        return jsonify({
            'message': 'Score created successfully',
            'score': score,
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)