# WORK IN PROGRESS
# 
# Hacker News - Who Is Hiring Tracker
#
# Y Combinator's Hacker News has a monthly "Who Is Hiring" thread. However,
# there is no option to sort the job postings on that thread by time posted.
# As a result, it's _very_ easy to miss new job postings. This script aims
# to solve that problem.
#
# Author:  Kevin Dong (https://www.github.com/kevindong)
# License: MIT License
# Date:    October 5, 2016
# Source:  https://github.com/kevindong/HackerNews-WhoIsHiringTracker

# ================
# INSERT URL BELOW
url = "https://news.ycombinator.com/item?id=12627852"
# INSERT URL ABOVE
# ================

import requests
import json
import os
import time
from sys import exit
from HTMLParser import HTMLParser

print("Please note that VERY little testing has been done on this script.\n")

print("Attempting to download page... "),
page = requests.get('https://hacker-news.firebaseio.com/v0/item/' + url.split('?id=')[1] + '.json')
if page.status_code != 200:
	print("Error")
	exit(1)
else:
	print("Done")

print("Attempting to save downloaded page... ")
if not (os.path.exists('HN_WhoIsHiring')):
	print("\tThe \"HN_WhoIsHiring\" directory was not found. Creating now...")
	os.makedirs("HN_WhoIsHiring")
currentTime = time.strftime("%Y%m%d_at_%H%M%S")
webpageFile = open("HN_WhoIsHiring/" + currentTime + '.json', 'w')
webpageFile.write(page.text.encode('utf8'))
webpageFile.close()
print("\tDone writing to: " + currentTime + '.json')

print("Attempting to parse downloaded page... ")
webpageFile = open("HN_WhoIsHiring/" + currentTime + '.json', 'r')
rawJson = json.loads(webpageFile.read())
webpageFile.close()
posts = rawJson["kids"]
posts.sort()
parsedFile = open("HN_WhoIsHiring/" + currentTime + '.txt', 'w')
parsedFile.write('\n'.join(str(x) for x in posts))
parsedFile.close()
print("\tDone writing to: " + currentTime + '.txt')

print("Detecting if previous runs exist...")
jobsDirectory = os.listdir("HN_WhoIsHiring")
jobsDirectory.sort()
for item in jobsDirectory:
	if (('.txt' not in item) or ('diff' in item)):
		jobsDirectory.remove(item)
if (len(jobsDirectory) > 1):
	print("\tAssumed this program has been previously run...")
else:
	print("\tAssumed this program has not been previously run...")
	exit(0)

print("Attempting to open previous record: " + jobsDirectory[-2] + '...'),
previousJobsFile = open("HN_WhoIsHiring/" + jobsDirectory[-2], 'r')
print("Done\n\n")

print("Parsing previous record now...")
previousJobsList = [int(line.rstrip('\n')) for line in previousJobsFile]
newJobs = []
for item in posts:
	if item not in previousJobsList:
		newJobs.append(item)
if len(newJobs) == 0:
	print("No new jobs were detected. :(")
	os.remove("HN_WhoIsHiring/" + currentTime + '.txt')
	os.remove("HN_WhoIsHiring/" + currentTime + '.json')
	print("The files generated during this run were deleted.");
else:
	print("The following jobs are new: ")
	diffFile = open("HN_WhoIsHiring/" + currentTime + '.diff.html', 'w')
	h = HTMLParser()
	for item in newJobs:
		print(item)
		link = 'https://news.ycombinator.com/item?id=' + str(item)
		diffFile.write('<a href=\"' + link + '\">' + link + '</a></br>')
		jobDownload = requests.get('https://hacker-news.firebaseio.com/v0/item/' + str(item) + '.json')
		jobJson = json.loads(jobDownload.text)
		if ('text' in jobJson):
			diffFile.write((h.unescape(jobJson['text']) + '</br>').encode('utf8'))
			diffFile.write('=' * 80 + '</br>')
		else:
			print(str(jobJson['id']) + " was deleted.</br>")
	print("Each of those jobs has been saved to: " + "HN_WhoIsHiring/" + currentTime + '.diff.txt')
	print("\nHappy job hunting!")
