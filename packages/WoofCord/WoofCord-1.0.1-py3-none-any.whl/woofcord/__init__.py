import asyncio
import time
import aiohttp
import logging
import json
import websockets
from .message import Message
from .msg import Msg
from .intents import all
from .embed import Embed
from .guild import Guild
from .user import User
from . import color as Color

class Client:
  def __init__(self, token, intents=None, prefix=None):
    self.token = token
    self.prefix = prefix
    self.event_handlers = {}
    self.commands = {}
    self.guilds = []
    self.user = None
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    self.logger = logger
    self.session = None
    if intents == None:
      self.intents = all()
      self.logger.warn("Intents were not set! Using default Intents (all)")
    else:
      self.intents = intents
    if prefix == None:
      self.logger.warn("Prefix was not set! Bot commands won't be available!")
    
  async def _get_session(self):
    self.session = aiohttp.ClientSession()
    self.logger.info("Aiohttp Session started")

  async def _close_session(self):
    await self.session.close()
    self.logger.info("Aiohttp Session stopped")

  def event(self, coro):
    if asyncio.iscoroutinefunction(coro):
      self.event_handlers[coro.__name__] = coro
    else:
      raise TypeError('Event handler must be a coroutine function')
    return coro

  def command(self, coro):
    if asyncio.iscoroutinefunction(coro):
      self.commands[coro.__name__] = coro
    else:
      raise TypeError('Command handler must be a coroutine function')
    return coro

  async def latency(self):
    start_time = time.perf_counter()
    async with self.session.get('https://discord.com/api/v9/gateway', headers={'Authorization': f'Bot {self.token}'}) as response:
      if response.status == 200:
        latency = (time.perf_counter() - start_time) * 1000  
        return latency
      else:
        raise Exception(f"HTTP Error: {response.status}")
    
  async def _connect(self):
    while True:
      try:
        self.logger.info("Starting Connection to Discord API")
        async with websockets.connect("wss://gateway.discord.gg/?v=10&encoding=json", max_size=10000000) as ws:
          await self._identify(ws)
          hello_message = await ws.recv()
          hello_data = json.loads(hello_message)
          heartbeat_interval = hello_data['d']['heartbeat_interval'] / 1000
          async def send_heartbeat():
            while True:
              await asyncio.sleep(heartbeat_interval)
              heartbeat_payload = {
                'op': 1,
                'd': None
              }
              await ws.send(json.dumps(heartbeat_payload))
          asyncio.create_task(send_heartbeat())                 
                    
          self.logger.info(f"Connection Successful. Latency {await self.latency()} MS")
          async for message in ws:
            try:
              await self._handle(message)
            except websockets.exceptions.PayloadTooBig:
              self.logger.error("Payload too big. Skipping this message.")

      except websockets.ConnectionClosed as e:
        self.logger.error(f'Connection closed: {e}')
        await asyncio.sleep(1)
        
      except Exception as e:
        self.logger.error(f'An error occurred: {e}')
        await asyncio.sleep(1)
      self.logger.info("Trying to Establish Connection")
        

  async def _identify(self, ws):
    await ws.send(json.dumps({
      "op": 2,
      "d": {
        "token": self.token,
        'intents': self.intents,
        "properties": {
          "$os": "WoofCord",
          "$browser": "WoofCord",
          "$device": "WoofCord",
        },
        "presence": {"status": "online", "afk": False},
      },
    }))

  async def _handle(self, message):
    event = json.loads(message)
    event_name = event.get('t')
    event_data = event.get('d')
    if event_name == 'MESSAGE_CREATE':
      handler = self.event_handlers.get('on_message_create')
      msg_obj = Message(event_data, self)
      if handler:
        await handler(msg_obj)
      elif self.prefix and event_data['content'].startswith(self.prefix):
        await self.process(event_data, _side=True)
    elif event_name == "READY":
      handler = self.event_handlers.get('on_ready')
      self.user = User(event_data['user'], self)
      for guild in event_data['guilds']:
        self.guilds.append(Guild(guild, self))
      if handler:         
        await handler(self.user)
    elif event_name == 'MESSAGE_UPDATE':
      handler = self.event_handlers.get('on_message_update')
      msg_obj = Msg(event_data, self)
      if handler:
        await handler(msg_obj)
    elif event_name == 'MESSAGE_DELETE':
      handler = self.event_handlers.get('on_message_delete')
      msg_obj = Message(event_data, self)
      if handler:
        await handler(msg_obj)
    elif event_name == "GUILD_CREATE":
      handler = self.event_handlers.get('on_guild_join')
      guild_obj = Guild(event_data, self)
      self.guilds.append(guild_obj)
      if handler:
        await handler(guild_obj)
    elif event_name == "GUILD_DELETE":
      handler = self.event_handlers.get('on_guild_leave')
      guild_obj = Guild(event_data, self)
      self.guilds.pop(guild_obj)
      if handler:
        await handler(guild_obj)
    elif event_name == "GUILD_UPDATE":
      handler = self.event_handlers.get('on_guild_update')
      guild_obj = Guild(event_data, self)
      if handler:
        await handler(guild_obj)
    elif event_name == "GUILD_MEMBER_ADD":
      handler = self.event_handlers.get('on_member_join')
      user_obj = User(event_data, self)
      if handler:
        await handler(user_obj)
    elif event_name == "GUILD_MEMBER_REMOVE":
      handler = self.event_handlers.get('on_member_leave')
      user_obj = User(event_data, self)
      if handler:
        await handler(user_obj)

  async def process(self, event_data, _side=False):
    if _side == False:
      event_data = event_data._JSON
    parts = event_data['content'][len(self.prefix):].split()
    command = parts[0]
    args = parts[1:]          
    msg_obj = Msg(event_data, self)
    handler = self.commands.get(command)
    if handler:
      await handler(msg_obj, *args)
        
  def start(self):
    asyncio.get_event_loop().run_until_complete(self._get_session())
    asyncio.get_event_loop().run_until_complete(self._connect())
    asyncio.get_event_loop().run_forever()