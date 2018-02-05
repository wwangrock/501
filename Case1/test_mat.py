import matplotlib.pyplot as plt
bins=[0, 10, 20, 30, 40, 50, 100]

# Your code starts here
#   Please add comments or text cells in between to explain the general idea of each block of the code.
#   Please feel free to add more cells below this cell if necessary

user_mentions = [ user_mention['id']
                  for status in statuses
                      for user_mention in status['entities']['user_mentions']]
c = Counter(user_mentions)
plt.hist(c.values())

# Add a title and y-label ...
plt.title(label)
plt.ylabel('user_mentions')
plt.xlabel('bins')

# ... and display as a new figure
plt.figure()
plt.show()
