#!usr/bin/python3

# Send email with gmail smtp server.
# should change setting in google to allow less secure apps.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender = 'gilymerkado@gmail.com'
gmail_pwd = 'cdUdji9fgoogle'

receivers = 'gilymerkado@yahoo.com'

msg = MIMEMultipart('alternative')
msg['Subject'] = 'Link'
msg['From'] = sender
msg['To'] = receivers

# Body of the message
text="Hi!\nHow are you ?\nHere is the link you wanted:\nhttp://www.python.org"
html="""\
<html>
	<head></head>
	<body>
	<p>Hi!<br />
		Here is the <a href="https://www.python.org">link</a> you wanted.
	</p>
	</body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'text')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case 
# the HTML message, is best and preffered.
msg.attach(part1)
msg.attach(part2)

# Send the message via gmail smtp server.
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, gmail_pwd)
server.sendmail(sender, [receivers], msg.as_string())
server.quit()
