from requests_html import HTMLSession
import json
import os

import collections
import itertools
os.system('cls' if os.name == 'nt' else 'clear')

resolution = '1080x1920'
batch = 10
commentbatch = 2

postdict = {}
titles = []

disallowedids = []
dirtypostids = []
filteredpostids = []

urls = []
filteredurls = []

s = HTMLSession()

print(f"""
┌┐ ┬─┐┌─┐┌─┐┌┬┐╔╦╗╔╦╗╔═╗
├┴┐├┬┘├┤ ├─┤ ││ ║  ║ ╚═╗
└─┘┴└─└─┘┴ ┴─┴┘ ╩  ╩ ╚═╝
github.com/protonbread
═══════════════════════
[Resolution: {resolution}]
[Post Count: {batch}]
[Comment Count: {commentbatch}]
═══════════════════════
""")
print('[%]Scraping Reddit...')
url = 'https://gateway.reddit.com/desktopapi/v1/subreddits/AskReddit?rtj=only&redditWebClient=web2x&app=web2x-client-production&allow_over18=&include=prefsSubreddit&dist=8&forceGeopopular=false&layout=card&sort=hot'
r = s.get(url)
postjson = r.json()

for i in itertools.islice(postjson['posts'], batch):
    post = postjson['posts'][i]['title']
    url = postjson['posts'][i]['permalink']
    postid = postjson['posts'][i]['id']

    dirtypostids.append(postid)
    titles.append(post)
    urls.append(url)

donotreadlist = open('./donotread.txt', 'a+')
alreadyread = open('./alreadyread.txt', 'a+')

donotread = [item for item, count in collections.Counter(titles).items() if count > 1]
titles = [elem for elem in titles if elem not in donotread]

#Ad url's vary so we can't check for duplicates
for i in urls:
    if 'https://www.reddit.com/user/' in i:
        badid = i.split('/')
        disallowedids.append(f't3_{badid[6]}')
    else:
        filteredurls.append(i)

for i in dirtypostids:
    if '=' in i:
        pass
    else:
        filteredpostids.append(i)

for i in filteredpostids:
    if i in disallowedids:
        filteredpostids.remove(i)

lastid = filteredpostids[len(filteredpostids)-1]

for (postid, posttitle) in zip(filteredpostids, titles):
    postdict.update({postid: posttitle})

for i in filteredurls:
    pass


print(f"[!]Got {len(titles)} Posts And ")

#r = s.get('')