from domain.entities import ChatMessage, Room

class ChatService:
    @staticmethod
    def create_room(room_name: str) -> Room:
        room = Room(room_name)
        return room

    @staticmethod
    def send_message(room: Room, sender: str, message: str) -> ChatMessage:
        chat_message = ChatMessage(room=room, sender=sender, message=message)
        return chat_message

    @staticmethod
    def get_room_messages(room: Room):
        return room.return_room_messages()
