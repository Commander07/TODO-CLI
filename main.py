"""
TODO-CLI is a simple tool for managing todo list and more using a
user friendly ui/cli.

License: MIT License
Author: https://commander07.cf
"""
import os
import time
import keyboard
import yaml

import colors

CHECKMARK = "✔"
X = "✖"
DOT = "•"
LIST_FORMAT = "%DOT% %name% %finished%"
HIGHLIGHT = colors.CYAN
TASKS_FILE = "data/tasks.yml"


class Task:
  """
  The 'Task' class is the class which stores information about a task and
  methods to change and get value along with formating task list text.
  """
  def __init__(self, name, desc=None, finished=False):
    self.name = name
    self.desc = desc
    self.finished = finished

  def toggle(self):
    """
    Uncomplete and complete the task
    """
    self.finished = not self.finished

  def rename(self, name):
    """
    Rename the task
    """
    self.name = name

  def set_desc(self, desc):
    """
    Sets the description of the task.
    """
    self.desc = desc

  def get_desc(self):
    """
    Return the description of the task
    """
    return self.desc

  def get_finished(self):
    """
    Checks if a task is completed and returns the correct color and symbol
    to use
    """
    if not self.finished:
      return f"{colors.RED}{X}{colors.RESET}"
    return f"{colors.GREEN}{CHECKMARK}{colors.RESET}"

  def __str__(self):
    format_ = LIST_FORMAT.replace("%DOT%", DOT).replace("%name%", self.name)
    return format_.replace("%finished%", self.get_finished())

  def __repr__(self):
    return self.__str__()


def get_color(button_idx, idx):
  """
  Takes the current index and a index of a button and if it
  matches it returns the correct HIGHLIGHT color.
  """
  if idx == button_idx:
    return HIGHLIGHT
  return colors.RESET


def menu(idx, tasks):
  """
  Main menu
  """
  os.system("cls")
  end = 0
  for i, task in enumerate(tasks):
    print(get_color(i, idx) + task.__str__())
    end = i + 1
  print(get_color(end, idx) + "[Add new task]")
  print(get_color(end + 1, idx) + "[Exit]")


def edit(task, tasks):
  """
  Shows a menu that lets you edit the selected task.
  """
  idx = 0
  end = 2

  def _menu():
    os.system("cls")
    print("Editing", task.name, "!")
    print(get_color(end - 2, idx) + "[Change name]")
    print(get_color(end - 1, idx) + "[Change description]")
    print(get_color(end, idx) + "[Back]")
  _menu()
  while True:
    _menu()
    time.sleep(0.1)
    key = keyboard.read_key(False)
    if key in ('w', keyboard.KEY_UP):
      if idx > 0:
        idx -= 1
    elif key in ('s', keyboard.KEY_DOWN):
      if idx < end:
        idx += 1
    elif key == "enter":
      if idx == end - 1:
        name = ""
        os.system("cls")
        print("Task description: ", end="", flush=True)
        while True:
          time.sleep(0.1)
          key = keyboard.read_key(False)
          if key == "backspace":
            name = name[:-1]
            os.system("cls")
            print("Task name:", name, end="", flush=True)
          elif key == "space":
            name += " "
            print(" ", end="", flush=True)
          elif len(key) > 1:
            pass
          elif key == "enter":
            break
          else:
            print(key, end="", flush=True)
            name += key
        task.setDesc(name)
        open(TASKS_FILE, "w").write(yaml.dump(tasks))
      elif idx == end - 2:
        name = ""
        os.system("cls")
        print("Task name: ", end="", flush=True)
        while True:
          time.sleep(0.1)
          key = keyboard.read_key(False)
          if key == "backspace":
            name = name[:-1]
            os.system("cls")
            print("Task name:", name, end="", flush=True)
          elif key == "space":
            name += " "
            print(" ", end="", flush=True)
          elif len(key) > 1:
            pass
          elif key == "enter":
            break
          else:
            print(key, end="", flush=True)
            name += key
        task.rename(name)
        open(TASKS_FILE, "w").write(yaml.dump(tasks))
      elif idx == end:
        open(TASKS_FILE, "w").write(yaml.dump(tasks))
        show_more(task, tasks)
        break


def show_more(task, tasks):
  """
  Creates the info menu for tasks thats shows options and more info.
  """
  idx = -1
  end = 2

  def _menu():
    os.system("cls")
    print(task.name)
    if task.desc:
      print(task.desc)
    print(get_color(end - 3, idx) + "[Delete]")
    print(get_color(end - 2, idx) + "[Mark]")
    print(get_color(end - 1, idx) + "[Edit]")
    print(get_color(end, idx) + "[Back]")
  while True:
    _menu()
    time.sleep(0.1)
    key = keyboard.read_key(False)
    if key in ('w', keyboard.KEY_UP):
      if idx > -1:
        idx -= 1
    elif key in ('s', keyboard.KEY_DOWN):
      if idx < end:
        idx += 1
    elif key == "enter":
      if idx == end - 2:
        task.toggle()
      elif idx == end - 3:
        tasks.remove(task)
        open(TASKS_FILE, "w").write(yaml.dump(tasks))
        main()
        break
      elif idx == end - 1:
        edit(task, tasks)
        break
      elif idx == end:
        open(TASKS_FILE, "w").write(yaml.dump(tasks))
        main()
        break


def main():
  """
  Main function for the todo app which starts the main menu and load tasks
  """
  tasks = yaml.load(open(TASKS_FILE), Loader=yaml.Loader)
  idx = 0
  end = 2
  while True:
    menu(idx, tasks)
    time.sleep(0.1)
    key = keyboard.read_key(False)
    if key in ('w', keyboard.KEY_UP):
      if idx > 0:
        idx -= 1
    elif key in ('s', keyboard.KEY_DOWN):
      if idx < end + 1:
        idx += 1
    elif key == "enter":
      if idx == end:
        name = ""
        os.system("cls")
        print("Task name: ", end="", flush=True)
        while True:
          time.sleep(0.1)
          key = keyboard.read_key(False)
          if key == "backspace":
            name = name[:-1]
            os.system("cls")
            print("Task name:", name, end="", flush=True)
          elif key == "space":
            name += " "
            print(" ", end="", flush=True)
          elif len(key) > 1:
            pass
          elif key == "enter":
            break
          else:
            print(key, end="", flush=True)
            name += key
        tasks.append(Task(name))
        open(TASKS_FILE, "w").write(yaml.dump(tasks))
      elif idx == end + 1:
        open(TASKS_FILE, "w").write(yaml.dump(tasks))
        print(colors.RESET)
        raise SystemExit
      else:
        show_more(tasks[idx], tasks)
        break


main()
