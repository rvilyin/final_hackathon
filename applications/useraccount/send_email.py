from django.core.mail import send_mail


def send_activation_code(email, code):
    send_mail(
        'Asiastream activation code',
        f'http://localhost:8000/api/v1/useraccount/activate/{code}/',
        'baitikovskij@gmail.com',
        [email]
    )


def send_reset_code(email, code):
    send_mail(
        'Asiastream reset code',
        f'http://localhost:8000/api/v1/useraccount/reset/{code}/',
        'baitikovskij@gmail.com',
        [email]
    )