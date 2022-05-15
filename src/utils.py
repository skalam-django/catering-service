from django.template.loader import get_template
from django.http import FileResponse
import pdfkit
import datetime
from random import randint

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ntpath

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    now = datetime.datetime.now()
    context_dict.update({'timestamp' : now.strftime('%d-%m-%Y %H:%M:%S')})
    html  = template.render(context_dict)
    pdf = pdfkit.from_string(html, 'media/outfile.pdf', options={     
                                                                    'page-size': 'A4',
                                                                    'margin-top': '0.75in',
                                                                    'margin-right': '0.75in',
                                                                    'margin-bottom': '0.75in',
                                                                    'margin-left': '0.75in', 
                                                                    'disable-smart-shrinking': ''
                                                                }
                            )
    if pdf:
        return FileResponse(open('media/outfile.pdf', 'rb'), as_attachment=True, filename=f"{context_dict.get('filename')}.{now.strftime('%d-%m-%y')}.pdf") 


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)



def send_email(sender_email, password, receiver_email, attachments, subject="Menu PDF | Niraj Caterer", body="Please find the attached files for menu.", sender_name="Niraj Caterer", receiver_name=None):
    print(sender_email, password, receiver_email, attachments, subject, body, sender_name, receiver_name)
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        html = f"""\
        <html>
          <body>
            <p>Hi{' <strong>'+receiver_name+'</strong>,' if receiver_name else ','}<br>
               <br>
               {body}
            </p>
            <p>Thanks & Regards,</p>
            <p><strong>{sender_name}</strong></p>
          </body>
        </html>
        """

        message.attach(MIMEText(html, "html"))

        for attachment in attachments:
            part = None
            with open(attachment, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            if part:
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {ntpath.basename(attachment)}",
                )
                message.attach(part)

        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        return True    
    except Exception as e:
        print("send_email Error: ", e)
        return False        
