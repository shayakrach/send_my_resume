import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from getpass import getpass

NUM_OF_TRIES = 2


def send_mail(my_email, my_pass, addressee_email, text):
    # The domain name of gmail server
    host = 'smtp.gmail.com'
    port = 587
    # log in to server and send email
    conn = smtplib.SMTP(host, port)
    conn.ehlo()
    conn.starttls()
    for i in range(NUM_OF_TRIES):
        try:
            conn.login(my_email, my_pass)
            conn.sendmail(my_email, addressee_email, text)
            conn.quit()
            print('Your resume sent to {}'.format(addressee_name))
            return
        except:
            print('Password Incorrect')
            # print(my_pass)
            my_pass = getpass('Password: ')
    print('Remember the password and then come back')


# my_email  == my email address
my_email = 'shayakrach@gmail.com'
print('email: {}'.format(my_email))
# You can enter your password in privacy every time or change it to a const variable
my_pass = getpass('Password: ')
# Change it to your name
my_name = 'Shay Rachmany'

addressee_name = input("Addressee first name: ")
addressee_email = input("Addressee email: ")

subject = "CV - {}".format(my_name)
body = """
Dear {},

I’ve attached my resume to this email so you can
take a closer look at my qualifications. Please feel
free to reply at your convenience.

Sincerely,

{}

""".format(addressee_name, my_name)

# Create the container (outer) email message.
msg = MIMEMultipart()
# Create the base text message.
msg['From'] = my_email
msg['To'] = addressee_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Set the resume file path
file_path = r'C:\Users\shayr\Documents\CV\ShayRachmanyCV.pdf'

attachment = open(file_path, 'rb')
part = MIMEBase('application', 'ostet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)

# Set resume file name
filename = 'ShayRachmanyCV.pdf'
# Set the filename parameter
part.add_header('Content-Disposition', "attachment; filename= " + filename)

msg.attach(part)
text = msg.as_string()

# Use the send_mail function
send_mail(my_email, my_pass, addressee_email, text)
