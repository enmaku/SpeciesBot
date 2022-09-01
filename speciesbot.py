import praw
import config
import time
import os
from pathlib import Path
import re
import traceback
from datetime import datetime

startTime = datetime.utcnow()

list_of_names = ["enmaku", "modestmenagerie"]
subreddits = ["speciesbot_testing"]
sig = "*I am a bot created to help with animal identification and natural history education."

commands = [
	{'command': "commandword", 'text': "This will be the reply when !commandword is typed"},
	{'command': "commandword2", 'text': "Another example, with !commandword2"}
]

specieslist = []
for filename in os.listdir('species'):
    specieslist.append(Path(filename).stem)

def bot_login():
	print("Logging in...")
	r = praw.Reddit(username=config.username,
	                password=config.password,
	                client_id=config.client_id,
	                client_secret=config.client_secret,
	                user_agent="speciesbot v0.1")
	print("Logged in!")

	return r


def checkComment(comment):
	if comment.saved or comment.author == r.user.me() or datetime.utcfromtimestamp(comment.created_utc) < startTime:
		return
	bldr = []

	for species in specieslist:
		if "*" + species + "*" in comment.body:
			print("String with " + species + " found in comment " + comment.id)
			with open("species/" + species + ".txt", "r") as f:
				comment_reply = f.read()
				bldr.append(comment_reply)
				print("Replied to comment " + comment.id)

	for command in commands:
		if "!" + command['command'] in comment.body:
			print("!" + command['command'] + " found in comment " + comment.id)
			bldr.append(command['text']) 
	if len(bldr): 
		bldr.append(sig) 
		comment.reply(body="\n\n--------------------------------------------------------\n\n".join(bldr))
	comment.save()


def run_bot(r):

	print("Checking reliable responders...")
	for username in list_of_names: #Check comments of reliable responders first
		user = r.redditor(username)
		for comment in user.comments.new(limit=10):
			checkComment(comment)

	print("Checking subreddit comments...")
	for comment in r.subreddit(subreddits).comments(limit=10): #Check comments in patrolled subreddits
		checkComment(comment)

	print("Checking subreddit posts...")
	for submission in r.subreddit(subreddits).new(limit=10): #Check posts in patrolled subreddits
		if submission.saved or submission.author == r.user.me() or datetime.utcfromtimestamp(submission.created_utc) < startTime:
			break

		if len(re.findall('\[.+\]', submission.title)) == 0:
			submission.reply(body="It looks like you didn't provide a rough geographic location [in square brackets] in your title. "
			                 "Some species are best distinguishable from each other by geographic range, and not all "
			                 "species live all places. Providing a location allows for a quicker, more accurate ID."
			                 + "\n\n" + "If you provided a location but forgot the correct brackets, ignore this message "
			                            "until your next submission. Thanks!" + "\n\n" + sig)
			print("Replied to submission " + submission.id)

		if submission.link_flair_text == "Dead":
			submission.reply(body="This automatic message accompanies any image of a dead, injured or roadkilled animal"
                    + "\n\n" + sig)
			print("Replied to Dead Animal flair - " + submission.id)

		submission.save()


r = bot_login()

while True:
	try:
		run_bot(r)
	except Exception as err:
		print("Hit an error in main loop")
		print(traceback.format_exc())

	print("Sleeping for 30 seconds...")
	time.sleep(30)