from slackclient import SlackClient
import os
import requests
import time

def upload_photo(client, path, filename):
    """ Takes the slackclient, path to file, and desired name of the file to upload, and uploads it.
    """
    if os.path.isfile(path):
        with open(path, 'rb') as photo:
            client.api_call(
                'files.upload',
                channels='CHQ8XNN3W',
                file=photo,
                filename=filename,
                title=filename
            )    

def download_photo(url, path):
    """ Download photo at url using urllib's request.
    """
    response = requests.get(url, headers={'Authorization': 'Bearer xoxb-602303763332-603785151702-XVoHKLGMJUTUlndndhgzB1UO'})
    with open(path, 'wb') as photo:
        for chunk in response.iter_content(chunk_size=128):
            photo.write(chunk)

def event_processor(event, client):
    """ Processes slackclient events captured using rtm_read. Takes the pure event (list with a dict in it), but performs work on it in its dict form.
    """
    # Manipulation
    event = event[0]

    # Handle messages from me
    if event['type'] == 'message' and event['user'] == 'UHQ8XNFFE':
            # Handle files I send
            if 'files' in event and 'url_private' in event['files'][0]:
                # Send me back the file i uploaded
                photo = event['files'][0]
                download_photo(photo['url_private'], photo['name'])
                time.sleep(5)
                upload_photo(client, photo['name'], photo['name'])

def main():
    # Intitialization
    slack_token = 'xoxb-602303763332-603785151702-XVoHKLGMJUTUlndndhgzB1UO'
    sc = SlackClient(slack_token)

    # Connecting to Slack
    if sc.rtm_connect(with_team_state=False):
        # Unending event loop
        i = 0
        while True:
            # Get new events if there are any
            event = sc.rtm_read()

            # Event processing
            if event:
                event_processor(event, sc)

            # Event loop footer
            time.sleep(1)
            i += 1
    else:
        print("Connection Failed")

if __name__ == '__main__':
    main()