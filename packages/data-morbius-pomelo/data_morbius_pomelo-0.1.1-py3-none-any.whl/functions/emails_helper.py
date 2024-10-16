import sys
import base64
import os
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid import SendGridAPIClient
from utilities import aws_helper
from python_http_client.exceptions import HTTPError

SENGRID_API_KEY=aws_helper.get_secrets(
        "arn:aws:secretsmanager:us-east-1:248666061168:secret:use1-infra-data-ofas-bi-job-2l5IHT",
        "us-east-1").get('sengrid_key_bi')

def add_atachment(file,name,list):
    encoded = base64.b64encode(file).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('application/pdf')
    attachment.file_name = FileName(name)
    attachment.disposition = Disposition('attachment')
    attachment.content_id = ContentId('Example Content ID')
    list.append(attachment)

def send_email_with_attach(from_,to_,subject_,html_,list_attachement):
    os.environ["SENDGRID_API_KEY"] = SENGRID_API_KEY
    message = Mail(
        from_email='{}'.format(from_),
        to_emails=to_,
        subject='{}'.format(subject_),
        html_content='{}'.format(html_))
    message.attachment = list_attachement
    sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sendgrid_client.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)


def send_email_no_attach(from_,to_,subject_,html_):
    os.environ["SENDGRID_API_KEY"] = SENGRID_API_KEY
    message = Mail(
        from_email='{}'.format(from_),
        to_emails=to_,
        subject='{}'.format(subject_),
        html_content='{}'.format(html_))
    sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    try:
        response = sendgrid_client.send(message)
    except HTTPError as e:
        print(e.to_dict)
    print(response.status_code)
    print(response.body)
    print(response.headers)


