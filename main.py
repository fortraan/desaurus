import praw
import processor
from auth import CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD

reddit = praw.Reddit(client_id = CLIENT_ID,
                     client_secret = CLIENT_SECRET,
                     username = USERNAME,
                     password = PASSWORD,
                     user_agent = "server:desaurus:2.0.0")

with open("commonwords.txt") as f:
    common = f.readlines()

ssf = processor.SimpleSynonymFinder("She proffered a grandiose idea", common)

print(ssf.simplify())