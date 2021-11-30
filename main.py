from requests_html import HTMLSession
import json
import os

import collections
import itertools
os.system('cls' if os.name == 'nt' else 'clear')

resolution = '1080x1920'
batch = 3
comment_batch = 2
thread_batch = 2

post_dict = {}
titles = []
post_ids = []
post_urls = []

s = HTMLSession()

print(f"""
┌┐ ┬─┐┌─┐┌─┐┌┬┐╔╦╗╔╦╗╔═╗
├┴┐├┬┘├┤ ├─┤ ││ ║  ║ ╚═╗
└─┘┴└─└─┘┴ ┴─┴┘ ╩  ╩ ╚═╝
github.com/protonbread
═══════════════════════
[Resolution: {resolution}]
[Post Count: {batch}]
[Comment Count: {comment_batch}]
═══════════════════════
""")

url = 'https://gateway.reddit.com/desktopapi/v1/subreddits/AskReddit?rtj=only&redditWebClient=web2x&app=web2x-client-production&allow_over18=&include=prefsSubreddit&dist=8&forceGeopopular=false&layout=card&sort=hot'
r = s.get(url)
post_json = r.json()
print('[%]Scraping Reddit...')
for i in itertools.islice(post_json['posts'], batch):
    titles.append(post_json['posts'][i]['title'])
    post_urls.append(post_json['posts'][i]['permalink'])
    post_ids.append(post_json['posts'][i]['id'])

donotread = [item for item, count in collections.Counter(titles).items() if count > 1]
titles = [elem for elem in titles if elem not in donotread]

#Ad url's vary so we can't check for duplicates

for i in post_urls[:]:
    if 'https://www.reddit.com/user/' in i:
        post_urls.remove(i)
        badid = i.split('/')[6]
        try:
            post_ids.remove(f't3_{badid}')
        except:
            pass

for i in post_ids[:]:
    if '=' in i:
        post_ids.remove(i)

last_id = post_ids[len(post_ids)-1]

for (posturl, posttitle) in zip(post_urls, titles):
    post_dict.update({posturl: posttitle})

comment_sel = '._1qeIAgB0cPwnLhDF9XSiJM'

for i in itertools.islice(post_urls, comment_batch):
    url = s.get(i)
    comment = url.html.find(comment_sel)
    for i in comment:
        print(i.text)

print(f"[!]Got {len(titles)} Posts And ")

#r = s.get('')