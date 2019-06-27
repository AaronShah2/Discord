"""
Written by Aaron Shah
6 / 24 / 2019
Bot Function: interacts with reddit
to perform miscallaneous functions
"""
from discord.ext.commands import Bot
from discord.ext.commands.core import CommandInvokeError
from prawcore import NotFound
from praw.models import MoreComments
import praw
"""
discord initialization
"""
BOT_PREFIX = ("?", "!")
TOKEN = "<insert-token>"
r_bot = Bot(command_prefix = BOT_PREFIX) 
"""
reddit initialization
"""
CLIENT_ID = "<insert-client-id>"
CLIENT_SECRET = "<insert-client-secret>"
USER_AGENT = "<insert-user-agent>"
reddit = praw.Reddit(client_id = CLIENT_ID,
                     client_secret = CLIENT_SECRET,
                     user_agent = USER_AGENT)
"""
Bot variables
"""
post_count = 1 #number of posts returned
comment_count = 10 #number of comments returned
"""
Function obtains data on latest post from inputted subreddit
sr_name = name of subreddit
"""
@r_bot.command(name = "NewPosts",
                description = "Retrieves data on the latest post in subreddit.",
                brief = "Data on latest post in subreddit",
                aliases = ["newposts", "NEWPOSTS", "NP","np"])
async def seeNewestPost(ctx, sr_name = "all"):
    try:
        reddit.subreddits.search_by_name(sr_name, exact=True)
        subreddit = reddit.subreddit(sr_name.strip())
        for post in subreddit.new(limit = post_count):
            response = (f"{post.name} posted the thread '{post.title}' with a score of {post.score}. "
                        f"Link: {post.url}")
            await ctx.send(response)
    except NotFound:
        await ctx.send("Subreddit does not exist")

"""
Function obtains top comment on latest post from inputted subreddit
sr_name = name of subreddit
"""
@r_bot.command(name = "NewComments",
                description = "Retrieves the latest original post in subreddit",
                brief = "Text of newest OP in subreddit",
                aliases = ["NEWCOMMENTS", "newcomments",
                           "nc", "NC"])
async def getNPComments(ctx, sr_name = "all"):
    try:
        reddit.subreddits.search_by_name(sr_name, exact=True)
        subreddit = reddit.subreddit(sr_name.strip())
        count = 0
        for comment in subreddit.stream.comments():
            count +=1
            response = (f"{comment.name} posted '{comment.body}'")
            await ctx.send(response)
            if comment_count <= count:
                break
    except NotFound:
        await ctx.send("Subreddit does not exist")

"""
Changes post count to inputted integer as long as
it is between 1 and 10
count - integer which post_count will default towards
"""
@r_bot.command(name = "PostCounter",
               description = ("Modifies the number of posts returned by bot"
                              " (must be between 1 and 10)."),
               brief = "Changes # of posts outputted",
               aliases = ["postcounter", "POSTCOUNTER","PC", "pc"])
async def changePostCount(ctx, count):
    try:
        count = float(count)
        if count > 10 or count < 1:
            await ctx.send(f"Inputted integer must be between between 1 and 10")
        else:
            global post_count
            post_count = int(count)
            await ctx.send(f"{post_count} post(s) will now be outputted.")
    except ValueError:
        await ctx.send(f"Inputted value is not an integer.")

"""
Changes comment count to inputted integer
as long as it is between 1 and 100
count - integer which comment_count will default towards
"""
@r_bot.command(name = "CommentCounter",
               description = ("Modifies the number of comments returned by bot"
                              " (must be between 1 and 100)"),
               brief = "Changes # of posts outputted",
               aliases = ["commentcounter", "COMMENTCOUNTER","CC","cc"])
async def changeCommentCount(ctx, count):
    try:
        count = float(count)
        if count >100 or count <1:
            await ctx.send(f"Inputted integer must be between between 1 and 100")
        else:
            global comment_count
            comment_count = int(count)
            await ctx.send(f"{comment_count} comment(s) will now be outputted.")
    except ValueError:
        ctx.send(f"Inputted value is not an integer.")
r_bot.run(TOKEN)
    
