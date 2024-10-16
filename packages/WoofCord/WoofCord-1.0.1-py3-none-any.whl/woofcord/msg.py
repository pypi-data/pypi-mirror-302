from .channel import Channel
from .user import User
from .message import Message

class Msg:
  def __init__(self, message_data, client):
    self.id = message_data['id']
    self._JSON = message_data
    self.content = message_data['content']
    self.message = Message(message_data, client)
    self.author = User(message_data['author'], client)
    self.channel = Channel(message_data['channel_id'], client)

  async def remove(self):
    return await self.channel.remove_message(self.id)
    
  async def send(self, content=None, embed=None):
    return await self.channel.send(content, embed)

  async def reply(self, content=None, embed=True):
    return await self.channel.send(content, embed, reference=self.id)