import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

# Email credentials got in os variables
sender_email = os.environ['sender_email']
password = os.environ['password']

# Variables
receiver_email = variable_to_be_sent
file_path = file_in_google_cloud_storage

# Create the email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "Testing Email"

# Email body
body = "Hello,\n\nPlease sign the contract.\n\nBest regards."
msg.attach(MIMEText(body, 'plain'))

# Attach the PDF
filename = os.path.basename(file_path)

with open(file_path, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode the attachment
encoders.encode_base64(part)
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Attach the file to the message
msg.attach(part)

# Connect to the SMTP server and send the email
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:  # Use the appropriate SMTP server and port
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")