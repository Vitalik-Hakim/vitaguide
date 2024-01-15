import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_email(to_email, subject, message):
    # Your email and password for the sender's email account
    sender_email = ""
    sender_password = ""

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = f" Hakim from VitaGuide {sender_email}"
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, "plain"))

    # Establish a connection to the SMTP server (Gmail in this example)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    # Log in to the sender's email account
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, to_email, msg.as_string())

    # Quit the server
    server.quit()

# to_email = "vitalikhakim@gmail.com"
# subject = "Test email"
# message = "This is a test email from Python."
# send_email(to_email, subject, message)
