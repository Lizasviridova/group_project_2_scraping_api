import re
import asyncio
import pandas as pd
from telethon import TelegramClient

api_id=2040
api_hash="b18441a1ff607e10a989891a5462e627"
channel_name='rbc_news'

date_from = pd.Timestamp('2024-01-01', tz='UTC').to_pydatetime()

client = TelegramClient('sessions', api_id, api_hash)

def get_links(text):
    if text is None:
        return ''
    links = re.findall(r'https?://\S+', text)
    return ', '.join(links)

def get_media_type(msg):
    if msg.photo:
        return 'photo'
    if msg.video:
        return 'video'
    if msg.document:
        return 'document'
    return 'no_media'

def get_reactions(msg):
    if msg.reactions is None:
        return 0, ''
    total = 0
    parts = []

    for one_reaction in msg.reactions.results:
        total += one_reaction.count

        emoji = ''
        if hasattr(one_reaction.reaction, 'emoticon'):
            emoji = one_reaction.reaction.emoticon

        if emoji != '':
            parts.append(f'{emoji}:{one_reaction.count}')
        else:
            parts.append(str(one_reaction.count))
    return total, ', '.join(parts)
