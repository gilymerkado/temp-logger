#!usr/bin/python3

# Send email with gmail smtp server.
# should change setting in google to allow less secure apps.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmailAlert(logger, temp):
	"""Send an email message with the current temperature.
	The body of the mail contains the logger number that generated the 
	alert and the current temperature."""
	
	logger = str(logger)
	temp = str(temp)
	
	sender = 'bguforams@gmail.com'
	gmail_pwd = 'forams1234'
	
	receivers = 'gilymerkado@gmail.com'
	
	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Temperature alert'
	msg['From'] = sender
	msg['To'] = receivers
	
	# Body of the message
	text="Hi!\nIt looks like there's a problem with the temperature.\n"
	html="""\
	<html>
		<head></head>
		<body>
		<p>Hi!<br />
			Logger {0} currently feels a temperature of {1}.
		</p>
		</body>
	</html>
	""".format(logger, temp)
	
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
	server.ehlo()
	server.starttls()
	server.login(sender, gmail_pwd)
	server.sendmail(sender, [receivers], msg.as_string())
	server.quit()
	
