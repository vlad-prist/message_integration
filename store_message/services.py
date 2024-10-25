from .models import Store, EmailAccount
import request
from django.contrib.auth.hashers import make_password
from users.models import User
from email.header import decode_header
import email
import datetime as dt

def save_account_and_messages(email, password, messages):
    # Пример шифрования пароля
    encrypted_password = make_password(password)  # Реализовать шифрование

    # Сохранение аккаунта
    account, created = EmailAccount.objects.get_or_create(
        user=User.objects.get(pk=1), email=email,
        defaults={'password': password}
    )

    # Сохранение писем
    for msg in messages:
        Store.objects.create(
            owner=User.objects.get(pk=1),
            theme=msg['subject'],
            description=msg['body'],
            # date_sanding=msg['date_sanding'],
            date_receiving=msg['decoded_raw_date'],
            attachment=msg['attachment']
        )


def decode_mime_header(header_value):
    decoded_parts = decode_header(header_value)
    header_parts = []
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            encoding = encoding or 'utf-8'
            header_parts.append(part.decode(encoding))
        else:
            header_parts.append(part)
    return ''.join(header_parts)


def parse_date(date_string):
    # Парсим дату из строки заголовка
    date_tuple = email.utils.parsedate_tz(date_string)
    if date_tuple:
        # Конвертируем дату в объект datetime и форматируем её
        local_date = dt.fromtimestamp(email.utils.mktime_tz(date_tuple))
        return local_date.strftime('%d.%m.%Y %H:%M')
    return date_string
