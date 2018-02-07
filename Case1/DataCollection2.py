
import twitter
import json
import io
from urllib import unquote
from test import *

twitter_api = oauth_login()

q = "Superbowl"
results = twitter_search(twitter_api, q, max_results=10)

# Show one sample search result by slicing the list...
print json.dumps(results[0], indent=1)
with io.open('superbowl.json','w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(statuses, ensure_ascii=False)))
