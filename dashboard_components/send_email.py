import ssl
import smtplib

creds = {l.split('=')[0].strip():l.split('=')[1].strip() for l in open('dashboard_components/credentials/teg_gmail.txt','r').readlines()}
port = 465  # For SSL
sender_email = creds['EMAIL']
receiver_email = 'dahlia.dry24@gmail.com'
message= """Subject: testing

hello :) """

def send_email(receiver_emails, message):
    """This function sends an automated email from the account teg.dashboard@gmail.com
    receiver_emails: list of recipieints
    message: email content. First line should contain Subject: [subject]."""
    # Create a secure SSL context
    context = ssl.create_default_context()       
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(creds['EMAIL'], creds['PASSWORD'])
            for recipient in receiver_emails:
                server.sendmail(sender_email, recipient, message)
            server.quit()
        return 'success'
    except Exception as e:
        return f'email send failed with message {e}'