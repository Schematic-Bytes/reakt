import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

otp_mail_content = """Hello,
The OTP to verify your email address is given below.

{}

If you didn't ask to verify your email address, you can
ignore this email.

Thanks,

Reakt team
"""


reset_mail_content = """Hello,
Your password of your reakt account is given below.
please delete this mail after copying the password.

{}

If you didn't ask to reset your password, you can
ignore this email.

Thanks,

Reakt team
"""


# The mail addresses and password
sender_address = "reaktmail@gmail.com"
sender_pass = ""


def send_otp(receiver_address: str, otp: str) -> bool:
    # Setup the MIME
    try:
        message = MIMEMultipart()
        message["From"] = sender_address
        message["To"] = receiver_address
        message["Subject"] = "Verify your email address for Reakt"

        message.attach(MIMEText(otp_mail_content.format(otp), "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as session:
            session.starttls()
            session.login(sender_address, sender_pass)
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
        print(f"mail send for address {receiver_address} with otp :- {otp}")
        return True
    except Exception as e:
        print(
            "Exception occured while sending mail "
            f"to {receiver_address} with otp :- {otp}\n{e}"
        )
        return False


def send_reset_password(receiver_address: str, password: str) -> bool:
    # Setup the MIME
    try:
        message = MIMEMultipart()
        message["From"] = sender_address
        message["To"] = receiver_address
        message["Subject"] = "Password for your email address"

        message.attach(MIMEText(reset_mail_content.format(password), "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as session:
            session.starttls()
            session.login(sender_address, sender_pass)
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
        print(f"mail send for address {receiver_address} with password  :- {password}")
        return True
    except Exception as e:
        print(
            "Exception occured while sending mail "
            f"to {receiver_address} with password :- {password}\n{e}"
        )
        return False
