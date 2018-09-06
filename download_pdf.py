# Qui Le
# September 3, 2018
# Download pdf's from the San Jose City Meeting Detail webpage

# imported the sys library
import sys

# imported the os.path module
from os.path import join
# import os module
from os import getcwd 

# imported the pickle library
import pickle

# imported urlopen from the urllib.request library
from urllib.request import urlopen

# Get the second argument on the command line
# which is the name of the file
filename = sys.argv[1]

# path to Folder for downloading
folder = getcwd() + '/DownloadedFiles'

# Read back from storage
f = open(filename, 'rb')

# Load the object from the file
storedlist = pickle.load(f)

# Print out 1st item in storelist
#print(storedlist[0])

counter = 0
for url in storedlist:
	# start counting
	counter += 1
	# open the URL
	website = urlopen(url)
	# open file to write to
	with open(join(folder,'Document_' + str(counter) + '.pdf'), 'wb') as file:
		# write to each document 
		file.write(website.read())
	

