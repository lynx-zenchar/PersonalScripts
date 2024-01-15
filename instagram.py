#!/usr/bin/env python3
'''
This program can help me check who I follow and who I don't follow on instagram. Data will be subject to change depending on when I gathered the data.

'''
from bs4 import BeautifulSoup 

# file path
followers_file = "/mnt/c/Users/matte/Downloads/instagram-matthewjacob_eleazar-2024-01-13-AUENuhz2/connections/followers_and_following/followers_1.html"

following_file = "/mnt/c/Users/matte/Downloads/instagram-matthewjacob_eleazar-2024-01-13-AUENuhz2/connections/followers_and_following/following.html"

# open files
followers = open(followers_file, 'r', encoding="utf-8")
following = open(following_file, 'r', encoding="utf-8")

# list of followers
myFollowers = []

#parse followers
follower_soup = BeautifulSoup(followers, 'html.pa 3rser')
follower_links = follower_soup.find_all('a')
for link in follower_links:
	myFollowers.append(link['href'])

# print followers line by line
#for line in myFollowers:
#	print(line)

# List of following
myFollowing = []

# Parse following
following_soup = BeautifulSoup(following, 'html.parser')
following_links = following_soup.find_all('a')
for link in following_links:
	myFollowing.append(link['href'])

# print following line by line
#for line in myFollowing:
#	print(line)

# convert lists to sets for efficient set operations
followers_set = set(myFollowers)
following_set = set(myFollowing)


# nodes in myFollowing that does not exist in myFollowers: AKA people who do not follow me
nodes_not_in_followers = following_set - followers_set

'''
# Print the result
print("Nodes in myFollowing that do not exist in myFollowers (People who don't follow me):")
for node in nodes_not_in_followers:
    print(node)

'''

print("People that I don't follow:")
not_following = followers_set - following_set
for node in not_following:
	print(node)


#close opened files
followers.close()
following.close()


# the ratio of more followers vs less following is just articifial clout, man