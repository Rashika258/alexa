import speech_recognition as sr, pyttsx3, pywhatkit, wikipedia, pyjokes, webbrowser,requests,PyPDF2,json
from googlesearch.googlesearch import GoogleSearch
from GoogleNews import GoogleNews
from datetime import datetime


# listen to microphone so create listener object
listener = sr.Recognizer()

# initialise text to speech converter
engine = pyttsx3.init()

#Voice selection
voices = engine.getProperty('voices')  # getting details of current voice
engine.say("If you need a male voice assisatant press 'm' else 'f' ")
engine.runAndWait()
gender = input().lower()
if gender == 'm':
	engine.setProperty('voice', voices[0].id)  # changing index, changes voices. o for male
elif gender == 'f':
	engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female
else:
	engine.say("Please enter a valid choice")
	engine.runAndWait()


# Naming ceremony
engine.say("Hiii, I am your voice assistant. Please give me a name")
engine.runAndWait()
name = input()

# set rate and volume
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.say('You can change my speech rate by giving a number')
engine.runAndWait()
r = int(input())
engine.setProperty('rate', r)     # setting up new voice rate


volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.say("You can adjust my volume levels between 0 and 1")
engine.runAndWait()
v = float(input())
engine.setProperty('volume',v)    # setting up volume level  between 0 and 1

# function for assistant to talk
def talk(text):
	engine.say(text)
	engine.runAndWait()

# Input to assisstant using microphone
def take_command():
	try:
		# sr is speech recognition module
		with sr.Microphone() as source:
			print("listening")
			engine.say("Hii Rashika, I am listening.....")
			engine.runAndWait()
			voice = listener.listen(source)
			command = listener.recognize_google(voice)
			command = command.lower()
			if name in command:
				engine.say("Hiiii, I am your " + name + "     You said" + command)
				engine.runAndWait()
				command = command.replace(name,'')
				print(command)
	except:
		engine.say("Rashika,  Please talk again I couldn't hear you")
		engine.runAndWait()
	return command

