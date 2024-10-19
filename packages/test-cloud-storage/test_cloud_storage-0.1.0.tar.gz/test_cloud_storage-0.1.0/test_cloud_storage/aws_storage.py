class AWSStorage:
    def __init__(self):
        print("Initialized AWS Storage Service")

    def get_document_details(self, bucket_name, prefix='', file_type=None):
        print(f"Fetching document details from AWS S3: bucket={bucket_name}, prefix={prefix}, file_type={file_type}")
