# Deneyap-Kart-Web-Agent

This project is made for https://deneyapkart.org/deneyapkart/deneyapblok/

It uses arduino-cli to interact  with Deneyap Kart/Mini.

Basically  this program uses websockets to connect websites front end communicates with it, parses information and utilizes arduino-cli.

Can be modified for other hardware like esp32 and Arduino.

Front-end code is in blockWebsocket.js file.

Following functionalities are implemented:

    Compiling Code
    Uploading Code
    Changing Upload Options
    Serial Monitor
    Serial Write
    Adding library
    Changing Core Version


I did this project solo, so don't mind commit names, lol

## How To Run
You can basically download .exe from last release or

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.
```bash
pip install -r requirements
```
then
```bash
python main.py
```