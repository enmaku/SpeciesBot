# SpeciesBot

SpeciesBot is a fork of a bot (SEB PhyloBot) originally created for /r/whatsthissnake, /r/snakes and /r/herpetology to help with snake identification and natural history education. It is being hosted and modified here with the hopes of creating a general-purpose species identification and husbandry information bot that will be useful to all animal-related subreddits.

# What SpeciesBot Does

At its core, SpeciesBot (like SEB PhyloBot before it) is a keyword-detection-and-response system. It looks for formatted species names and specific !commands in comments on certain subreddits and responds to them accordingly. There are also a small number of custom per-subreddit rules carried over from legacy PhyloBot functionality.

### Current List of Commands

- !deadsnake - Invokes the information from the dead snake auto response
- !myths - Provides a list of common snake myths ( in development - send me your favorite with a high quality link to a source refuting it and I'll put it in!)
- !poisonous or !venomous - Provides information on the definitions of venomous and poisonous as they relate to snakes
- !keels - Provides information on snake scale architecture.
- !cats - Provides information on outdoor cats, one of the largest threats to wildlife worldwide.
- !shed - Provides basic information and resources on identifying a snake from a shed skin.
- !blackrat - Provides a basic rundown of why you might hear the term 'black ratsnake' and why, as an enlightened individual, you don't repeat it.
- !resources - Provides a basic list of resources for worldwide snake identification
- !gluetrap - Provides information on gluetraps and how to get snakes unstuck
- !location - Invokes the 'location needed' message from the auto response on /r/whatsthissnake
- !wildpet - Provides information on why keeping wild snakes as pets isn't usually a good idea, even if they come from a pet store.
- !aggressive or !defensive - Rebuttal to the commonly misunderstood defensive posturing in snakes.
- !headshape - Explanation of how head shape isn't a reliable indication of if a snake is venomous
- !rhyme - A specific response to the 'red touches yellow, kill a fellow' rhyme.
- !hot - Provides information on best practices in biological terminology of venomous snakes.
- !specificepithet - Explains species names and their formatting. Uses an example, but not snake specific.
- !harmless - An explanation of the word harmless and how the category does indeed include species that bite in self defense.
- !ecdysis - Provides information on the shedding process, needs to be expanded.
- !snakehole - Info on how snakes don't dig their own burrows
- !fiveline - Info on commonly confused skinks with yellow lines and blue tails
- !pool - Provides information on mitigating pools as wildlife sinks

# How to Contribute

- If you're a programmer, I don't need to tell you what to do. This is a github repo, you can see what the code does. Make it do more. Make it do what it already does better. If you've got an idea, we're open to hearing it.
- If you're more of a biology enthusiast, please feel free to contribute to our [species](https://github.com/enmaku/SpeciesBot/tree/main/species) list or add useful [commands](https://github.com/enmaku/SpeciesBot/tree/main/commands).
- If you're a user or moderator of a subreddit and would like to use SpeciesBot, simply add yourself to [the list](https://github.com/enmaku/SpeciesBot/blob/main/subreddits.txt). We will contact the moderators of each subreddit for explicit permission before approving such submissions.
- We also maintain a [list](https://github.com/enmaku/SpeciesBot/blob/main/reliable.txt) of "reliable responders" who can usually be counted on to both reliably identify species within their specialties and educate the public in a respectable manner. SpeciesBot responds to such users no matter what subreddit they may currently be perusing. This takes both resources and time for the bot and creates potential spam issues if misused. To that end, reliable responders are currently screened using an individual, subjective approach. Efforts are underway to create more standardized criteria. You may request reliable responder status by editing your reddit username into the linked file or by asking one of the developers via reddit or discord. We may also contact users we believe to be worthy of the status.

All of the linked files may be edited by anyone with a free github account. To add a species or command, create a new file with a name in the format "Species genus.md" in the appropriate folder. To create a new command, create a new file with a file name in the format "command.md" in the appropriate folder - the comman will then be triggerable by typing "!command" in a patrolled subreddit.

Such edits will not take effect until a pull request is created by the user and accepted by one of the developers. For more information on this process, please see the [Editing files](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files) and [Adding a file to a repository](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) sections of GitHub's documentation, paying special attention to the *Editing files in another user's repository* section. You can also just go to the appropriate file or folder and seek out an add/edit button - GitHub makes it pretty easy to follow the process. Fill out the appropriate fields, click the green buttons, when it says you have an open pull request, you're done. Check back later to see if your request is accepted, rejected, commented upon, or has suggested edits.
