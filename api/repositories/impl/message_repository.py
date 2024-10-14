# repositories/message_repository.py
from api.models import Message


class MessageRepository:
    def create_message(self, conversation, owner_type, content='', image=None, file=None, sender=None):
        message = Message(
            conversation=conversation,
            owner_type=owner_type,
            content=content,
            image=image,
            file=file,
            sender=sender
        )
        message.save()
        return message

    def get_messages_by_conversation(self, conversation):
        return Message.objects.filter(conversation=conversation).order_by('timestamp')

    def get_message_by_id(self, message_id):
        return Message.objects.filter(id=message_id).first()

    def update_message(self, message_id, **kwargs):
        message = self.get_message_by_id(message_id)
        if message:
            for key, value in kwargs.items():
                setattr(message, key, value)
            message.save()
        return message

    def delete_message(self, message_id):
        message = self.get_message_by_id(message_id)
        if message:
            message.delete()
        return message