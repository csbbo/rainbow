import dramatiq

from management.utils import send_email_captcha


@dramatiq.actor(max_retries=10)
def send_email_captcha_task(email_addr, captcha):
    send_email_captcha(email_addr, captcha)
