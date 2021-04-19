import smtplib
from email.message import EmailMessage


def send_mail(name, email):
    message = "Thank you" + " " + name + " " + "for registration"
    msg = EmailMessage()
    msg['Subject'] = 'Registration'
    msg['From'] = 'Trend Follower'
    msg['To'] = email
    msg.set_content(message)   



    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('example@gmail.com', 'password')
        smtp.send_message(msg)
