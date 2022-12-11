import io
import uuid
import boto3
from google.cloud import storage

# internal imports
import aws_bucket
import gcp_bucket

def transfer_from_S3_to_GCP(s3_client, s3_bucket, gc_bucket, src_key, dst_key):
    # download from aws
    data_stream = io.BytesIO()
    s3_client.download_fileobj(
        Bucket=s3_bucket,
        Key=src_key,
        Fileobj=data_stream
    )

    # upload blob to gc
    blob = gc_bucket.blob(dst_key)
    blob.upload_from_file(data_stream, rewind=True)

def transfer_from_GCP_to_S3(s3, s3_bucket_name, gc_bucket, src_key, dst_key):
    # download from gc
    data_stream = io.BytesIO()
    blob = gc_bucket.blob(src_key)
    blob.download_to_file(data_stream)

    # upload to aws
    dst_bucket = s3.Bucket(s3_bucket_name)
    dst_bucket.upload_fileobj(data_stream, dst_key)

def simulate_S3_to_GCP():
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    src_bucket_name = 'cs243-src-bucket-{}'.format(uuid.uuid4())
    dst_bucket_name = 'cs243-dst-bucket-{}'.format(uuid.uuid4())
    src_key = 'cs243-src-key-{}'.format(uuid.uuid4())
    dst_key = 'cs243-dst-key-{}'.format(uuid.uuid4())
    source_region = 'us-west-2'
    destination_region = 'EUROPE-WEST2'

    # create src aws bucket and upload data
    aws_bucket.create_bucket(src_bucket_name, source_region, {})
    src_bucket = s3.Bucket(src_bucket_name)
    aws_bucket.upload_data(src_key, src_bucket)
    
    # create dst gcp bucket and perform transfer
    storage_client = storage.Client(project='grounded-datum-367811')
    gc_bucket = gcp_bucket.create_bucket(storage_client, dst_bucket_name, destination_region)
    transfer_from_S3_to_GCP(s3_client, src_bucket_name, gc_bucket, src_key, dst_key)


def simulate_GCP_to_S3():
    s3 = boto3.resource('s3')
    src_bucket_name = 'cs243-src-bucket-{}'.format(uuid.uuid4())
    dst_bucket_name = 'cs243-dst-bucket-{}'.format(uuid.uuid4())
    src_key = 'cs243-src-key-{}'.format(uuid.uuid4())
    dst_key = 'cs243-dst-key-{}'.format(uuid.uuid4())
    source_region = 'US-WEST1'
    destination_region = 'eu-west-1'

    # create src gcp bucket and upload data
    storage_client = storage.Client(project='grounded-datum-367811')
    src_bucket = gcp_bucket.create_bucket(storage_client, src_bucket_name, source_region)
    gcp_bucket.upload_data(src_key, src_bucket)

    # create dst aws bucket and perform transfer
    aws_bucket.create_bucket(dst_bucket_name, destination_region, {})
    transfer_from_GCP_to_S3(s3, dst_bucket_name, src_bucket, src_key, dst_key)

if __name__ == '__main__':
    simulate_S3_to_GCP()
    simulate_GCP_to_S3()
    