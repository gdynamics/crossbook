import asyncio
from telethon import TelegramClient, sync, events, tl
import os

def dialogs_dict(client):
    """ Return a dictionary of the non-deleted accounts from the connected client.
    """
    dialogs_dict = {}
    for dialog in client.get_dialogs():
        entity = dialog.entity
        if type(entity) is tl.types.User: # Users have first name (mandatory), last name (optional), and username (optional)
            if not entity.deleted:
                name = entity.first_name
                name += ' ' + entity.last_name if entity.last_name else ''
                name += '(' + entity.username + ')' if entity.username else ''
        else: # Channels and groups just have a title
            name = entity.title
        dialogs_dict[name] = entity.id
    return dialogs_dict

async def shutdown_switch(event):
    """ Shutdown the client which received the argument NewMessage event if the text includes a keyword.
    """
    if 'sid' in event.raw_text:
        print('Close triggered!')
        await event.client.disconnect()

async def image_reception(event):
    """ Download media if it's a picture.
    """
    if event.media and type(event.media) is tl.types.MessageMediaPhoto:
        await event.download_media()

def main():
    # Initialization
    api_id = int(os.environ['TELETHON_API_ID'])
    api_hash = os.environ['TELETHON_API_HASH']

    # Body
    print('Starting client...')
    with TelegramClient('session_name', api_id, api_hash) as client:
        print('Client initializing...')
        # Choosing which groups to monitor the messages of
        dialogs = dialogs_dict(client)
        recepients = []
        for dialog in dialogs:
            test = dialog.lower()
            if 'cbtesting' in test or 'cooper' in test:
                recepients.append(dialogs[dialog])
        
        # Adding event listeners for...
        client.add_event_handler(shutdown_switch, events.NewMessage(recepients)) # Shutting down this program (killswitch)
        client.add_event_handler(image_reception, events.NewMessage(recepients)) #, incoming=True)) # Handling messages received.

        # Running until sigint or killswitch
        print('Client initialized.')
        client.run_until_disconnected()

if __name__ == "__main__":
    main()
