from django.core.mail import send_mail


def send_activation_code(email, code):
    send_mail(
        'Asiastream activation code',
        f'https://asiastream.space/api/v1/account/activate/{code}/',
        'totalroma@gmail.com',
        [email]
    )


def send_reset_code(email, code):
    send_mail(
        'Asiastream reset code',
        f'https://asiastream.space/api/v1/account/reset/{code}/',
        'totalroma@gmail.com',
        [email]
    )


def send_notify_message(email, streamer, user):
    send_mail(
        'AsiaStream',
        f'Dear {user}, {streamer}',
        'totalroma@gmail.com',
        [email]
    )