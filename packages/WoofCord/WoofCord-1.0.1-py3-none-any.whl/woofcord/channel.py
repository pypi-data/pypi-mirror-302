class Channel:
  def __init__(self, channel_id, client):
    self.id = channel_id
    self.client = client
    self.session = client.session

  async def remove_message(self, message_id):
    url = f'https://discord.com/api/v6/channels/{self.id}/messages/{message_id}'
    headers = {
      'Authorization': f'Bot {self.client.token}',
      'Content-Type': 'application/json',
    }
    async with self.session.delete(url, headers=headers) as response:
      return await response.json()
  
  async def send(self, content=None, embed=None, reference=None):     
    url = f'https://discord.com/api/v6/channels/{self.id}/messages'
    headers = {
      'Authorization': f'Bot {self.client.token}',
      'Content-Type': 'application/json',
    }
    if embed:
      embed_json = embed.jsonize()
    else:
      embed_json = None
    payload = {
      'content': str(content) if content else None,
      'embeds': [embed_json],
      'message_reference': {'message_id': reference} if reference else None
    }
    async with self.session.post(url, headers=headers, json=payload) as response:
      return await response.json()