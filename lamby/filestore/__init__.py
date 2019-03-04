import os
import sys

import boto3

from botocore.client import Config
from botocore.exceptions import ClientError

"""
###########
Boto3 Notes
###########

Exception Error Codes
---------------------
BucketAlreadyExists
BucketAlreadyOwnedByYou
NoSuchBucket
NoSuchKey
NoSuchUpload
ObjectAlreadyInActiveTierError
ObjectNotInActiveTierError
"""


class Filestore(object):
    def __init__(self):
        self.client = None
        self.default_bucket = None

    def init_app(self, app):
        self.client = boto3.resource(
            's3',
            endpoint_url=app.config['MINIO_SERVER_URI'],
            aws_access_key_id=app.config['MINIO_ACCESS_KEY'],
            aws_secret_access_key=app.config['MINIO_SECRET_KEY'],
            config=Config(signature_version='s3v4'),
            region_name='us-east-1'
        )
        self.create_default_bucket()
        self.default_bucket = self.client.Bucket(os.getenv('FLASK_ENV'))

    def create_default_bucket(self):
        try:
            self.client.create_bucket(Bucket=os.getenv('FLASK_ENV'))
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'BucketAlreadyOwnedByYou' or \
                    error_code == 'BucketAlreadyExists':
                pass
        except Exception as e:
            sys.stderr.write('Unexpected Error: %s' % str(e))
            exit(2)

    def clear_testing_bucket(self):
        try:
            bucket = self.client.Bucket('testing')
            bucket.delete_objects(Delete={
                'Objects': [{'Key': obj.key} for obj in bucket.objects.all()]
            })
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket' or error_code == 'NoSuchKey':
                pass
        except Exception as e:
            sys.stderr.write('Unexpected Error: %s' % str(e))
            exit(2)


fs = Filestore()
