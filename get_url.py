# September 2, 2018
# Qui Le
# Using module re to get href attribute of tag <a></a>

from bs4 import BeautifulSoup
from urllib.request import urlopen
# imported the requests library
import requests
import sys
# imported the re library
import re
# imported the pickle library
import pickle

# CONSTANT
gov_site = "https://sanjose.legistar.com/"

# This function will take a parameter which is the url (string type)
# And return a list of all the tags <a></a> in the html doc 
def get_list_of_tag_a(url):
	# Create HTTP response object
	page = requests.get(url)
	# Construct a BeautifulSoup object
	soup = BeautifulSoup(page.content, 'html.parser')
	# Find all <a></a> tags within the nested data structure of BeautifulSoup object
	tag_list = soup.find_all('a')

	return tag_list

# Go through the list of anchor tags
# Find href with 'View.ashx' and 'LegislationDetail.aspx'
def find_wanted_href(the_tag_list):
	View_list = []
	Legislation_list = []
	for tag in the_tag_list:
		match1 = re.search('View.ashx[\w;=\?\&-]+', str(tag))
		if match1:
			View_list.append(match1.group())

		match2 = re.search('LegislationDetail.aspx[\w;=\?\&-]+', str(tag))
		if match2:
			Legislation_list.append(match2.group())
	return View_list, Legislation_list

# This function fixes the incorrect href
# Returns a correct href
def remove(href_string):
	# We remove substring "amp;" within href
	new_string = href_string.replace("amp;", "")
	# Concatenate two string to create the desired url
	wanted_url = gov_site + new_string
	return wanted_url

# START OF SCRIPT
# Ask the user for the link to the webpage
web_link = input('Enter the url for the webpage: ')

# Call get_list_of_tag_a function 
anchor_tags = get_list_of_tag_a(web_link)

# Unpacking the tuple returned by find_wanted_href function
incorrect_View_href, incorrect_Legislation_href = find_wanted_href(anchor_tags)

# Always len(incorrect_View_href) == 1 because there is one pdf for the agenda of the meeting
# List of new urls found on the first webpage
Legislation_url = []


# If there are more links (Legislation_href is nonempty),
# Need to go into each link and get href for each attachment on these webpages
if len(incorrect_Legislation_href): # len(Legislation_href) > 0 => True (There are more links)
									
	# Iterate through the list of incorrect href, fix each href,
	# make new url, 
	for href in incorrect_Legislation_href:
		# Append each new url to the Legislation_url
		Legislation_url.append(remove(href))

	for url in Legislation_url:
		more_anchor_tags = get_list_of_tag_a(url)
		href_for_View, href_for_Legislation = find_wanted_href(more_anchor_tags)
		incorrect_View_href.extend(href_for_View) 
		#print("Number of pdfs in incorrect_View_href: ", len(incorrect_View_href)) 
		# This line of code above tells how many more href were added to incorrect_View_href

# Below is a test to see total of href 
#print("-------------------------------")	
#print("Number of pdfs to be downloaded: ", len(incorrect_View_href))

# Once you have the list of incorrect View href ready
# Need to remove "amp;" in each href, also
list_of_pdf_url = []
for href in incorrect_View_href:
	new_url = remove(href)
	list_of_pdf_url.append(new_url)

# name of the file where we will store the object
pdflistfile = "pdflist.data"
# Write to the file
f = open(pdflistfile, 'wb')
# Dump the object to a file
pickle.dump(list_of_pdf_url, f)
f.close()

