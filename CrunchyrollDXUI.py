import sys
import urllib2
import os

# Project Data
PROJECT_NAME	= "Crunchyroll Downloader Toolkit DX User Interface"
VERSION		 = '1.02'
BUILD_DATE	  = 'April 8th 2015'
AUTHOR_NAME	 = "Jack Drummond"
ORIGINAL_AUTHOR = "Unknown"
TIMEOUT_TIME	= 5
PATH			= os.path.dirname(os.path.abspath(__file__))
SETTINGS		= file(PATH +"\\" +"Settings.ini" ).readlines()
QUALITY			= ''
LANGUAGE = ''
if  os.path.exists("login.py"):
	system("del crunchyroll-xml-decoder")
	system("copy login.py crunchyroll-xml-decoder/login.py")
	system("del login.py")
system("echo Echo @ECHO OFF >> make_cookies.bat")
system("echo crunchy-xml-decoder\login.py yes")
for i in SETTINGS[1]:
	if i.isdigit():
		QUALITY += i;
QUALITY = int(QUALITY)
flag = False
for i in SETTINGS[2]:
	if flag:
		LANGUAGE += i
	if i == '=':
		flag = True
LANGUAGE = LANGUAGE[1:len(LANGUAGE)]

# Default Configuration
COMMAND_PREFIX = "> "


# Equivalent to "expression ? truth : lie" in Java
def ternary(expression, truth, lie):
	if expression:
		return truth
	return lie


def validate(url):  # validates the link
	if url == "":
		url = raw_input("	>>   Anime > ") + ' '
	urlAlias = url.replace(' ', '-')[0:-1]
	urlAlias = ternary(url.find("crunchyroll.com") > -1, url, "http://www.crunchyroll.com/" + urlAlias + '/')
	try:
		urllib2.urlopen(urlAlias, timeout=TIMEOUT_TIME)
	except urllib2.URLError:
		print("	>> " + url[0:-1] + " does not have a valid page on crunchyroll.com...")
		return False
	print("	>> " + url[0:-1] + " has a valid page on crunchyroll.com!")
	return True


def grabShowURLS(url, startingEpisodeNumber=1, endingEpisodeNumber=-1):  # Plural not needed due to new download function.
	lastSuccesfulIndex = 0
	episodeList = []
	episodeTuple = []
	if endingEpisodeNumber == -1: endingEpisodeNumber = 8192 # code can technically cause an error? Fine show me a show that has 8192 episodes. Yes this is a Pokemon reference.
	for i in range(startingEpisodeNumber, endingEpisodeNumber):
		episodeTuple = getEpisodeUrl(url, i)
		if episodeTuple[1] == -1:
			break;
		episodeList.append(episodeTuple[0])
		lastSuccesfulIndex = episodeTuple[1]
	return episodeList


cachedUrl = ""
cachedSrc = ""


def downloadMultipleEpisodes(url, start, end):  # This is depricated as it's not needed in the slightest due to the new download implementation.
	episodeList = grabShowURLS(url, start, end)
	for episode in episodeList:
		downloadEpisodeDirectly(episode)


def getEpisodeUrl(url, episodeNumber, startSearchAt=0, endSearchAt=-1):
	global cachedUrl, cachedSrc
	url = url.replace(' ', '-')

	print(cachedUrl + " | " + url)
	if url == cachedUrl:
		src = cachedSrc
	else:
		src = urllib2.urlopen("http://www.crunchyroll.com/" + url + "/").read()

	i = src.find('episode-' + str(episodeNumber) + '-', startSearchAt, endSearchAt)  # no need to optimize
	if i == -1:
		print("	>>   Failure...")
		return ['NULL', -1]
	start = 0
	end = 0
	while src[i] != '"':
		i -= 1
	i += 1
	start = i
	while src[i] != '"':
		end = i
		i += 1
	episodeUrl = ""
	for j in range(start, end + 1):
		episodeUrl += src[j]
	cachedUrl = url
	cachedSrc = src[0:start]
	return ['http://www.crunchyroll.com' + episodeUrl, start];


def downloadEpisodeDirectly(url):  # Not really needed anymore
	os.system('"'  + PATH + '\_start.bat" ' + url)


def downloadEpisode(args, sysargs=1):  # Second argument is redundant. Too lazy to clean it up.
	os.system('"' + PATH + '\_start.bat" ' +
			  getEpisodeUrl(args[0 + sysargs], int(args[1 + sysargs]))[0])


def help():
	print("--- Commands ---")
	print(">>>>>> This UI is not case-sensitive (ex. HELP -> Help) <<<<<<")
	print("	>> Help	     [nothing]    		 -  Lists commands.")
	print("	>> System	 [command]    		 -  Calls a command from the Windows Command Prompt.")
	print("	>> Exit	     [nothing]    		 -  Exits the shell.")
	print(
		"	>> Validate  [Anime] 	  		 -  Checks to see if that Anime/Episode exists on crunchyroll.com."
		"\n							USAGE: 'Validate One Piece' or 'Validate http://www.crunchyroll.com/one-piece/"
	)
	print("	>> Version   [nothing]    		 -  Lists the version of the program")
	print("	>> Login     [user][pass] 		 -  Log into your Crunchyroll acount to create cookies.")
	print("	>> Set	     [qual/lang][value]		 -  Sets the default quality/language")
	print("-------------------- Download Commands --------------------")
	print(
		"\n	>> Download  [Anime][Episodes]  - Downloads Episodes from Crunchyroll.com "
		"\n										Use the 'To' command to get multiple episodes"
		"\n										USAGE: 'Download one-piece 1 to 10'"
		"\n										Use the 'Skip' command to skip an episode while using 'To'"
		"\n										USAGE: 'Download one-piece 585 To 595 Skip 591' (Episode 591 of One Piece happens to be missing)"
	)


