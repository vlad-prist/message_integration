import imaplib
import ssl
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class EmailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        email = data['email']
        password = data['password']

        # Подключение к Яндекс IMAP серверу (неблокирующая функция)
        mail = imaplib.IMAP4_SSL('imap.yandex.com', 993)
        try:
            mail.login(email, password)
            mail.select("inbox")
            result, data = mail.search(None, "ALL")
            mail_ids = data[0]
            id_list = mail_ids.split()

            latest_emails = []
            for i in id_list[-5:]:
                result, msg_data = mail.fetch(i, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        latest_emails.append(response_part[1].decode('utf-8'))

            # Отправка писем обратно через WebSocket
            await self.send(text_data=json.dumps({
                'emails': latest_emails
            }))
        except imaplib.IMAP4.error:
            await self.send(text_data=json.dumps({
                'error': 'Ошибка авторизации'
            }))
