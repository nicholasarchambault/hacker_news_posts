#!/usr/bin/env python
# coding: utf-8

# # Analyzing 'Hacker News' Posts
# by Nicholas Archambault
# 
# Hacker News is a website created by startup incubator Y-Combinator which allows users to submit posts related to technology and startups.  These posts can be voted and commented on, in a format similar to that of Reddit.  Posts with the most engagement can reach hundreds of thousands of visitors.
# 
# This project analyzes information on 20,000 Hacker News posts.  The dataset has been abridged from its full, 300,000-row version, and it represents a sample of all posts which received comments. 
# 
# Two types of popular Hacker News posts are `Ask HN`, where users submit a question to the Hacker News community, and `Show HN`, where users post their projects, products, or interesting stories and facts.
# 
# This project seeks to understand the metrics of these posts' popularity.  We examine whether `Ask HN` or `Show HN` posts receive higher levels of engagement, and whether posts created at a certain time generally garner more interactions from the community.

# ## Introduction
# 
# First, we'll read in the data and remove the headers.

# In[1]:


# Import data, clean header
from csv import reader
file = open("hacker_news.csv")
read_file = reader(file)
hn = list(read_file)
hn[:5]


# In[2]:


# Explore data
headers = hn[0]
hn = hn[1:]
print(headers)
hn[:5]


# ## Extracting Ask HN and Show HN Posts
# 
# We can see above that the data set contains the title of the posts, the number of comments for each post, and the date the post was created. Let's start by exploring the number of comments for each type of post. 
# 
# First, we'll identify posts that begin with either Ask HN or Show HN and separate the data for those two types of posts into different lists. Separating the data makes it easier to analyze in the following steps.

# In[3]:


# Create empty lists for each category
ask_posts = []
show_posts = []
other = []

# Increment each list for each occurrence of its post type
for row in hn:
    title = str(row[1].lower())
    if title.startswith("ask hn"):
        ask_posts.append(row)
    elif title.startswith("show hn"):
        show_posts.append(row)
    else:
        other.append(row)
print(len(ask_posts))
print(len(show_posts))
print(len(other))


# ## Average Number of Comments for Ask and Show Posts
# 
# Now that we've separated ask posts and show posts into different lists, we'll calculate the average number of comments each type of post receives.

# In[4]:


# Increment to count total number of ask comments
total_ask_comments = 0

for post in ask_posts:
    comments = int(post[4])
    total_ask_comments += comments

# Find average per post
avg_ask_comments = total_ask_comments/len(ask_posts)
avg_ask_comments


# In[5]:


# Repeat for show comments
total_show_comments = 0

for post in show_posts:
    comments = int(post[4])
    total_show_comments += comments

avg_show_comments = total_show_comments/len(show_posts)
avg_show_comments


# These figures reveal that Ask posts receive more comments, on average, than Show posts.

# ## Finding the Amount of Ask Posts and Comments by Hour Created
# 
# Next, we'll determine if we can maximize the amount of comments an ask post receives by creating it at a certain time. First, we'll find the amount of ask posts created during each hour of day, along with the number of comments those posts received. Then, we'll calculate the average amount of comments ask posts created at each hour of the day receive.

# In[6]:


# Import datetime reader
import datetime as dt
result_list = []

# Pull time and comment numbers from each post
for post in ask_posts:
    time = post[6]
    comments = int(post[4])
    result_list.append([time, comments])

# Initialize dictionaries to store hourly totals
counts_by_hour = {}
comments_by_hour = {}
date_format = "%m/%d/%Y %H:%M"

# Strip hours from datetime objects; increment dictionaries 
for i in result_list:
    date = i[0]
    comments = int(i[1])
    time = dt.datetime.strptime(date, date_format).strftime("%H")
    
    if time not in counts_by_hour:
        counts_by_hour[time] = 1
        comments_by_hour[time] = comments
    else:
        counts_by_hour[time] += 1
        comments_by_hour[time] += comments


# In[7]:


# Calculate average comments per hour
avg_by_hour = []

for i in counts_by_hour:
    avg_by_hour.append([i, comments_by_hour[i]/counts_by_hour[i]])

avg_by_hour


# To sort the results in order of comment numbers rather than by hour, we must swap the position of the two values.

# In[8]:


swap = []
for i in avg_by_hour:
    swap.append([i[1], i[0]])
swap = sorted(swap, reverse = True)
swap


# In[9]:


# Display top five hours of comment engagement
for i in swap[:5]:
    time = dt.datetime.strptime(i[1], "%H").strftime("%H:%M")
    comments = i[0]
    print("{}: {:.2f} average comments per post".format(time,comments))


# We can conclude that the 3:00pm EST hour averages about 60% more comments than the next closest hour, with ~39 comments per Ask post. We would maximize comment engagement with an Ask post by submitting it in the 3:00 hour.

# ## Finding the Amount of Show Posts and Comments by Hour Created
# 
# We can repeat these same steps for all Show posts, then compare whether the optimal posting hours are the same for both types.

# In[10]:


result = []
for post in show_posts:
    time = post[6]
    points = int(post[3])
    result.append([time, points])


# In[11]:


count_by_hour = {}
points_by_hour = {}
date_format = "%m/%d/%Y %H:%M"

for i in result:
    date = i[0]
    points = int(i[1])
    time = dt.datetime.strptime(date, date_format).strftime("%H")
    
    if time not in count_by_hour:
        count_by_hour[time] = 1
        points_by_hour[time] = points
    else:
        count_by_hour[time] += 1
        points_by_hour[time] += points


# In[12]:


avg_by_hour_2 = []

for i in counts_by_hour:
    avg_by_hour_2.append([i, points_by_hour[i]/counts_by_hour[i]])

avg_by_hour_2


# In[13]:


swap_2 = []
for i in avg_by_hour_2:
    swap_2.append([i[1], i[0]])

swap_2 = sorted(swap_2, reverse = True)
swap_2


# In[14]:


for i in swap_2[:5]:
    time = dt.datetime.strptime(i[1], "%H").strftime("%H:%M")
    points = i[0]
    print("{}: {:.2f} average points per post".format(time,points))


# ## Conclusion
# 
# After examining the popularity of each post type at all hours of the day, we find that the best hour for Ask posts is 3:00pm EST, when it garners around 60% more comments than the next most optimal hour. For Show posts, the best hour is 12:00pm EST. At their best hours, the two post types garner similar numbers of comments: Ask posts average ~4 more than Show posts. 
# 
# Ask posts tend to perform best in the afternoon and evening -- four of the top five hours are between 3:00pm and 9:00pm. Show posts, meanwhile, accrue the most comments in the middle of the day -- three of its top five hours are 11:00am, 12:00pm, and 1:00pm. 
# 
# The spread of comment totals for the top five hours for each post is a final intriguing factor. The difference between the average comments of the top and fifth most popular hours is ~23 for Ask posts, but just 10 for Show posts. This could indicate that the best-performing Ask posts, at any hour, tend to attract a concentration of comments, whereas comments are distributed across Show posts somewhat more evenly.
