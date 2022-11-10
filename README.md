# Voice Assistant

This project, as the name implies, is a console voice assistant. I wrote it to work in my native language - Polish. It recognizes speech, converts it into text, and carries out spoken commands. Using many libraries (bs4, ecapture, webbrowser, wikipedia, speech_recognition, Pyttsx3, and more...), it creates, searches for or executes queries, and informs the user about everything in speech.
#### What can the assistant do?
- Using the API of Polish weather stations, it responds live and provides synoptic data for the requested city in Poland
- Taking advantage of a website with Polish jokes, the program selects a random joke each time to make the user laugh.
- When asked to take a picture, the program takes it and saves it in a folder.
- Directly finds and opens the desired Spotify music or YouTube videos.
- Provides the current date and time.
- Most of all, it answers **EVERY** question (whether you want to know how to cook curry chicken or who is Equatorial Guinea's finance minister) by selecting the first search result and scraping the most relevant content from those results.

## Installation

In order for the program to work, you need to install the following libraries:

```bash
pip install ecapture
pip install PyAudio
pip install SpeechRecognition
pip install wikipedia
pip install pyttsx3
pip install beautifulsoup4
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
