class User:
  def __init__(self, user_data, client):
    self.id = user_data["id"]
    self.username = user_data['username']
    self.display = user_data["global_name"]
    self.bot = user_data.get('bot', False)
    self.client = client
    self.dm = None
    self.session = client.session

  def set_dm(self, id: int):
    self.dm = id

  async def remove_message(self, message_id):
    if self.dm == None:
      raise Exception("You haven't created a DM before trying to send something to user")
    url = f'https://discord.com/api/v6/channels/{self.dm}/messages/{message_id}'
    headers = {
      'Authorization': f'Bot {self.client.token}',
      'Content-Type': 'application/json',
    }
    async with self.session.delete(url, headers=headers) as response:
      return await response.json()
  
  async def create_dm(self):
    url = f'https://discord.com/api/v9/users/@me/channels'
    headers = {
      'Authorization': f'Bot {self.client.token}',
      'Content-Type': 'application/json',
    }
    payload = {'recipient_id': self.id}
    async with self.session.post(url, headers=headers, json=payload) as response:
      if response.status_code == 200:
        idd = await response.json().get('id')
        self.set_dm(idd)
      else:
        raise Exception(f"Failed to create DM channel: {dm_response.json()}")
  
  async def send(self, content=None, embed=None, reference=None):
    if self.dm == None:
      raise Exception("You haven't created a DM before trying to send something to user")
    url = f'https://discord.com/api/v6/channels/{self.dm}/messages'
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