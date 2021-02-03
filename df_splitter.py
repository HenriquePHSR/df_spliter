import os
import pandas as pd
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

pd.set_option('display.max_columns', 0)
pd.set_option('display.max_rows', 0)


def split_df(args):
    fname = args[0]
    try:
        df = pd.read_excel(fname)
        # E-mail/CPF/Nome/Período do Curso
        features_list = ['E-Mail', 'CPF', 'Nome']
        print('')
        print('file to split: ' + fname.split('/')[-1])
        if "Curso" in df.columns:
            print('spliting ...')
            if not os.path.exists('splited_df'):
                os.mkdir('splited_df')
            for Curso in df.Curso.unique():
                df[df['Curso'] == Curso][features_list].to_excel('splited_df/' + Curso + '.xlsx')
                print('file save to: ' + Curso + '.xlsx')
            print(str(len(df.Curso.unique())) + ' file(s) created')
        else:
            print('Coluna Curso nao encontrada')
    except FileNotFoundError:
        print('File not found')
    except:
        print('Something went wrong')


def fill_mail(sender_email, receiver_email, attachment, subject, body):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    file_path = attachment

    if file_path != '':
        filename = file_path.split("/")[-1]
        # open has a binary stream
        with open(file_path, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        # Add attachment to message and convert message to string
        message.attach(part)

    text = message.as_string()
    return text


def dispatch_email_from_df(args):
    fname = args[0]
    print(str(fname.split('/')[-1]) + " selecionado")
    try:
        df = pd.read_excel(fname)
        # henrique_pedro@id.uff.br
        # Log in to server using secure context and send email
        username = str(input("email: "))
        password = "njmrtbutmennrekn"
        subject = "An email with attachment from Python"
        body = "This is an email with attachment sent from Python"
        # subject = input("assunto: ")
        # body = input("corpo: ")
        #print('select attachment: ')
        #attachment = fd.askopenfilename()
        if len(args) > 1:
            attachment = args[1]
        else:
            attachment = ''
        user = {
            "username": username,
            "pass": password
        }
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            if not is_valid(user["username"]):
                print("Invalid Email")
                raise Exception()
            server.login(user["username"], user['pass'])

            to_send = []
            if 'E-Mail' in df.columns:
                for email in df['E-Mail'].values:
                    if is_valid(email):
                        to_send.append(email)
            else:
                print("email column not found")
                to_send = None
            not_send = []
            for email in to_send:
                try:
                    server.sendmail(user['username'], email,
                                    fill_mail(user['username'], email, attachment, subject, body))
                    print("mail sent to " + email)
                except:
                    print("exception occurred mail to " + email + " not send")
                    not_send.append(email)

    except FileNotFoundError:
        print('File not found')
    except:
        print('Something went wrong')


def is_valid(email):
    if type(email) == str:
        if re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        else:
            return False
    else:
        return False
