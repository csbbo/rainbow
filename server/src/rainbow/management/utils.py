import logging
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from utils.constans import ConfigEnum
from utils.shortcuts import get_config

logger = logging.getLogger(__name__)


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(to_list, subject, html):
    config = get_config()
    msg = MIMEText(html, 'html', 'utf-8')
    msg['From'] = _format_addr('Magic Style <%s>' % config.get(ConfigEnum.EMAIL_ADDR))  # who i am
    msg['To'] = ';'.join([_format_addr('你好! <%s>' % addr) for addr in to_list])     # recipients
    msg['Subject'] = Header(subject, 'utf-8').encode()

    try:
        server = smtplib.SMTP(config.get(ConfigEnum.EMAIL_SMTP_SERVER), config.get(ConfigEnum.EMAIL_PORT))
        server.starttls()
        # server.set_debuglevel(1)
        server.login(config.get(ConfigEnum.EMAIL_ADDR), config.get(ConfigEnum.EMAIL_PASSWORD))
        r = server.sendmail(config.get(ConfigEnum.EMAIL_ADDR), to_list, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        logger.error(str(e))
        return False


def send_email_captcha(email_addr, captcha):
    to_list = [email_addr, ]
    subject = 'send captcha'
    html = f'you captcha is {captcha}'
    return send_email(to_list, subject, html)
