import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

MAIL_PASSCODE = os.getenv('MAIL_PASSCODE')
MAIL_EMAIL = os.getenv('MAIL_EMAIL')
MAIL_SERVER = os.getenv('MAIL_SERVER')

def mail(email: str, name: str, code: str):
    """
    This function sends an email with a verification code using a pre-defined HTML template.
    :return: A dictionary with the message "Verification code sent to {recipient}" and a status of True
    if the email was sent successfully, or an error message if there was an exception.
    """
    template = """
    <html>
    <head></head>
    <body>
      <img src='https://app.cryptoflixinvest.org/logo.png' align='center' width='100' height='100' />
      <h2>Dear [RECIPIENT_NAME],</h2>
      <p align='center'>Your <a href='cryptoflixinvest.org' style='display: inline'>CRYPTOFLIXINVEST ORG</a> account verification code is <b style='color: black; font-weight: bold;'>[CODE]</b></p>
      <p>Regards,<br>
         [SENDER_NAME]</p>
    </body>
    </html>
    """
    
    sender = MAIL_EMAIL
    password = MAIL_PASSCODE
    recipient = email
    subject = 'Verification Code'

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject

    template = template.replace('[RECIPIENT_NAME]', name)
    template = template.replace('[SENDER_NAME]', 'CRYPTOFLIXINVEST ORG')
    template = template.replace('[CODE]', code)

    message.attach(MIMEText(template, 'html'))

    try:
        server = smtplib.SMTP(MAIL_SERVER, 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(message)
        server.quit()
        return dict(message=f'Verification code sent to {recipient}', status=True)
    except Exception as e:
        return dict(message=f'An error occurred while sending the email: {str(e)}', status=False)
