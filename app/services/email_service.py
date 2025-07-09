from flask_mail import Message
from app import mail

def send_email(email: str, status: str) -> bool:
    try:
        message = "Sorry you have been rejected by Organization to use Account. "

        if status == 'approve':
            message = "Congratulations you have been approved to use account. Thanks for joining PRIME. "
        msg = Message(
            subject='PRIME Researcher Account Status',
            recipients=[email],
            body=message
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False