def run_alexa():
	command = take_command()
	print(command)
	if  'music' in command:
		song = command.replace('play song', '')
		talk('I am playing your favourite ' +song)
		# print('playing')
		print(song)
		# playing the first video that appears in yt search
		pywhatkit.playonyt(song)

	elif 'time' in command:
		now = datetime.now()
		time = now.strftime("%H:%M:%S")
		print("time:", time)
		talk("Current time is " +time)

	elif ('month' or 'year') in command:
		now = datetime.now()
		year = now.strftime("%Y")
		print("year:", year)
		talk("Current year is  " + year)
		month = now.strftime("%m")
		print("month:", month)
		talk("Current month is  " + month)

	elif 'date' in command:
		now = datetime.now()
		date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
		print("date and time:", date_time)
		talk("Current date and time is " + date_time)

	# opens web.whatsapp at specified time i.e before 10 minutes and send the msg
	elif 'whatsapp' in command:
		talk("To which number do you have to whatsapp")
		talk("Please dont forget to enter 10 digits with country code")
		num = input()
		talk("Enter the message you have to send")
		msg = input()
		talk("Enter the time to send the message")
		time = int(input())
		pywhatkit.sendwhatmsg(num, msg, time,00)
		pywhatkit.showHistory()
		pywhatkit.shutdown(3000000000)
		# pywhatkit.sendwhatmsg("+919876543210", "This is a message", 15, 00)

	# Convert text to handwritten format
	elif 'convert' in command:
		text = command.replace('convert', '')
		pywhatkit.text_to_handwriting(text, rgb=[0, 0, 0])

	# Perform google search
	elif 'search' in command:
		key = command.replace('search', '')
		pywhatkit.search("key")

	elif 'wikipedia' in command:
		person = command.replace('wikipedia','')
		talk("How many pages do you want to read")
		num_pages = int(input())
		# talk("In which language do you want to read")
		# l = input()
		# wikipedia.set_lang(l)
		info = wikipedia.summary(person, num_pages)
		print(info)
		talk(info)

	elif 'can you work for me' in command:
		talk ("sorry, I have headache. Please do your work")

	elif 'are you single' in command:
		talk ("I am in relationshhip with wifi")

	elif 'joke' in command:
		talk(pyjokes.get_joke())
		talk("sorry for the lamest joke")

	elif  'open google browser' in command:
		try:
			urL = 'https://www.google.com'
			chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
			webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
			webbrowser.get('chrome').open_new_tab(urL)
			talk("Successfully opened chrome its upto you to search")
		except:
			webbrowser.Error

	elif 'google search' in command:
		word_to_search = command.replace('google search', '')
		response = GoogleSearch().search(word_to_search)
		print(response)
		for result in response.results:
			print("Title: " + result.title)
			talk("You can look for the following titles  " + result.title)

	elif 'weather' in command:
		# base URL
		BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
		talk("Which city weather are you looking for")
		try:
			with sr.Microphone() as source:
				print('listening weather...')
				city_voice = listener.listen(source)
				city = listener.recognize_google(city_voice)
				# city = '\"'+city.lower()+'\"'

				print(city)
				# city="bangalore"
				# API key API_KEY = "Your API Key"
				API_KEY = "b5a362ef1dc8e16c673dd5049aa98d8f"
				# upadting the URL
				URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
				# HTTP request
				response = requests.get(URL)
				# checking the status code of the request
				if response.status_code == 200:
					# getting data in the json format
					data = response.json()
					# getting the main dict block
					main = data['main']
					# getting temperature
					temperature = main['temp']
					# getting the humidity
					humidity = main['humidity']
					# getting the pressure
					pressure = main['pressure']
					# weather report
					report = data['weather']
					print(f"{CITY:-^30}")
					print(f"Temperature: {temperature}")
					print(f"Humidity: {humidity}")
					print(f"Pressure: {pressure}")
					print(f"Weather Report: {report[0]['description']}")
					talk("Temperature in "+city+ " is "+temperature+" humidity is "+ humidity+ " pressure is "+ pressure +" and your final weather report" +report)
				else:
					# showing the error message
					print("Error in the HTTP request")
					talk("Error in the HTTP request")
		except:
			talk("Hmmmmm, it looks like there is something wrong")

	elif 'news' in command:
		try:
			googlenews = GoogleNews()
			googlenews.set_lang('en')
			# googlenews.set_period('7d')
			# googlenews.set_time_range('02/01/2020', '02/28/2020')
			googlenews.set_encode('utf-8')

			talk("What news are you looking for")
			try:
				with sr.Microphone() as source:
					print('listening news ...')
					news_voice = listener.listen(source)
					news_input = listener.recognize_google(news_voice)
					news_input = news_input.lower()
					print(news_input)
					googlenews.get_news(news_input)
					googlenews.search(news_input)
					googlenews.get_page(2)
					result = googlenews.page_at(2)
					news = googlenews.get_texts()
					print(news)
					talk(news)
			except:
				print("Error")
				talk("Error in reading input")

		except:
			print("No news")
			talk(" I couldn't find any news on this day")

	elif 'play book' or 'read pdf' in command:
		talk("Which pdf do you want me to read")
		book_input = input()
		print(book_input)
		book = open(book_input, 'rb')
		# create pdfReader object
		pdfReader = PyPDF2.PdfFileReader(book)
		# count the total pages
		total_pages = pdfReader.numPages
		total_pages = str(total_pages)
		print("Total number of pages " + total_pages)
		talk("Total number of pages " + total_pages)
		# initialise speaker object
		# speaker = pyttsx3.init()
		# talk("Enter your starting page")
		# start_page = int(input())
		talk(" here are the options for you, you can press 1 to  Play a single page     2 to   Play between start and end points  and  3 to  Play the entire book ")
		talk("Enter your choice")
		choice = int(input())
		if (choice == 1):
			talk("Enter index number")
			page = int(input())
			page = pdfReader.getPage(page)
			text = page.extractText()
			talk(text)
			# speaker.say(text)
			# speaker.runAndWait()
		elif (choice == 2):
			talk("Enter starting page number")
			start_page = int(input())
			talk("Enter ending page number")
			end_page = int(input())
			for page in range(start_page + 1, end_page):
				page = pdfReader.getPage(start_page + 1)
				text = page.extractText()
				talk(text)
				# speaker.say(text)
				# speaker.runAndWait()
		elif (choice == 3):
			for page in range(total_pages + 1):
				page = pdfReader.getPage(page)
				text = page.extractText()
				talk(text)
				# speaker.say(text)
				# speaker.runAndWait()
		else:
			talk("Haha!! Please enter valid choice")
	else:
		talk("Hiii Rashika, I am so bored can you please give me some proper commands")


while True:
    try:
        run_alexa()
    except UnboundLocalError:
        print("No command detected! Alexa has stopped working ")
        break