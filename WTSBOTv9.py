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
sig = "*I am a bot created for /r/subreddithere to help with animal identification and natural history education."

commands = [
	{'command': "commandword", 'text': "This will be the reply when !commandword is typed"},
	{'command': "commandword2", 'text': "Another example, with !commandword2"}
]

specieslist = []
with open('species.txt', 'r') as filehandle:
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
			with open(species + ".txt", "r") as f:
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

	for username in list_of_names:
		user = r.redditor(username)
		for comment in user.comments.new(limit=10):
			checkComment(comment)

	for comment in r.subreddit('speciesbot_testing').comments(limit=10): ###'whatsthissnake+herpetology+snakes'
		checkComment(comment)

	for submission in r.subreddit('whatsthissnake').new(limit=10): ##change to test 'whatsthissnake'
		if submission.saved or submission.author == r.user.me() or datetime.utcfromtimestamp(submission.created_utc) < startTime:
			break

		if len(re.findall('\[.+\]', submission.title)) == 0:
			submission.reply("It looks like you didn't provide a rough geographic location [in square brackets] in your title. "
			                 "Some species are best distinguishable from each other by geographic range, and not all "
			                 "species live all places. Providing a location allows for a quicker, more accurate ID."
			                 + "\n\n" + "If you provided a location but forgot the correct brackets, ignore this message "
			                            "until your next submission. Thanks!" + "\n\n" + sig)
			print("Replied to submission " + submission.id)

		if submission.link_flair_text == "Dead, Injured or Roadkilled Snake":
			submission.reply("This automatic message accompanies any image of a dead, injured or roadkilled snake: " + "\n\n" +
			                 "Please don't kill snakes - they are a natural part of the ecosystem and [even species that "
			                 "use venom for prey acquisition and defense are beneficial to humans]"
			                 "(https://web.archive.org/web/20180802190346/https://umdrightnow.umd.edu/news/timber-rattlesnakes-vs-lyme-disease). One cannot expect "
			                 "outside to be sterile - if you see a snake you're in or around their preferred habitat. "
			                 "Most snakes are valued and as such are protected from collection, killing or harassment "
			                 "as non-game animals at the state level.\n\n[Neighborhood dogs]"
			                 "(http://livingalongsidewildlife.com/?p=3141) "
			                 "are more likely to harm people. Professional snake relocation services are often free or "
			                 "inexpensive, but snakes often die trying to return to their original home range, so it is "
			                 "usually best to enjoy them like you would songbirds or any of the other amazing wildlife "
			                 "native to your area. Commercial snake repellents are not effective - to discourage snakes, "
			                 "eliminate sources of food and cover; clear debris, stacked wood and eliminate rodent "
			                 "populations. Seal up cracks in and around the foundation/base of your home." + "\n\n" + sig)
			print("Replied to Dead Snake flair - " + submission.id)

		submission.save()
		
	for submission in r.subreddit('Herpetology').new(limit=10): ##change to test 'whatsthissnake'
		if submission.saved or submission.author == r.user.me() or datetime.utcfromtimestamp(submission.created_utc) < startTime:
			break

		if submission.link_flair_text == "Herpetoculture":
			submission.reply("Herpetology is the study of reptiles and amphibians. This post has been marked by the original poster as herpetoculture, which is the keeping of reptiles and amphibians in captivity. Herpetoculture posts are not suitable for /r/Herpetology and your post will be removed shortly. There are many suitable locations to post a pet or ask for pet care help, including /r/Herpetoculture and /r/Reptiles" + "\n\n" + "If you applied this flair in error, for example to a photo of an animal in the wild, please clear it." + "\n\n" + sig)
			print("Replied to Herpetoculture flair - " + submission.id)

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