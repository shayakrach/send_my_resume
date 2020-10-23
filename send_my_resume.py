import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tkinter import *

# Import the variables from setting
from setting import my_email, my_pass, my_name, file_path, filename, my_color

HEIGHT = 270
WIDTH = 550
COLORS = {
    'azure': '#80c1ff',
    'pink': '#C7849E',
    'orange': '#FAD699',
    'purple': '#A5ADD9',
    'blue': '#239ED9',
    'yellow': '#FAEBA7',
    'green': '#008F7E',
    'red': '#DA5552'
}

# Set default color
DEFAULT_COLOR = '#FAEBA7'


def send_resume(addressee_email, addressee_name):
    # if addressee email or name is empty
    if len(addressee_email) == 0:
        message_label['text'] = 'Enter addressee email'
        return
    if len(addressee_name) == 0:
        message_label['text'] = 'Enter addressee name'
        return

    mail_subject = 'CV - {}'.format(my_name)

    body = """
       Dear {},

       I’ve attached my resume to this email so you can
       take a closer look at my qualifications. Please feel
       free to reply at your convenience.

       Sincerely,

       {}

       """.format(addressee_name, my_name)

    # Create the container (outer) mail message.
    msg = MIMEMultipart()
    # Create the base text message.
    msg['From'] = my_email
    msg['To'] = addressee_email
    msg['Subject'] = mail_subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        attachment = open(file_path, 'rb')

        part = MIMEBase('application', 'ostet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)

        # Set the filename parameter
        part.add_header('Content-Disposition', "attachment; filename= " + filename)

        msg.attach(part)
        text = msg.as_string()

        # The domain name of gmail server
        host = 'smtp.gmail.com'
        port = 587

        # log in to server and send email
        conn = smtplib.SMTP(host, port)
        conn.ehlo()
        conn.starttls()
        conn.login(my_email, my_pass)
        conn.sendmail(my_email, addressee_email, text)
        conn.quit()

        # The resume sent successfully
        email_entry.delete(0, len(addressee_email))
        name_entry.delete(0, len(addressee_name))
        message_label['text'] = 'Your resume sent to {}'.format(addressee_name)

    except Exception as e:
        print(type(e).__name__)
        if type(e).__name__ == 'FileNotFoundError':
            message_label['text'] = 'Invalid file'

        elif type(e).__name__ == 'OSError':
            message_label['text'] = 'Invalid file path'

        elif type(e).__name__ == 'SMTPAuthenticationError':
            message_label['text'] = 'Your email or password are Invalid'

        elif type(e).__name__ == 'SMTPRecipientsRefused':
            message_label['text'] = 'Invalid addressee email'

        else:
            message_label['text'] = 'Something went wrong, check in setting.py'


# Set main color
color = DEFAULT_COLOR
if my_color in COLORS.keys():
    color = COLORS[my_color]

root = Tk(className=' {}'.format(my_name))

# Set default size
canvas = Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# Set title
upper_frame = Frame(root, bg=color)
upper_frame.place(relx=0, rely=0, relwidth=1, relheight=0.25)
title_label = Label(upper_frame, bg=color, font=('modern', 30), text="Send My Resume")
title_label.place(relx=0.26, rely=0.2, relwidth=0.5, relheight=1)

# Set email and name entries
label_width = 0.4
label_height = 0.2
label_font = ('arial bold', 17)

entry_width = 0.55
entry_height = 0.2
entry_font = ('arial', 15)

middle_frame = Frame(root, bg=color)
middle_frame.place(relx=0, rely=0.25, relwidth=1, relheight=0.65)

email_label = Label(middle_frame, bg=color, font=label_font, text="addressee email:")
email_label.place(relx=0, rely=0.15, relwidth=label_width, relheight=label_height)
email_entry = Entry(middle_frame, font=entry_font)
email_entry.place(relx=0.4, rely=0.15, relwidth=entry_width, relheight=entry_height)

name_label = Label(middle_frame, bg=color, font=label_font, text="addressee name:")
name_label.place(relx=0, rely=0.4, relwidth=label_width, relheight=label_height)
name_entry = Entry(middle_frame, font=entry_font)
name_entry.place(relx=0.4, rely=0.4, relwidth=entry_width, relheight=entry_height)

# Set send button
button = Button(middle_frame, text="Send", font=('arial', 16),
                command=lambda: send_resume(email_entry.get(), name_entry.get()))
button.place(relx=0.45, rely=0.8, relwidth=0.12, relheight=0.15)

# Set message label for the user
lower_frame = Frame(root, bg=color)
lower_frame.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

message_label = Label(lower_frame, font=('Courier', 14), bg=color)
message_label.place(relx=0, rely=0, relwidth=1, relheight=1)

root.mainloop()
