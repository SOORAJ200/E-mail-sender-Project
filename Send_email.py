import smtplib
import argparse
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(sender_email, sender_password, recipient_email, subject, body, attachment=None):
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the body to the email
    msg.attach(MIMEText(body, 'plain'))

    # Check if there's an attachment
    if attachment:
        # Open the file to be sent
        try:
            with open(attachment, "rb") as attachment_file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment_file.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment)}',
                )
                msg.attach(part)
        except Exception as e:
            print(f"Failed to attach file: {str(e)}")
            return

    # Create an SMTP session
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
    finally:
        server.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send email from the command line.')
    parser.add_argument('--sender', required=True, help='Sender email address')
    parser.add_argument('--password', required=True, help='Sender email password')
    parser.add_argument('--recipient', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Subject of the email')
    parser.add_argument('--body', required=True, help='Body of the email')
    parser.add_argument('--attachment', help='Path to an optional attachment')

    args = parser.parse_args()

    send_email(args.sender, args.password, args.recipient, args.subject, args.body, args.attachment)
