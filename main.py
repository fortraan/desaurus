import praw
import processor

reddit = praw.Reddit(client_id = "yDXsTk2DJG0TBg",
                     client_secret = "xshrPld57vEmDXYzXg6jOGdZJs0",
                     username = "desaurus_bot",
                     password = "desu396",
                     user_agent = "server:desaurus:2.0.0")

with open("commonwords.txt") as f:
    common = f.readlines()

ssf = processor.SimpleSynonymFinder("She proffered a grandiose idea", common)

print(ssf.simplify())