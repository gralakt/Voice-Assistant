from datetime import datetime
import requests
import json
# This module converts text to speech in a program and works offline. 
import pyttsx3
# A module for recognizing speech and converting it into text.
import speech_recognition as speech_r
# This module is used to access information from Wikipedia.
import wikipedia
# This built-in module is used for web search.
import webbrowser
# This module is used for capturing images from camera.
import ecapture as ec	
# Web scraping module.
from bs4 import BeautifulSoup


# Setup webbrowser module
webbrowser.register('google-chrome', 'google-chrome', instance=None, preferred=False)


# Setup pyttsx module
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
# Setting to understand Polish language
engine.setProperty('voice', voices[0].id)


# This function converts the given text into sound
def speak(audio):
	engine.say(audio)
	engine.runAndWait()


# This function converts heard sounds into text
def take_command():
	# Init speech_recognition library
	r = speech_r.Recognizer()

	with speech_r.Microphone() as source:
	# Get and save the words said by the user
		print("Słucham...")
		r.pause_threshold = 1
		audio = r.listen(source)
	try:
	# Try to translate them into text
		print("Przetwarzam...")
		query = r.recognize_google(audio, language='pl')
		print("Użytkownik powiedział:" + query + "\n")
	except Exception as e:
	# Unless something goes wrong then ask for to repeat and return 'None' in string
		print(e)
		speak("Powtórz proszę. Nie zrozumiałem.")
		return "None"
	# Return the user's words written in the text
	return query


