import os

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
        self.raw_client = None
        self.default_bucket = None

    def init_app(self, app):
        self.client = boto3.resource(
            's3',
            endpoint_url=app.config['MINIO_SERVER_URI'],
            aws_access_key_id=app.config['MINIO_ACCESS_KEY'],
            aws_secret_access_key=app.config['MINIO_SECRET_KEY'],
            config=Config(signature_version='s3v4'),
            region_name='us-east-1')
        self.raw_client = boto3.client(
            's3',
            endpoint_url=app.config['MINIO_SERVER_URI'],
            aws_access_key_id=app.config['MINIO_ACCESS_KEY'],
            aws_secret_access_key=app.config['MINIO_SECRET_KEY'],
            config=Config(signature_version='s3v4'),
            region_name='us-east-1')
        self.create_default_bucket()
        # The name of the bucket is just the current environment (ie. testing)
        self.default_bucket_name = os.getenv('FLASK_ENV')
        self.default_bucket = self.client.Bucket(self.default_bucket_name)

    def get_link(self, key):
        return self.raw_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': self.default_bucket_name,
                'Key': key
            },
            ExpiresIn=100)

    def create_default_bucket(self):
        try:
            self.client.create_bucket(Bucket=os.getenv('FLASK_ENV'))
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code != 'BucketAlreadyOwnedByYou' and \
                    error_code != 'BucketAlreadyExists':
                raise
        except Exception as e:
            raise Exception('Unexpected Error: %s' % str(e))

    def clear_testing_bucket(self):
        try:
            bucket = self.client.Bucket('testing')
            bucket.delete_objects(Delete={
                'Objects': [{
                    'Key': obj.key
                } for obj in bucket.objects.all()]
            })
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code != 'NoSuchBucket' and error_code != 'NoSuchKey':
                raise
        except Exception as e:
            raise Exception('Unexpected Error: %s' % str(e))

    def get_object_from_key(self, key):
        """
        Fetch an object from the minio server.
        """
        try:
            return self.client.Object(os.getenv('FLASK_ENV'), key)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                raise Exception('Cannot find bucket named %s' %
                                self.default_bucket_name)

            elif error_code == 'NoSuchKey':
                raise Exception('Cannot find object with key %s\n' % key)
            else:
                raise Exception('Unknown client error %s' % error_code)

    def get_object_body(self, obj):
        """
        Convert an object to a string.
        """
        return obj.get()['Body'].read().decode('utf-8')

    def download_file_from_key(self, key, path):
        """
        Download an object into a physical file at the given path on the server
        """
        try:
            with open(path, 'wb') as data:
                self.default_bucket.download_fileobj(key, data)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                raise Exception('Cannot find object with key %s' % key)
            else:
                raise Exception('Unknown client error %s' % error_code)

    def delete_project(self, project):
        """
        Delete a project from the Minio Server.
        """
        if project is None or len(project.commits) == 0:
            return

        objects = [{
            'Key': f'{project.id}/{commit.id}'
            for commit in project.commits
        }]

        self.raw_client.delete_objects(
            Bucket=self.default_bucket_name,
            Delete={
                'Objects': objects,
                'Quiet': True,
            },
        )


fs = Filestore()
