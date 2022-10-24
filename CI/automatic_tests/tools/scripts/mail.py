from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ansi2html import Ansi2HTMLConverter
import smtplib
import time


def send_mail(message):
    text= "GET STARTED"
    server = smtplib.SMTP('localhost')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"[PF Robot] Test result : {text}"
    # ???? BAD ??? msg['From'] = formataddr(('Luos PF Robot', 'pf.qa@luos.io'))
    msg['From'] = formataddr(('Luos PF Robot', 'robot.qa@luos.io'))
    msg['To'] = formataddr(('Luos Team', 'robot.qa@luos.io'))

    html = f"""\
    <html>
      <head></head>
      <body>
        <p>{message}</p>
      </body>
    </html>
    """
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1) # text must be the first one
    msg.attach(part2) # html must be the last one
    server.sendmail("pf.qa@luos.io", ['jerome.galan@luos.io'], msg.as_string())
    ###

    server.quit()



resultFile="/home/luos_adm/Luos_tests/Docker/Quality_assurance/CI/automatic_tests/tools/Results/test_result.log"
conv = Ansi2HTMLConverter()
text_file = open(resultFile, "r")
html=""
result = text_file.read()
text_file.close()
ansi = "".join(result)
html += conv.convert(result)
send_mail(html)
