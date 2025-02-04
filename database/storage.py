from google.cloud import storage
from connection.secrets import settings


def load_archive_storage(file, destiny):

    client = storage.Client.from_service_account_json(settings.GOOGLE_APPLICATION_CREDENTIALS)
    bucket_name = 'videoprod_customers'
    file_path = file
    blob_name = destiny

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Upload file
    blob.upload_from_filename(file_path)

    return 
