from telethon.tl.custom.conversation import Conversation
from telethon import TelegramClient
from telethon import types

from telethon.tl.custom import Message
from . import stop_event


class EasyConv(Conversation):
    def __init__(
        self,
        client: TelegramClient,
        user_id: int,
        timeout: float = 100_000,
        cancel_command: str = "/cancel",
        cancelled_info: str = "❗️ Operation cancelled",
    ):
        super().__init__(
            client,
            input_chat=user_id,
            timeout=timeout,
            total_timeout=timeout,
            max_messages=1000_000,
            exclusive=False,
            replies_are_responses=True,
        )
        self.cancel_command = cancel_command
        self.cancelled_info = cancelled_info

    async def check_cancel(self, text: str) -> str:
        if text.lower().startswith(self.cancel_command.lower()):
            await self.send_message(f"❗️ Operation cancelled")
            return stop_event()

        return text

    async def send_cancel_info(self) -> None:
        await self.send_message(
            f"ℹ️ To cancel the operation at any point use {self.cancel_command} command."
        )

    async def get_text_response(self, prompt: str) -> str:
        if prompt:
            await self.send_message(prompt)
        resp = await self.get_response()
        return await self.check_cancel(resp.message)

    async def get_number_response(self, prompt: str) -> int:
        try:
            return int(await self.get_text_response(prompt))

        except ValueError:
            await self.send_message(f"❗️ You didn't enter a number. Enter again.")
            return await self.get_number_response(prompt)

    async def get_file(self, prompt: str) -> tuple[types.MessageMediaDocument, Message]:
        await self.send_message(prompt)
        resp: Message = await self.get_response()
        await self.check_cancel(str(resp.message))
        if not isinstance(resp.media, types.MessageMediaDocument):
            await self.send_message(
                "❗️ You didn't upload a valid file in the message. Please try again."
            )
            return await self.get_file(prompt)

        return resp.media, resp
