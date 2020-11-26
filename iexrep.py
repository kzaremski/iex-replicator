#!/usr/bin/env python

# Konstantin Zaremski
# IEX Replicator

# Import requirements
import datetime
from termcolor import colored
from time import sleep
import configparser
import urllib.request
import json
import sys
import os

# Console logging function
def log(message, type = "default"):
  # Colors corresponding to the type of message
  typeColors = {
    "default": "white",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "info": "cyan"
  }
  # Output console log
  print(colored("[ " + str(datetime.datetime.now().strftime("%Y-%m-%d T%H:%M:%S"))  + " ]", "white", "on_blue") + "[ " + colored(type.upper().rjust(7), typeColors[type]) + " ]  " + message)

# Download and parse index
def dlIndex(apikey):
  log("Beginning download of symbol index from IEX")
  try:
    response = urllib.request.urlopen("https://" + ("cloud" if apikey[0:3] == "pk_" or apikey[0:3] == "sk_" else "sandbox") + ".iexapis.com/stable/ref-data/symbols?token=" + apikey)
    data = response.read()
  except:
    log("Unable to download symbol index from IEX", "error")
    return False
  else:
    log("Successfully downloaded symbol index from IEX", "success")
    # Removing escape characters that might mess up json parsing from a slice of the returned string that excludes useless chars at the beginning and the end
    allSymbols = json.loads(str(data).replace("\\", "")[2:-1])
    log("Found " + str(len(allSymbols)) + " supported symbols", "info")
    symbols = []
    # Go through the array of all the symbols and add the (cs/common stock), (ps, preferred stock), and (et, ETF) symbols to a new array
    for symbol in allSymbols:
      if symbol["type"] in ["cs", "ps", "et"]:
        symbols.append(symbol["symbol"])
    log(str(len(symbols)) + " symbols are ETFs, Common Stock, or Preferred stock", "info")
    log("Writing symbol index to drive in JSON format at './data/allsymbols.json'")
    # Make a new data folder if it does not exist
    if not os.path.exists('data'):
      os.makedirs('data')
    try:
      # Convert the list to a string and put it into the allsymbols.json file in the root of the data directory
      file = open('./data/allsymbols.json', 'w')
      file.write(json.dumps(symbols))
      file.close()
    except:
      log("Unable to write symbol index, make sure that you have write permissions", "error")
      return False
    else:
      log("Successfully wrote symbol index to drive", "success")
      return symbols

def main():
  print(colored(" /// IEX Replicator \\\\\\ ", "white", "on_blue"))
  config = configparser.ConfigParser()
  # Load the API key from the config file, otherwise notify and quit
  try:
    config.read("config.ini")
    apikey = config["iexcloud"]["apikey"]
  except:
    log("Unable to read configuration for IEX Cloud api key in config.ini", "error")
    log("Exiting...")
    return
  else:
    log("Loaded API key for IEX Cloud from config.ini", "success")
    log("API key: " + apikey[0:3] + (len(apikey[3:25]) * "*") + apikey[25:], "info")
  # Download a current list of available symbols
  symbolList = dlIndex(apikey)
  if not symbolList: return


if __name__ == "__main__":
  main()