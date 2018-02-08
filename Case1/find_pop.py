import json
import io
from collections import Counter
from prettytable import PrettyTable


with io.open('superbowl-t.json',encoding='utf-8') as f:
    statuses = json.load(f)

status_texts = [ status['text']
                 for status in statuses ]

screen_names = [ user_mention['screen_name']
                 for status in statuses
                     for user_mention in status['entities']['user_mentions'] ]

hashtags = [ hashtag['text']
             for status in statuses
                 for hashtag in status['entities']['hashtags'] ]

# Compute a collection of all words from all tweets
words = [ w
          for t in status_texts
              for w in t.split() ]

counts = Counter(words)



#plot a table

pt = PrettyTable(field_names=['words', 'Count'])
c = Counter(words)
[ pt.add_row(kv) for kv in c.most_common()[:30] ]
pt.align['words'], pt.align['Count'] = 'l', 'r' # Set column alignment
print pt
