import uuid
import boto3

def create_bucket(name, region, bucket_config):
    if region is None or name is None:
        raise Exception('incorrect params')

    s3_client = boto3.client('s3', region_name=region)
    bucket_config['LocationConstraint'] = region
    print(bucket_config)
    s3_client.create_bucket(
        Bucket=name, CreateBucketConfiguration=bucket_config)

def upload_data(key, bucket):
    f = open('data/test.txt', 'rb') 
    bucket.upload_fileobj(f, key)

def transfer_data(src_bucket_name, src_key, dst_bucket, dst_key):
    # for reference on AWS data transfer: https://aws.amazon.com/blogs/architecture/overview-of-data-transfer-costs-for-common-architectures/
    dst_bucket.copy(
        {
            'Bucket': src_bucket_name, 
            'Key': src_key
        },
        dst_key
    )
    
if __name__ == '__main__':
    # initial constants
    src_bucket_name = 'cs243-src-bucket-{}'.format(uuid.uuid4())
    dst_bucket_name = 'cs243-dst-bucket-{}'.format(uuid.uuid4())
    src_key = 'cs243-src-key-{}'.format(uuid.uuid4())
    dst_key = 'cs243-dst-key-{}'.format(uuid.uuid4())
    source_region = 'us-west-2'
    destination_region = 'eu-west-1'

    # determined by the destination region
    # for pricing, reference: https://aws.amazon.com/s3/pricing/?p=pm&c=s3&z=4
    perGBtransfercost = 0.02

    # list buckets
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()
    print(response)

    # create bucket in source region
    create_bucket(name=src_bucket_name, region=source_region, bucket_config={})
    src_bucket = s3.Bucket(src_bucket_name)

    # upload to source bucket (ingress)
    upload_data(src_key, src_bucket)

    # create bucket in destination region
    create_bucket(name=dst_bucket_name, region=destination_region, bucket_config={})
    dst_bucket = s3.Bucket(dst_bucket_name)
    
    # transfer to destination bucket (egress)
    transfer_data(src_bucket_name, src_key, dst_bucket, dst_key)