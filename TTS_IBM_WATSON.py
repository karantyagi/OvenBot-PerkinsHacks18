### Text to speech
# Pyttsx text to speech
# Pytsx is a cross-platform text-to-speech wrapper.
# It uses different speech engines based on your operating system:
# nsss – NSSpeechSynthesizer on Mac OS X 10.5 and higher
# sapi5 – SAPI5 on Windows XP, Windows Vista, and (untested) Windows 7
# espeak – eSpeak on any distro / platform that can host the shared library (e.g., Ubuntu / Fedora Linux)

# Install with pip (using pyenv, pipenv or virtualenv):
#
# sudo pip install pyttsx

# Have pip installed and run
# pip install pywin32  (for win32com.client)

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")
speak.Speak("Fuck This is a demo to call microsoft text to speech service in Python.")
