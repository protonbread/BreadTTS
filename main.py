from requests_html import HTMLSession
import json
import os

import collections
import itertools
os.system('cls' if os.name == 'nt' else 'clear')

resolution = '1080x1920'
batch = 15
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
[Reply Count: {thread_batch}]
═══════════════════════
""")

url = 'https://reddit.com/r/askreddit.json'
r = s.get(url)
post_json = r.json()['data']
print('[%]Scraping Reddit...')
for i in range(comment_batch):
    titles.append(post_json['children'][i]['title'])
    print(titles)
    post_urls.append(f'{post_json["children"][i]["url"]}.json')
    post_ids.append(post_json['children'][i]['id'])

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

comment_replys = []
comments = {}

for u in post_urls:
    post_json = s.get(u).json()
    comment_data = post_json[1]['data']['children'][post_urls.index(u)]['data']

    for r in range(comment_batch):

        reply_data = post_json[1]['data']['children'][r]['data']
        comment_author = (reply_data['author'])
        comment_body = (reply_data['body'])

        for i in range(thread_batch):
            try:
                comment_replys.append(reply_data['replies']['data']['children'][i]['data']['body'])
            except:
                print('[*]Reply Not In Range')
            comments.update({comment_author:{u:{comment_body: list(comment_replys)}}})                
        comment_replys.clear()
    

print(f"[!]Got {len(titles)} Posts And {len(comments)} Threads")
print(comments)
#r = s.get('')