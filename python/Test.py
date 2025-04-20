from email_notification import send_mail

reciever_id = []  # add a list of IDs to queried from database
subject = "Test Email"
body = "This is a test email"
send_mail(reciever_id, subject, body)
