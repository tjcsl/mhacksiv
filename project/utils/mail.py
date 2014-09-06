import sendgrid
import os

sgclient = sendgrid.SendGridClient(os.getenv('SENDGRID_USERNAME'),
        os.getenv('SENDGRID_PASSWORD'), raise_errors = True)
