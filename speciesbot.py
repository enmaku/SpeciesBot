import praw
import config
import time
import os
import requests
import re
import traceback
from datetime import datetime

startTime = datetime.utcnow()

list_of_names = ["user1", "user2", "user3"]
subreddits = ["speciesbot_testing"]
sig = "*I am a bot created for /r/subreddithere to help with animal identification and natural history education."

commands = [
	{'command': "commandword", 'text': "This will be the reply when !commandword is typed"},
	{'command': "commandword2", 'text': "Another example, with !commandword2"}
]

specieslist = []
with open('species/species.txt', 'r') as filehandle:
	for line in filehandle:
		specieslist.append(line.strip())


def bot_login():
	print("Logging in...")
	r = praw.Reddit(username=config.username,
	                password=config.password,
	                client_id=config.client_id,
	                client_secret=config.client_secret,
	                user_agent="phylohelper v0.1")
	print("Logged in!")

	return r


def checkComment(comment):
	if comment.saved or comment.author == r.user.me() or datetime.utcfromtimestamp(comment.created_utc) < startTime:
		return
	bldr = [] # create an empty array


	for species in specieslist:
		if "*" + species + "*" in comment.body:
			print("String with \"+ species""\" found in comment " + comment.id)
			with open("species/" + species + ".txt", "r") as f:
				comment_reply = f.read()
				bldr.append(comment_reply)
				print("Replied to comment " + comment.id)

	for command in commands:
		if "!" + command['command'] in comment.body:
			print("!" + command['command'] + " found in comment " + comment.id)
			bldr.append(command['text']) ##was comment.reply(command['text'] + "\n\n" + sig)
	if len(bldr): # if we have appended anything to bldr
		bldr.append(sig) # add the signature at the end
		comment.reply("\n\n--------------------------------------------------------\n\n".join(bldr)) # take each of the replies we put in the list, separate them with the double newline, and reply to the comment
	comment.save()


def run_bot(r):
	print("Obtaining 10 comments...")

	for username in list_of_names: #Check comments of reliable responders first
		user = r.redditor(username)
		for comment in user.comments.new(limit=10):
			checkComment(comment)

	for comment in r.subreddit("+".join(subreddits)).comments(limit=10): #Check comments in patrolled subreddits
		checkComment(comment)

	for submission in r.subreddit("+".join(subreddits)).new(limit=10): #Check posts in patrolled subreddits
		if submission.saved or submission.author == r.user.me() or datetime.utcfromtimestamp(submission.created_utc) < startTime:
			break

		if len(re.findall('\[.+\]', submission.title)) == 0:
			submission.reply("It looks like you didn't provide a rough geographic location [in square brackets] in your title. "
			                 "Some species are best distinguishable from each other by geographic range, and not all "
			                 "species live all places. Providing a location allows for a quicker, more accurate ID."
			                 + "\n\n" + "If you provided a location but forgot the correct brackets, ignore this message "
			                            "until your next submission. Thanks!" + "\n\n" + sig)
			print("Replied to submission " + submission.id)

		if submission.link_flair_text == "Dead":
			submission.reply("This automatic message accompanies any image of a dead, injured or roadkilled animal"
                    + "\n\n" + sig)
			print("Replied to Dead Animal flair - " + submission.id)

		submission.save()
		
	for submission in r.subreddit("+".join(subreddits)).new(limit=10): #Check for trap flairs
		if submission.saved or submission.author == r.user.me() or datetime.utcfromtimestamp(submission.created_utc) < startTime:
			break

		if submission.link_flair_text == "Trap":
			submission.reply("That flair is a trap meant to catch people posting off-topic things!" + "\n\n" + sig)
			print("Replied to Trap flair - " + submission.id)

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