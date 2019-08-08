#!/usr/local/bin/python3

'''
  Hera, a basketball statistics tracker

  Tracks (per quarter):
    - Kick outs
    - Passes: swing passes, skip passes, perimeter passes,
      low post passes, mid post passes, high post passes,
      outlet passes, hand-offs, cross court passes, lobs,
      , dump offs, short corner passes, and miscellaneous passes
    - Paint touches
    - Points
'''

# Libraries
import os
import sys
import getopt
import keyboard
import errno
import signal

# Globals
KEYBIND_POSSESSION = "enter"
KEYBIND_QUARTER = "q"
KEYBINDS = {  "u": "Kick Outs",
              "s": "Swing Passes",
              "k": "Skip Passes",
              "e": "Perimeter Passes",
              "l": "Low Post Passes",
              "m": "Mid Post Passes",
              "h": "High Post Passes",
              "o": "Outlet Passes",
              "f": "Hand-offs",
              "c": "Cross Court Passes",
              "l": "Lobs",
              "d": "Dump Offs",
              "r": "Short Corner Passes",
              "l": "Miscellaneous Passes",
              "p": "Paint Touches",
              "1": "Points",
              "2": "Points",
              "3": "Points" }

'''
  Usage function

  @param exit code
'''
def usage(exitCode = 0):
  print('''Usage: hera.py [OPTION]...
  
  Options:
          -f  FILENAME
              Filename to output the csv output (required)
          -h  USAGE
  '''.format(os.path.basename(sys.argv[0])), sys.stderr)
  sys.exit(exitCode)

'''
  Signal Integer (Control-C) handler

  @param signal
  @param frame
'''
def handleSigInt(signal, frame):
  print("\nHera terminated")
  exit(0)

'''
  Removes plurality from a string

  Example:
    dogs -> dog
    passes -> pass

  Only handles 's' and 'es'

  @param string
'''
def removePlurality(string):
  if string.endswith("es"):
    string = string[:-2]
  elif string.endswith("s"):
    string = string[:-1]

  return string

'''
  Prints a statement that the given
  keybind was pressed

  @param key
'''
def alertPressedKeys(key):
  print("\n" + removePlurality(key) + " recorded")

'''
  Alerts that the key was pressed
  and then, increments the key
  in the Dictionary of key and integers;
  if the key is of type 'Points', then
  it will append to a List

  @param map
  @param key
'''
def add(map, key):
  alertPressedKeys(KEYBINDS[key])

  if KEYBINDS[key] == "Points":
    if key in map:
      map[key].append(value)
    else:
      map[key] = []
      map[key].append(value)
  else:
    if key in map:
      map[key] += 1
    else:
      map[key] = 1

'''
  Creates a file if does not exist,
  along with the directory structure;
  if the file does exist, will prompt for
  overwrittening the file

  @param filename
'''
def createFile(filename):
  if os.path.exists(filename):
    overwrite = input("File exists, would you like to overwrite (Y or N): ").lower()
    
    while overwrite not in ["y", "n"]:
      overwrite = input("Please input Y or N: ").lower()

    if overwrite == "n":
      exit(0)
  else:
    if os.path.dirname(filename) != "":
      os.makedirs(os.path.dirname(filename), exist_ok=True)
  
  return open(filename, "w")

'''
  Usage function for Hera,
  prints the keybinds for this
  application
'''
def printKeybinds():
  print("Keybinds:")
  
  for keybind in KEYBINDS:
    print("\t" + keybind + ": " + KEYBINDS[keybind])

'''
  Adds headers to the output file
'''
def addHeaders():
  headers = []
  for keybindNames in KEYBINDS.values():
    if keybindNames not in headers:
      headers.append(keybindNames)
  file.write(",".join(headers) + ",Quarter" + "\n")
  file.flush()

'''
  Handles the ENTER keybind,
  signalling a possession change,
  will write the current possession
  to a file and then flush the file

  @param keyboardEvent
'''
def handlePossession(keyboardEvent):
  print("Possession changed")
  global possession 
  
  possessionRow = []
  
  # Appends all current possession attributes
  # and the current quarter to the file
  for keybindKey in KEYBINDS.keys():
    if keybindKey in possession:
      possessionRow.append(str(possession[keybindKey]))
    else:
      possessionRow.append("0")

  file.write(",".join(possessionRow) + "," + str(quarter) + "\n")
  file.flush()

  possession = {}

'''
  Handles the quarter changing,
  will increment the quarter

  @param keyboardEvent
'''
def handleQuarter(keyboardEvent):
  global quarter
  print("\nQuarter: " + str(quarter))
  quarter += 1

'''
  Handles all other keybinds;
  simply adds it to the current
  possession dictionary

  @param keyboardEvent
'''
def handleKeybind(keyboardEvent):
  keybind = keyboardEvent.name
  add(possession, keybind)

'''
  Main application function,
  handles the creation of the file,
  and the binding of the keyboard
  press listeners

  @param filename
'''
def run(filename):
  # Create the file as global
  # so that the keyboard press
  # handlers may access them
  global file
  file = createFile(filename)

  # Adds headers to the created
  # file
  addHeaders()

  # Show the available keybinds to
  # the user
  printKeybinds()

  # Create global possession
  # object so that all handlers
  # may access it
  global possession
  possession = {}

  # Create global quarter integer
  # so that all handlers may access it
  global quarter
  quarter = 1

  # Bind the KEYBIND_POSSESSION to its handler
  keyboard.on_release_key(KEYBIND_POSSESSION, handlePossession)

  # Bind the KEYBIND_QUARTER to its handler
  keyboard.on_release_key(KEYBIND_QUARTER, handleQuarter)

  # Bind all other keybinds
  for keybind in KEYBINDS:
    keyboard.on_release_key(keybind, handleKeybind)

  # while True:
  keyboard.wait()

# Main Execution
if __name__ == '__main__':
  filename = None

  try:
    options, arguments = getopt.getopt(sys.argv[1:], "f:h")
  except getopt.GetoptError as e:
    usage(1)
  
  for option, value in options:
    if option == "-f":
      filename = value
    elif option == "-h":
      usage(0)

  # Filename is required
  if filename is None:
    usage(1)

  # Will handle SIGINTS
  signal.signal(signal.SIGINT, handleSigInt)

  run(filename)