#!/usr/bin/python
import sys
import time
import telepot
from pprint import pprint

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
      return
    pprint(msg)
    bot.sendMessage(chat_id, msg['text'])


TOKEN = sys.argv[1]
print 'received token :', TOKEN

bot = telepot.Bot(TOKEN)
pprint( bot.getMe() )

bot.notifyOnMessage(handle)

print 'Listening...'

while 1:
  time.sleep(10)