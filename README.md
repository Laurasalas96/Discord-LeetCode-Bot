# Discord LeetCode bot 

A little LeetCode ("yeetcode") bot that:

1. Hands out a daily set of leetcode problems of one easy, one medium and one hard problem on a specific channel with the following message:

   > Heeeelllooo! here are today's daily leetcodes #24: 
   >     LC easy for those that want to take it easy:  https://leetcode.com/problems/design-hashmap
   >     LC medium for those who don't have time to waste: https://leetcode.com/problems/rotting-oranges
   >     LC hard for the beasts: https://leetcode.com/problems/binary-tree-maximum-path-sum

2. Hands out a random problem of a specific difficulty, as specified by a user with the following command

   ```
   $yeet random_problem medium
   ```

   where the last word can be "easy", "medium", "hard" or "random", and to which the bot replies, for instance with a medium problem as requested above:

   > You get a medium problem! https://leetcode.com/problems/rotting-oranges

The "database" of leetcode links is contained within the files *easy.txt*, *medium.txt*, and *hard.txt*, which can be modified to include more or less leetcode links.  Please refer to section ["adding more problems"](#adding-more-problems) if modifying these files. 

As of now, the bot is not hosted, so you will need to figure out how to host it on a free server.  More info about how to do so is written under the [requirements](#requirements) section. 

## Table of contents

- [Requirements](#requirements) 
- [Getting started](#getting-started) 
- [Usage](#usage)
  - [Commands for requesting a problem](#commands) 
  - [Daily leetcode problems](#daily-leetcodes)
  - [Adding more problems](#adding-more-problems) 
- [Further development](#further-development)
- [License & copyright](#license-and-copyright)  
- [Special thanks](#special-thanks)

## Requirements

##### The discord bot itself requires:

- An existing discord server with at least one channel where the bot will set 
- A bot token. You can find out how to get one [here](https://discordpy.readthedocs.io/en/stable/discord.html)

##### To run the server for the bot (you must configure it first!)

**NOTE: do *not* attempt to run the server before adding custom token and channel ID as indicated on the section below.**

- A server to run the script. A few options are: 
  - Running it from a raspberry pi ([tutorial here](https://www.gngrninja.com/code/2017/3/24/python-create-discord-bot-on-raspberry-pi))
  - Running it on a free (or paid) server. I use *heroku* ([tutorial here](https://medium.com/@linda0511ny/create-host-a-discord-bot-with-heroku-in-5-min-5cb0830d0ff2)) for mine and recommend it for this, as I already pre-configured the project. AWS would work too but may require further tinkering for installing libraries and such. 

##### The discord bot itself requires the following libraries to run:

NOTE: if you plan on using heroku, you don't need to worry about this, as the "*requirements.txt*" file included in this package already takes care of telling heroku which libraries to fetch. 

- the discord.py library, which can be found [here](https://github.com/Rapptz/discord.py)
- [PyNaCl 1.3.0 or newer](https://pypi.org/project/PyNaCl/#files)
- pandas (usually the server can just import it with python's standard libraries)
- [dnspython 1.16.0 or newer](https://pypi.org/project/dnspython/#files)
- [async-timeout 3.0.1 or newer](https://pypi.org/project/async-timeout/)

## Getting started

1. Grab the token of the bot (again, [here is a tutorial](https://discordpy.readthedocs.io/en/stable/discord.html)), and replace the token on line 15 of *bot.py*
2. Grab the channel ID of the channel you want the bot to send daily leetcodes in, and replace the number on line 24 of *bot.py* 
3. Host the bot on a server (see section above) 

That's it! The bot should now send a message on the specified channel for daily problems, and should be able to respond to the *$yeet* commands

## Usage

### Commands: 

```
$yeet help
```

lists out the commands for requesting a random leetcode 



```
$yeet random_problem easy
```

Gives a leetcode of easy difficulty, from one of the links in the "easy.txt" file  



```
$yeet random_problem medium
```

Gives a leetcode of medium difficulty, from one of the links in the "medium.txt" file  



```
$yeet random_problem hard
```

Gives a leetcode of hard difficulty, from one of the links in the "hard.txt" file  



```
$yeet random_problem surprise
```

Gives a leetcode of an unknown difficulty, from one of the links in any of the three files. 



### Daily LeetCodes

###### Disabling daily leetcodes:

Comment out the "*sendDaily*" function of line 168 of *bot.py*

##### How daily leetcodes work:

After specifying the channel ID where you want the bot to send a daily set of problems, the bot will send a daily set at the exact hour at which the server went online. 

For instance,  if the server went online at 8pm on a Wednesday,  every day it will send the "daily leetcode" at 8 pm on this channel. 

The bot is programmed to only send one set of problems per day, so even if the server were to go down and come back up later that day, it would not resend the message again. 



### Adding more problems

Simply modify the *.txt* file of the respective difficulty you want to add/remove problems to. 

Note that each file should have:

- One **VALID** LeetCode link per line, without **ANY** other character, including no quotation marks, comas, etc.
- At least **one** link per difficulty. 



## Further Development

**IMPORTANT:**

There may be links on the included text files that are only accessible to *pro* members of LeetCode. 

It would be neat if:

- A feature could be added to update the "leetcode database files" (the text files) by simply sending a command with a link to the bot
- Someone could host the bot permanently and publicly, so other people could more easily implement the bot in their server 
- A more efficient database implementation was done. 

## License and Copyright

leetcode.com , its content, website and branding are a property of LeetCode LLC. 

I am not in any way or form affiliated with the company.  

This bot is free to use anywhere. 

[Like this bot? Buy me a pizza slice on Patreon :-)](https://www.patreon.com/laurascode)

## Special Thanks 
1. Emma
2. my cat
