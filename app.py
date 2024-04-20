from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import os

app = Flask(__name__)

@app.get("/")
def get_home():
    return "Welcome to StepScribe", 200

@app.route('/upload', methods=['POST'])
def upload_file():
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    bucket_name = os.getenv('BUCKET_NAME')


    if 'photo' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        # Upload the file to S3
        s3.upload_fileobj(
            file,
            bucket_name,
            f'photos/{file.filename}'
        )
        # Get the public URL of the uploaded file
        file_url = f'https://{bucket_name}.s3.amazonaws.com/photos/{file.filename}'
        return jsonify({'imageUrl': file_url})

    except ClientError as e:
        print(e)
        return jsonify({'error': 'Upload failed'}), 500

if __name__ == '__main__':
    app.run()