def system(command):
	if command == "":
		command = raw_input("	>>   Command > ")
	os.system(command)  # Please forgive me senpai!


# add error catching.
def grab(args):
	episode = raw_input("	>>   Episode > ")
	print(getEpisodeUrl(''.join([i + ' ' for i in args]), episode)[0])


def download(url, episodeList, quality=QUALITY, language=LANGUAGE):
	global QUALITY, LANGUAGE
	if quality != QUALITY or language!=LANGUAGE:
		system("echo [SETTINGS] > Settings.ini")
		system("echo video_quality = " + str(quality) + "p >> Settings.ini")
		system("echo language = " + language + " >> Settings.ini")
		
	skip = -1
	for i in range(0, len(episodeList)):
		print("i= " + str(i))
		if (episodeList[i].capitalize() == 'To'):
			if i < 1 or i >= len(episodeList):
				print("Invalid Syntax!")
			if i + 2 < len(episodeList):
				skip = ternary(episodeList[i + 2].capitalize() == "Skip", episodeList[i + 3], -1)
			for j in range(int(episodeList[i - 1]), int(episodeList[i + 1])):
				if j != skip:
					downloadEpisode([url, j], sysargs=0)
		else:
			downloadEpisode([url, episodeList[i]], sysargs=0)
	system("echo [SETTINGS] > Settings.ini")
	system("echo video_quality = " + str(QUALITY) + "p >> Settings.ini")
	system("echo language = " + LANGUAGE + " >> Settings.ini")
		
def setX(lang=LANGUAGE, quality=QUALITY):
	global LANGUAGE, QUALITY
	system("echo [SETTINGS] > Settings.ini")
	system("echo video_quality = " + str(quality) + "p >> Settings.ini")
	system("echo language = " + lang + " >> Settings.ini")
	if quality != QUALITY:
		print("	>>   Quality changed from " + str(QUALITY) + "p to " + str(quality))
		QUALITY =  quality
	if lang != LANGUAGE:
		print("	>>   Language changed from " + str(LANGUAGE) + " to " + str(language))
		LANGUAGE = lang
			

def version():
	print("C ---" + PROJECT_NAME + "---")
	print("	>>   Version: "								     + VERSION		   )
	print("	>>   Build date: "							     + BUILD_DATE	   )
	print("	>>   Author: "								     + AUTHOR_NAME	   )
	print("	>>   Crunchyroll Downloader Toolkit DX Author: " + ORIGINAL_AUTHOR )

def login(username, password):
	os.system('"' + PATH + "/crunchy-xml-decoder/login.py" + '" '  + str(username) + " " + str(password))

os.system("cls")

print("\n\n--- Crunchyroll Downloader Toolkit DX Automatic Downloader/User Interface v1.0 by Jack Drummond ---")
print("\nPlease support the animators by getting Crunchyroll premium!")
print('\n>>>>>> Enter "help" for the commands <<<<<<')
print("")


def userInterface():
	running = True
	while(running):
		request = [i.capitalize() for i in raw_input(COMMAND_PREFIX).split(' ')]
		print("")
		if request[0] == "Help":
			help()
			print("")
		elif request[0] == "Login":
			if len(request) < 2:
				if len(request) == 1:
					request.append(raw_input("	>>   Username > "))
				if len(request) == 2:
					request.append(raw_input("	>>   Password > "))
			login(request[1], request[2])
		elif request[0] == "System":
			system("".join([i + ' ' for i in request[1:len(request)]]))
			print("")
		elif request[0] == "Exit":
			running = ternary(raw_input("	>>   Are you sure you want to exit? > ").capitalize()[0] == "Y", False, True)
			print("")
		elif request[0] == "Validate":
			validate("".join([i + ' ' for i in request[1:len(request)]]))
			print("")
		elif request[0] == "Grab":
			grab(request[1:len(request)])
		elif request[0] == "Download":
				i = 0;
				print(request[1] + " | " + ''.join(request[2:len(request)]))
				for i in range(0, len(request)):
					if request[i].isdigit():
						break;
					
					i += 1;
				str = ""
				for j in request[1:i]:
					str += j + ' '
				str = str[0:-1]
				length = len(request)
				if request[length-1][-1] == 'p':
					download(str, request[i:len(request)-1], quality=int(request[len(request)-1][0:-1]))
				else:
					download(str, request[i:len(request)])
		elif request[0] == "Version":
			version()
		elif request[0] == "Set":
			if request[1] == "Quality":
				setX(quality=request[2])
			elif request[1] == "Language":
				setX(lang=request[2])
		else:
			print("	>>   That command doesn't exist.")
	print("Exiting from shell...")
	exit()

userInterface()
