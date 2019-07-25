from flask import Flask, request
import json
import requests
import praw
import sys
import random
app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAADTk1w6nTQBAIvJNQwELQeaybMKm5QEke0qALECWBYtG9LG1p97la2Sdv8nIdAW2VcZBWb1CWPYVpHLpjUz23BWwBF2kTIsZBFUmcdknhWuK6KUPNFI2CwwNkZBbRn0NOIGxu2SRwoU6ZBFS9gyZAMVzPeURxJ34275Xcwc7OIjxsa3BQHvP'
reddit=praw.Reddit(client_id='EmKyAVOd_Lv-AA',client_secret='a2fM-qmVNQH6J-ejLtrzfT6LyJs',user_agent='Fellaini_Legend')
@app.route('/', methods=['GET'])
def handle_verification():
  print("Handling Verification.")
  if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
    print("Verification successful!")
    return request.args.get('hub.challenge', '')
  else:
    print("Verification failed!")
    return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
  print("Handling Messages")
  payload = request.get_data()
  print(payload)
  for sender, message in messaging_events(payload):
    print("Incoming from %s: %s" % (sender, message))
    send_message(PAT, sender, message)
  return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"

x=0
def send_message(token, recipient, text):
	x+=1
	subs=list(reddit.subreddit("dankmemes").hot(limit=20))
	payload=subs[20-x%20].title
	r = requests.post("https://graph.facebook.com/v2.6/me/messages",params={"access_token": token},data=json.dumps({"recipient": {"id": recipient},"message": {"text": payload.decode('unicode_escape')}}),headers={'Content-type': 'application/json'})
	if r.status_code != requests.codes.ok:
		print(r.text)
if __name__ == '__main__':
  app.run()
