# repositories.py
from .models import Room, ChatMessage

class RoomRepository:
    @staticmethod
    def create_room(room_name):
        room = Room(room_name=room_name)
        room.save()
        return room

    @staticmethod
    def get_room(room_id):
        try:
            return Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return None

    @staticmethod
    def update_room(room_id, room_name=None):
        room = RoomRepository.get_room(room_id)
        if room:
            if room_name is not None:
                room.room_name = room_name
            room.save()
            return room
        return None

    @staticmethod
    def delete_room(room_id):
        room = RoomRepository.get_room(room_id)
        if room:
            room.delete()
            return True
        return False

    @staticmethod
    def list_rooms():
        return Room.objects.all()

    @staticmethod
    def get_room_messages(room_id):
        room = RoomRepository.get_room(room_id)
        if room:
            return room.return_room_messages()
        return None

    @staticmethod
    def create_room_message(room_id, sender, message):
        room = RoomRepository.get_room(room_id)
        if room:
            return room.create_new_room_message(sender, message)
        return None

class ChatMessageRepository:
    @staticmethod
    def get_message(message_id):
        try:
            return ChatMessage.objects.get(id=message_id)
        except ChatMessage.DoesNotExist:
            return None

    @staticmethod
    def delete_message(message_id):
        message = ChatMessageRepository.get_message(message_id)
        if message:
            message.delete()
            return True
        return False

    @staticmethod
    def list_messages():
        return ChatMessage.objects.all()