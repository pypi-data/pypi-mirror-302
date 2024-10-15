import re
import os
import asyncio
import aiofiles

import httpx

from yandexbot.types.message import PolingResponse, Message


class BotAPI:
    def __init__(
        self,
        token: str,
        base_url: str = "https://botapi.messenger.yandex.net/bot/v1",
        polling_interval: int = 1,
    ):
        self.base_url = base_url
        self.headers = {"Authorization": f"OAuth {token}"}
        self.handlers = {}

        self.polling_offset = 0
        self.polling_interval = polling_interval
        self.polling_endpoint = "/messages/getUpdates/?limit={limit}&offset={offset}"

        self.send_text_message_endpoint = "/messages/sendText"
        self.send_file_message_endpoint = "/messages/sendFile"
        self.send_image_message_endpoint = "/messages/sendImage"

    async def get_new_messages(self):
        response = await self.call_api_for_messages()
        new_messages = []

        for update in response.updates:
            new_messages.append(update)

        return new_messages

    async def call_api_for_messages(self) -> PolingResponse:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.base_url
                + self.polling_endpoint.format(limit=100, offset=self.polling_offset),
                headers=self.headers,
            )
            if response.status_code == 200:
                polling_response = PolingResponse.model_validate(response.json())
                update_ids = [update.update_id for update in polling_response.updates]
                if update_ids:
                    self.polling_offset = max(update_ids) + 1
                return polling_response
            else:
                print(response.status_code)

    async def send_text_message(self, message: Message, text: str):
        """
        Sends a text message. Automatically determines whether to send via login or chat_id.
        :param message: The received message object, which contains chat_id or login.
        :param text: The content of the message.
        """
        recipient, recipient_type = self.get_recipient_info(message)
        async with httpx.AsyncClient() as client:
            payload = {recipient_type: recipient, "text": text}
            response = await client.post(
                self.base_url + self.send_text_message_endpoint,
                headers=self.headers,
                json=payload,
            )
            if response.status_code != 200:
                print(f"Failed to send text message: {response.status_code}")

    async def send_file_message(self, message: Message, file_path: str):
        """
        Sends a file message. Automatically determines whether to send via login or chat_id.
        :param message: The received message object, which contains chat_id or login.
        :param file_path: The file path of the document to send.
        """
        recipient, recipient_type = self.get_recipient_info(message)
        async with httpx.AsyncClient() as client:
            files = {"document": open(file_path, "rb")}
            response = await client.post(
                self.base_url + self.send_file_message_endpoint,
                headers=self.headers,
                data={recipient_type: recipient},
                files=files,
            )
            if response.status_code != 200:
                print(f"Failed to send file message: {response.status_code}")

    async def send_image_message(self, message: Message, image_path: str):
        """
        Sends an image message. Automatically determines whether to send via login or chat_id.
        :param message: The received message object, which contains chat_id or login.
        :param image_path: The file path of the image to send.
        """
        recipient, recipient_type = self.get_recipient_info(message)
        async with httpx.AsyncClient() as client:
            files = {"image": open(image_path, "rb")}
            response = await client.post(
                self.base_url + self.send_image_message_endpoint,
                headers=self.headers,
                data={recipient_type: recipient},
                files=files,
            )
            if response.status_code != 200:
                print(f"Failed to send image message: {response.status_code}")

    async def get_file(self, file_id: str, file_name: str, save_folder: str) -> str:
        """
        Downloads the file from Yandex Messenger by file_id and saves it to the specified folder asynchronously.
        :param file_id: The ID of the file to be downloaded.
        :param file_name: The name of the file.
        :param save_folder: The folder where the file will be saved.
        :return: The path of the saved file or None if failed.
        """
        file_download_url = f"{self.base_url}/messages/getFile"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                file_download_url,
                headers=self.headers,
                data={"file_id": file_id}
            )
            if response.status_code == 200:
                # Ensure the save folder exists
                os.makedirs(save_folder, exist_ok=True)
                
                # Save the file asynchronously
                file_path = os.path.join(save_folder, file_name)
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(response.content)
                
                print(f"File saved to {file_path}")
                return file_path
            else:
                print(f"Failed to download file: {response.status_code}")
                return None

    def get_recipient_info(self, message: Message):
        """
        Determines whether to use the login or chat_id to send the message.
        :param message: The message object to extract recipient info.
        :return: A tuple of (recipient, recipient_type), where recipient_type is either 'login' or 'chat_id'.
        """
        if message.from_.login:
            return message.from_.login, "login"
        else:
            return message.chat.id, "chat_id"

    def message_handler(self, pattern=None, message_type="text"):
        """
        Decorator to register a message handler for a specific pattern or message type.
        :param pattern: A string or regex pattern to match message text (for text messages).
        :param message_type: The type of message to handle (e.g., 'text', 'file', 'image', 'sticker').
        """

        def decorator(func):
            if message_type == "text" and pattern:
                self.handlers[(message_type, pattern)] = func
            else:
                self.handlers[(message_type, None)] = func
            return func

        return decorator


    async def process_message(self, message: Message):
        if message.text:
            for (message_type, pattern), handler in self.handlers.items():
                if message_type == "text" and re.match(pattern, message.text):
                    await handler(message)
                    break
        elif message.file:
            handler = self.handlers.get(("file", None))
            if handler:
                await handler(message)
        elif message.images:
            handler = self.handlers.get(("image", None))
            if handler:
                await handler(message)
        elif message.sticker:
            handler = self.handlers.get(("sticker", None))
            if handler:
                await handler(message)
        else:
            print("Received an unknown type of message")


    async def start_polling(self):
        print("Polling for new messages...")

        while True:
            new_messages = await self.get_new_messages()

            if new_messages:
                for message in new_messages:
                    print(f"Received message: {message.text}")
                    await self.process_message(message)

            await asyncio.sleep(self.polling_interval)