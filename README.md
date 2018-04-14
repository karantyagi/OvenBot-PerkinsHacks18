
# PerkinsHacks18 - `Make a Meal`
 
# Introduction
A program to help improve the user experience of the visually impaired when working with home appliances such as Ovens, Microwaves etc. <br/>
@authors: <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Pratyusha Karnati<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;HITESH VERMA<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Max Davidowitz<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Winston Moh T.<br/> </i>
         
@PerkinsHacks

# Table of Contents
[Prerequisites](#prerequisites)<br/>
[Get API Key](#get_api_key)<br/>
[Run the sample application](#run_the_sample_application)<br/>
[Conclusion](#conclusion)<br/>

# <a name="prerequisites"></a>Prerequisites
## Platform requirements
The program was developed for Windows 10, MAC OSX and Python 3.3+.

## Pyttsx text to speech
 * Pytsx is a cross-platform text-to-speech wrapper. <br/>
 * It uses different speech engines based on your operating system: <br/>
 * nsss – NSSpeechSynthesizer on Mac OS X 10.5 and higher <br/>
 * sapi5 – SAPI5 on Windows XP, Windows Vista, and (untested) Windows 7 <br/>
 * espeak – eSpeak on any distro / platform that can host the shared library (e.g., Ubuntu / Fedora Linux) <br/>
 * Here we use the IBM WATSON Text To Speech API SERVICE 

## Install Chocolatey, Python 3+ and pip on System:
check https://chocolatey.org/install and http://docs.python-guide.org/en/latest/starting/install3/win/ for more resources.
### Installing Chocolatey
Chocolatey installs in seconds. You are just a few steps from running choco right now!
1. First, ensure that you are using an administrative shell - you can also install as a non-admin, check out Non-Administrative Installation. <br/>
2. Copy the text specific to your command shell - cmd.exe or powershell.exe. <br/>
 * cmd:
` @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"` <br/>
 * powershell:
` Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))` <br/>
3. Paste the copied text into your shell and press Enter. <br/>
4. Wait a few seconds for the command to complete. <br/>
5. If you don't see any errors, you are ready to use Chocolatey! Type choco or choco -? now. <br/>

Once done, installing Python 3 is very simple, because Chocolatey pushes Python 3 as the default. <br/>
run ` choco install python` <br/>
<br/>
Once you’ve run this command, you should be able to launch Python directly from to the console. (Chocolatey is fantastic and automatically adds Python to your path.)

### Installing pip
The two most crucial third-party Python packages are setuptools and pip, which let you download, install and uninstall any compliant Python software product with a single command. It also enables you to add this network installation capability to your own Python software with very little work.
All supported versions of Python 3 include pip, so just make sure it’s up to date: <br/>
run ` python -m pip install -U pip` on Windows <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; OR <br/>
run ` sudo easy_install pip` on MAC OSX

### Install with pip (using pyenv, pipenv or virtualenv):
` sudo pip install pyttsx`
### Have pip installed and run:
` pip install pywin32 `  (for win32com.client)

# <a name="get_api_key"></a>Get API Key
Subscribe to the Speech Recognition API, and get a free trial subscription key.
The Speech API is part of Cognitive Services (previously Project Oxford). You can get free trial subscription keys from the Cognitive Services subscription page. After you select the Speech API, select Get API Key to get the key. It returns a primary and secondary key. Both keys are tied to the same quota, so you can use either key. <br/>
Enter API KEY in the space for api_key in the code.

# <a name="run_the_sample_application"></a>Run the sample application
After the installing the different libraries, execute the python program.
ex ` python program.py`

# <a name="conclusion"></a>Conclusion
At the end, we were able to know about the services available to visually impaired people, what their feedback was and came up with a way to improve existing products to suit their needs.

