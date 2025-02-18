from google.cloud import storage
from connection.secrets import settings


def load_archive_storage(file, destiny,receiver_email):

    client = storage.Client.from_service_account_json(settings.GOOGLE_APPLICATION_CREDENTIALS)
    bucket_name = settings.bucket_name
    file_path = file
    blob_name = destiny

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Upload file
    blob.upload_from_filename(file_path)

    metadata = {"receiver_email": receiver_email}  # Create the metadata dictionary
    blob.metadata = metadata  # Set the metadata
    blob.update() #Important: you have to update the blob for the metadata to be saved

    return 
