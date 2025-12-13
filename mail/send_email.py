import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os

load_dotenv()

def send_email(html_content, subject, recipients, images=[]):
    smtp_host = os.environ['MAIL_SERVER']
    smtp_port = os.environ['MAIL_PORT']
    username = os.environ['ADDRESS']
    password = os.environ['PASSWORD']

    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = ", ".join(recipients)

    part_html = MIMEText(html_content, "html")
    msg.attach(part_html)

    for image_path in images:
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            image_id = image_path.split(".")[0]
            img.add_header('Content-ID', f'<{image_id}>')
            img.add_header('Content-Disposition', 'inline', filename=image_path)
            msg.attach(img)


    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(username, recipients, msg.as_string())
