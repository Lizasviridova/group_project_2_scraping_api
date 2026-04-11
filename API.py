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

async def main():
    await client.start()
    rows = []
    offset_id = 0
    batch_size = 100
    request_num = 0
    stop = False

    while True:
        msgs = await client.get_messages(channel_name, limit = batch_size, offset_id = offset_id)
        request_num += 1
        if len(msgs) == 0:
            break
        for msg in msgs:
            if msg is None:
                continue
            if msg.date < date_from:
                stop = True
                break
            text = msg.get_message
            reactions_count, reactions_detail = get_reactions(msg)
            row = {'id_post': msg.id, 'date': msg.date, 'text': text, 'views': msg.views, 'reactions_count': reactions_count, 'reactions_detail': reactions_detail, 'forwards': msg.forwards, 'has_media': 0 if msg.media is None else 1, 'media_type': get_media_type(msg), 'links': get_links(text), 'post_url': f'https://t.me/{channel_name}/{msg.id}'}
            rows.append(row)
        if stop:
            break
        offset_id = msgs[-1].id
    df = pd.DataFrame(rows)
    df = df.sort_values('date').reset_index(drop = True)
    df.to_csv('rbk_posts.csv', index = False)
    await client.disconnect()
await main()
