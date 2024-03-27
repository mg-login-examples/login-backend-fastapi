import smtplib
from email.message import EmailMessage


def send_email(to, subject, message):

    app_email_address = "mgautoemails@gmail.com"
    app_email_password = "ybddxyueijfkscku"

    # create email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = app_email_address
    msg['To'] = to
    msg.set_content(message)

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(app_email_address, app_email_password)
        smtp.send_message(msg)
