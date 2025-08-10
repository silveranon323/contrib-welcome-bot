import os
import sys
import json
import requests

def main():
    github_event_path = os.getenv('GITHUB_EVENT_PATH')
    if not github_event_path:
        print("GITHUB_EVENT_PATH not set.")
        sys.exit(1)

    with open(github_event_path) as f:
        event = json.load(f)

    if event.get('action') != 'opened' or 'pull_request' not in event:
        print("Not a pull_request opened event, skipping.")
        sys.exit(0)

    pr = event['pull_request']
    pr_number = pr['number']
    repo = pr['base']['repo']['name']         # fixed here
    owner = event['repository']['owner']['login']
    author = pr['user']['login']

    greeting_message = os.getenv('INPUT_GREETING_MESSAGE', 'Hello @${username}! Thanks for opening this PR.')
    greeting_message = greeting_message.replace('${username}', f'@{author}')

    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("GITHUB_TOKEN not set.")
        sys.exit(1)

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    comments_url = pr['comments_url']
    response = requests.get(comments_url, headers=headers)
    response.raise_for_status()
    comments = response.json()

    for comment in comments:
        if comment.get('user', {}).get('type') == 'Bot' and greeting_message.split()[0] in comment.get('body', ''):
            print("Greeting comment already exists, skipping.")
            sys.exit(0)

    post_response = requests.post(comments_url, headers=headers, json={'body': greeting_message})
    post_response.raise_for_status()

    print("Greeting comment posted successfully.")

if __name__ == "__main__":
    main()