if __name__ == '__main__':
	# Inform that the program is running
	speak("Asystent aktywowany.")
	speak("Jak mogę Ci pomóc?")

	while True:

		# Ask the user for a command and reduce it to lowercase
		query = take_command().lower()

		# If the query includes any mention of wikipedia
		if 'wikipedii' in query or 'wikipedia' in query:
			speak("Szukam w Wikipedii ...")
			# Remove the listed expressions from the query
			query = query.replace("wikipedii", "").replace("wikipedia", "").replace("w", "")
			# Set the Wikipedia language to Polish
			wikipedia.set_lang('pl')
			# Find the article related to your query, and save 3 sentences from that article
			results = wikipedia.summary(query, sentences=3)
			# Pass the information found to the user
			speak("Oto co znalazłem...")
			print(results)
			speak(results)

		# If any jokes were mentioned in the query
		elif 'żart' in query or 'dowcip' in query or 'kawał' in query or 'suchar' in query:
			# Go to the joke website and save a random joke from it
			r = requests.get('http://www.dowciplandia.pl/losowe')
			soup = BeautifulSoup(r.text, "html.parser")
			# Do this by searching for the second 'p' element on the page
			results = soup.find_all("p")[1]
			# Tell the user a saved joke
			speak(results)
			print(results)

		# If there are mentions about youtube in the query
		elif 'youtube' in query or "youtubie" in query:
			# Speak opening youtube
			speak("Otwieram Youtube")
			# Remove the listed expressions from the query
			query = query.replace("youtube", "").replace("otwórz", "").replace("włącz", "").replace("na", "").replace("filmik", "").replace("film", "").replace("youtubie", "").replace("jutubie", "")
			# Create url sequences with the given value
			url = 'https://www.youtube.com/results?search_query=' + str(query)
			# Open the created link in the browser
			webbrowser.open(url)

		# If there were any mention of a photo in the query
		elif 'zdjęcie' in query:
			# Get the current date
			now = datetime.now()
			# Using the above date, set a unique name for the png
			save_png = 'assistant_' + str(now.day) + str(now.month) + str(now.year) + str(now.hour) + str(now.minute) + str(now.second) + '.png'
			# Inform the user that the photo will be taken
			speak('Usmiech!')
			# Capture a photo and save it under the prepared name
			ec.capture(0,"frame", str(save_png))

		# If there is a mention of the weather in the query
		elif 'pogoda' in query:
			# Remove the listed expressions from the query and convert some Polish characters to English
			query = query.replace("jaka", "").replace("pogoda", "").replace(" ", "").replace("ó", "o").replace("ń","n")
			# Create url sequences with the city specified in query
			url = 'https://danepubliczne.imgw.pl/api/data/synop/station/' + str(query)
			# Send a request for access the page at this url
			response_API = requests.get(url)
			# If request has not been processed successfully
			if response_API.status_code != 200:
				# Ask the user to repeat the query with the larger city as argument
				speak("Wybierz większe miasto! Nie mamy stacji synoptycznej w wybranym mieście...")
				print('Wybierz większe miasto!')
			# If we got access to the server
			else:
				# Save and transform the received data into a convenient form
				data = response_API.text
				parse_json = json.loads(data)
				# Save the values of the specified keys
				temperature = parse_json['temperatura']
				rainfall = parse_json['suma_opadu']
				# Create a personalized answer depending on the temperature and whether it is raining
				response = ""
				if float(rainfall) > 0.2:
					respone = response + "Przygotuj parasol. Możliwe opady w twoim mieście..."
				if float(temperature) < 0:
					response = response + "Nie wychodź z domu bez herbaty w termosie!"
				elif float(temperature) < 10:
					response = response + "Ubierz kurtkę przed wyjśćiem z domu..."
				elif float(temperature) < 20:
					response = response + "Całkiem ciepło..."
				# Finally, add the number of degrees in celcius to the response
				response = response + "Dziś na zewnątrz " + temperature + " stopni Celcjusza..."
				# Reply to the user
				speak(response)

		# If there is any mention of the music industry in the query
		elif 'puść' in query or 'piosenkę' in query or 'spotify' in query:
			query = query.replace("piosenkę", "").replace("puść", "").replace("na", "").replace("spotify", "")
			speak("Włączam " + str(query) + " na Spotify...")
			url = 'https://open.spotify.com/search/' + query
			webbrowser.open(url)

		# If the user asks for a date or time
		elif 'godzina' in query or 'godzinę' in query or 'dzień' in query or 'data' in query or 'datę' in query:
			# Get the current date and time
			now = datetime.now()
			# Save the answer in a user-friendly format
			response = str(now.day) + '.' + str(now.month) + '.' + str(now.year) + ' , godzina ' + str(now.hour) + ':' + str(now.minute)
			# Reply to the user
			speak(response)
			print(response)

		# If the user thanks the program, the program will reply "to your service!"
		elif 'dziękuję' in query or 'dzięki' in query:
			speak('Do usług!')

		# If the user uses the phrase 'stop' the program will terminate
		elif 'stop' in query:
			speak('Do zobaczenia następnym razem!')
			exit(0)

		# In all other cases, as long as query is not 'none'
		elif query != 'none':
			speak("O to co znalazłem w sieci")
			# Substitute in query the listed expressions with the symbol '+'
			query = query.replace(" ", "+")

			URL = "https://pl.search.yahoo.com/search?p={}".format(query)
			# Get the content behind the created url
			r = requests.get(URL)
			soup = BeautifulSoup(r.text, "html.parser")
			# Find all items belonging to the first search result
			results = soup.find_all(class_="first")
			for result in results:
				# Save the link that has the href attribute
				newURL = result.select_one('a', href=True)
				# If it is correct and exists
				if newURL is not None:
					# Save this item as url to the direct search result
					direct_url_element = result
					# And break the conditional statement
					break
			# In the found element, find the link
			element = direct_url_element.find('a')
			# And save only the direct link to this page
			url = element['href']
			# Open the found page in the user's browser
			webbrowser.open(url)
			# Get the content behind the created url
			r2 = requests.get(url)
			soup2 = BeautifulSoup(r2.text, "html.parser")
			# Find first 'p' element
			results2 = soup.find('p')
			# Present the answer to the user
			print(results2)
			speak(results2)

