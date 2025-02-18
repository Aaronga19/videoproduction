import functions_framework
from google.cloud import storage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
import logging
# ... (rest of the email sending code is the same as the previous response)
# Email credentials got in os variables


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def send_email_on_gcs_upload(cloud_event):
    """Cloud Function triggered by GCS object creation/upload."""
    logging.info(cloud_event)

    data = cloud_event.data
    logging.info(data['bucket'])
    logging.info(data['name'])
    file_path = f"gs://{data['bucket']}/{data['name']}" # Construct the file path
    print(f"File uploaded: {file_path}") # Log the uploaded file

    # Extract receiver email from file metadata
    try:
      receiver_email = blob_metadata_email(data['bucket'],data['name']) # Get from file metadata

      if not receiver_email:
          raise ValueError("Receiver email not found in file metadata.")


      # Call your existing email function
      send_email_with_gcs_attachment_gcs_trigger(file_path, receiver_email) # Pass receiver_email to the function
      print("Email sending triggered.")
    except Exception as e:
      print(f"Error processing upload: {e}")
      return f"Error processing upload: {e}", 500


def send_email_with_gcs_attachment_gcs_trigger(file_path:str, receiver_email:str): #Modified to receive receiver_email
    """Cloud Function to send email with attachment from GCS."""

    try:
        # Extract bucket and blob name from the GCS file path
        try:
            gcs_uri_parts = file_path.replace("gs://", "").split("/", 1)
            bucket_name = gcs_uri_parts[0]
            blob_name = gcs_uri_parts[1]
        except IndexError:
            return 'Error: Invalid file_path format.  Should be gs://bucket/path', 400

        # Download file from GCS to in-memory buffer
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # In-memory file-like object
        from io import BytesIO
        file_content = BytesIO()
        blob.download_to_file(file_content)
        file_content.seek(0)  # Reset stream position to the beginning

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = os.environ.get('SENDER_EMAIL')
        msg['To'] = receiver_email  # Use the receiver_email from metadata
        msg['Subject'] = "Contract Signing Request" # More descriptive subject

        # Email body
        body = "Hello,\n\nPlease sign the attached contract.\n\nBest regards."
        msg.attach(MIMEText(body, 'plain'))

        # Attach the PDF from memory
        filename = blob_name.split("/")[-1] # Extract filename from blob path
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file_content.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")
        msg.attach(part)

        # Connect to the SMTP server and send the email (using Gmail's SSL port)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.environ.get('SENDER_EMAIL'), os.environ.get('PASSWORD'))
            server.sendmail(os.environ.get('SENDER_EMAIL'), receiver_email, msg.as_string())
        print('Email sent successfully!')
        return 200

    except Exception as e:
        print(f"Failed to send email: {e}")  # Log the error for debugging
        return f"Failed to send email: {e}", 500  # Internal Server Error
    
def blob_metadata_email(bucket_name:str, blob_name:str) -> str:
    """Get out a blob's metadata."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.get_blob(blob_name)

    print(f"Metadata: {blob.metadata.get("receiver_email")}")
    
    return blob.metadata.get("receiver_email")