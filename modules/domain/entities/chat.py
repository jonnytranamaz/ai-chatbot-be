from datetime import datetime

class Room:
    def __init__(self, room_name: str):
        self.room_name = room_name

    def return_room_messages(self):
        return ChatMessage.objects.filter(room=self)

    def create_new_room_message(self, sender, message):
        new_message = ChatMessage(room=self, sender=sender, message=message)
        new_message.save()


class ChatMessage:
    def __init__(self, message: str, sender: str, room: Room, date: datetime = None):
        self.message = message
        self.date = date or datetime.now()
        self.room = room
        self.sender = sender

    def __str__(self):
        return f"{self.message} - {self.date}"
