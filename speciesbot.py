import praw
import config
import time
import os
from pathlib import Path
import re
import traceback
from datetime import datetime
import threading
import urllib

thread_lock = threading.Lock()

startTime = datetime.utcnow()

list_of_names = []
subreddits = ""
sig = ""
commands = []
specieslist = []

def load_data():
	global list_of_names, subreddits, sig, commands, specieslist
 
	list_of_names = []
	subreddits = ""
	sig = ""
	commands = []
	specieslist = []

	with open("reliable.txt", "r") as f:
		list_of_names = f.read().splitlines()

	with open("subreddits.txt", "r") as f:
		subreddits = "+".join(f.read().splitlines())

	with open("signature.md", "r") as f:
		sig = f.read()

	for filename in os.listdir("commands"):
		with open(os.path.join("commands", filename), "r") as f:
			commandtext = f.read()
			commands.append(Path(filename).stem)

	for filename in os.listdir("species"):
		specieslist.append(Path(filename).stem)
    
print("Loading data from files")
load_data()

def bot_login():
	print("Logging in...")
	r = praw.Reddit(username=config.username,
	                password=config.password,
	                client_id=config.client_id,
	                client_secret=config.client_secret,
	                user_agent="speciesbot v0.1",
                 	ratelimit_seconds=600)
	print("Logged in!")

	return r


def checkComment(comment):
	if comment.saved or comment.author == r.user.me() or datetime.utcfromtimestamp(comment.created_utc) < startTime:
		return
	bldr = []
 
	with thread_lock:
		for species in specieslist:
			if "*" + species + "*" in comment.body:
				print("String with " + species + " found in comment " + comment.id)
				with open("species/" + species + ".md", "r") as f:
					comment_reply = f.read()
					bldr.append(comment_reply)
					print("Replied to comment " + comment.id)

		for command in commands:
			if "!" + command in comment.body:
				with open("commands/" + command + ".md", "r") as f:
					comment_reply = f.read()
					bldr.append(comment_reply)
				print("!" + command + " found in comment " + comment.id)
		if "!account" in comment.body:
			account = comment.body.strip().replace("!account ", "").capitalize()
			print("Account URL requested for " + account)
			if os.path.exists("species/" + account + ".md"):
				url = "https://github.com/enmaku/SpeciesBot/edit/main/species/" + urllib.parse.quote(account) + ".md"
				bldr.append("It looks like an account for that species already exists.\n\n[Click Here](" + url + ") to edit it.")
			else:
				url = "https://github.com/enmaku/SpeciesBot/new/main?filename=species/" + urllib.parse.quote(account) + ".md"
				bldr.append("A record for that species does not appear to exist.\n\n[Click Here](" + url + ") to create it.")
			bldr.append("\n\nPlease note that you may need to create a (free) GitHub account in order to finalize your submission.")
		if len(bldr): 
			bldr.append(sig) 
			comment.reply(body="\n\n--------------------------------------------------------\n\n".join(bldr))
		comment.save()

def reliable_responders(r):
    # Check reliable responder comments
	print("Checking reliable responders...")
	for username in list_of_names: 
		user = r.redditor(username)
		for comment in user.comments.new(limit=10):
			checkComment(comment)
	print("Reliable responders check complete.")


def subreddit_comments(r):
    # Check subreddit comments
	print("Checking subreddit comments...")
	for comment in r.subreddit(subreddits).comments(limit=10):
		checkComment(comment)
	print("Subreddit comments check complete.")


def subreddit_post_rules(r):
    # Subreddit-specific post rules
	print("Checking subreddit-specific rules...")
	for submission in r.subreddit("whatsthissnake").new(limit=10):
		if submission.saved or submission.author == r.user.me() or datetime.utcfromtimestamp(submission.created_utc) < startTime:
			break

		# r/whatisthissnake posts require a [location]
		if len(re.findall("\[.+\]", submission.title)) == 0:
			submission.reply("It looks like you didn't provide a rough geographic location [in square brackets] in your title. "
			                 "Some species are best distinguishable from each other by geographic range, and not all "
			                 "species live all places. Providing a location allows for a quicker, more accurate ID."
			                 + "\n\n" + "If you provided a location but forgot the correct brackets, ignore this message "
			                            "until your next submission. Thanks!" + "\n\n" + sig)
			print("Replied to submission " + submission.id)

		# r/whatisthissnake does not like it when people kill snakes
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
		
	# r/herpetology doesn't allow herpetoculture posts
	for submission in r.subreddit("Herpetology").new(limit=10):
		if submission.saved or submission.author == r.user.me() or datetime.utcfromtimestamp(submission.created_utc) < startTime:
			break

		if submission.link_flair_text == "Herpetoculture":
			submission.reply("Herpetology is the study of reptiles and amphibians. This post has been marked by the original poster as herpetoculture, which is the keeping of reptiles and amphibians in captivity. Herpetoculture posts are not suitable for /r/Herpetology and your post will be removed shortly. There are many suitable locations to post a pet or ask for pet care help, including /r/Herpetoculture and /r/Reptiles" + "\n\n" + "If you applied this flair in error, for example to a photo of an animal in the wild, please clear it." + "\n\n" + sig)
			print("Replied to Herpetoculture flair - " + submission.id)

		submission.save()
	print("Subreddit-specific rules check complete.")
    
    
def run_bot(r):	
	threads = []
	if config.reliable_responders:
		threads.append(threading.Thread(target=reliable_responders, args=(r,)))
	if config.subreddit_comments:
		threads.append(threading.Thread(target=subreddit_comments, args=(r,)))
	if config.subreddit_rules:
		threads.append(threading.Thread(target=subreddit_post_rules, args=(r,)))
  
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()


r = bot_login()

i = 0
while True:
	try:
		run_bot(r)
	except Exception as err:
		print("Hit an error in main loop")
		print(traceback.format_exc())

	print("Sleeping for " + str(config.sleep_time) + " seconds...")
	time.sleep(config.sleep_time)
	
	i += 1
	if i == config.reload_every:
		print("Reloading bot data...")
		load_data()
		i = 0