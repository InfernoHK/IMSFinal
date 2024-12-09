import os
from sys import stdout
from getkey import getkey, keys
from ansi.color import fg
from ansi import cursor
import random
global menu_sys_list 
menu_sys_list = []




def menu(choices):


  global pos
  pointer = fg.boldblue('>')
  for choice in choices:
    print(choice)
  print(cursor.hide()+cursor.up()*(len(choices))+pointer, end='    ')
  stdout.flush()

  pos = 1
  while 1:
    key = getkey()
    text = f'{""} {choices[pos-1]}'
    if (key == '\x1b[A' or key == 'w') and pos > 1:
      pos -= 1
      print(f'\r{text}\r' + cursor.up() + pointer + \
            fg.bold(f'{""} {choices[pos-1]}'), end = '      ')
    elif (key == '\x1b[B' or key == 's') and pos < len(choices):
      pos += 1
      print(f'\r{text}\r' + cursor.down() + pointer + \
            fg.bold(f'{""} {choices[pos-1]}'), end = '    ')
    elif key == '\n':
      print(cursor.down()*(len(choices)-pos)+cursor.show())
      return pos
    elif key.isdecimal():
      number = int(key)
      if 0 < number <= len(choices):
        print(cursor.down()*(len(choices)-pos)+cursor.show())
        return number
    stdout.flush()