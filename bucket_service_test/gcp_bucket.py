import uuid
from google.cloud import storage

def create_bucket(storage_client, bucket_name, region):
    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = 'COLDLINE'
    new_bucket = storage_client.create_bucket(bucket, location=region)
    print(
        'Created bucket {} in {} with storage class {}'.format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket

def upload_data(key, bucket):
    source_file_name = 'data/test.txt'
    blob = bucket.blob(key)
    blob.upload_from_filename(source_file_name)
    print(
        f"File {source_file_name} uploaded to {key}."
    )

def transfer_data(src_blob_name, src_bucket, dst_blob_name, dst_bucket):
    source_blob = src_bucket.blob(src_blob_name)
    blob_copy = src_bucket.copy_blob(
        source_blob, dst_bucket, dst_blob_name
    )
    print(
        "Blob {} in bucket {} copied to blob {} in bucket {}.".format(
            source_blob.name,
            src_bucket.name,
            blob_copy.name,
            dst_bucket.name,
        )
    )

if __name__ == '__main__':
    project_name = 'grounded-datum-367811'

    src_bucket_name = 'cs243-src-bucket-{}'.format(uuid.uuid4())
    dst_bucket_name = 'cs243-dst-bucket-{}'.format(uuid.uuid4())
    src_key = 'cs243-src-key-{}'.format(uuid.uuid4())
    dst_key = 'cs243-dst-key-{}'.format(uuid.uuid4())
    source_region = 'US-WEST1'
    destination_region = 'EUROPE-WEST2'

    # determined by the source and destination region
    # for pricing, reference: https://cloud.google.com/storage/pricing#operations-pricing
    perGBtransfercost = 0.05

    # init client
    storage_client = storage.Client(project=project_name)

    # list buckets
    buckets = storage_client.list_buckets()
    print("Listing existing buckets:")
    for bucket in buckets:
        print(bucket.name)

    # create src and dst buckets
    src_bucket = create_bucket(storage_client, src_bucket_name, source_region)
    dst_bucket = create_bucket(storage_client, dst_bucket_name, destination_region)

    # upload to source bucket (ingress)
    upload_data(src_key, src_bucket)

    # transfer to destination bucket (egress)
    transfer_data(src_key, src_bucket, dst_key, dst_bucket)