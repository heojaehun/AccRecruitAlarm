import smtplib
from email.mime.text import MIMEText
import configparser
import os

dir = os.path.dirname(os.path.abspath(__file__)

def send_mail():
	config = configparser.ConfigParser()
	config.read(dir + '/setting.cfg')
	mail_info_section = 'MAIL_INFO'

	sender = config.get(mail_info_section, 'sender')
	receivers = config.get(mail_info_section, 'receivers').split(', ')
	password = config.get(mail_info_section, 'password')
	subject = config.get(mail_info_section, 'subject')
	message = '''국립 아시아 문화전당 채용 게시판에 새 글이 등록 되었습니다.'''

	server = smtplib.SMTP_SSL('smtp.naver.com', 465)
	server.login(sender, password)

	for receiver in receivers:
	    msg = MIMEText(message, _charset='utf8')
	    msg['Subject'] = subject
	    msg['From'] = sender
	    msg['To'] = receiver

	    #server.sendmail(sender, [receiver], body.encode('utf8'))
	    server.sendmail(sender, [receiver], msg.as_string())

	server.quit()

	print('...Mail sended!...')

def send_mail(_message):
	config = configparser.ConfigParser()
	config.read(dir + '/setting.cfg')
	mail_info_section = 'MAIL_INFO'

	sender = config.get(mail_info_section, 'sender')
	receivers = config.get(mail_info_section, 'receivers').split(', ')
	password = config.get(mail_info_section, 'password')
	subject = config.get(mail_info_section, 'subject')
	message = _message

	server = smtplib.SMTP_SSL('smtp.naver.com', 465)
	server.login(sender, password)

	for receiver in receivers:
	    msg = MIMEText(message, _charset='utf8')
	    msg['Subject'] = subject
	    msg['From'] = sender
	    msg['To'] = receiver

	    #server.sendmail(sender, [receiver], body.encode('utf8'))
	    server.sendmail(sender, [receiver], msg.as_string())

	server.quit()

	print('...Mail sended!...')


if __name__ == '__main__':
    send_mail('테스트입니다.')
