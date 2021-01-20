import colors
import os
import time
import keyboard
import yaml
checkmark = "✔"
x = "✖"
dot = "•"
listFormat = "%dot% %name% %finished%"
highlight = colors.cyan
tasksFile = "data/tasks.yml"
end = 0


class Task:
  def __init__(self, name, desc=None, finished=False):
    self.name = name
    self.desc = desc
    self.finished = finished

  def toggle(self):
    self.finished = not self.finished

  def rename(self, name):
    self.name = name

  def setDesc(self, desc):
    self.desc = desc

  def getDesc(self):
    return self.desc

  def getFinished(self):
    if not self.finished:
      return f"{colors.red}{x}{colors.reset}"
    else:
      return f"{colors.green}{checkmark}{colors.reset}"

  def __str__(self):
    return listFormat.replace("%dot%", dot).replace("%name%", self.name).replace("%finished%", self.getFinished())

  def __repr__(self):
    return self.__str__()


def getColor(buttonIDX, idx):
  if idx == buttonIDX:
    return highlight
  else:
    return colors.reset


def menu(idx, tasks):
  global end
  os.system("cls")
  end = 0
  for i in range(len(tasks)):
    print(getColor(i, idx) + tasks[i].__str__())
    end = i + 1
  print(getColor(end, idx) + "[Add new task]")
  print(getColor(end + 1, idx) + "[Exit]")


def edit(task, tasks):
  idx = 0
  end = 2

  def _menu():
    os.system("cls")
    print("Editing", task.name, "!")
    print(getColor(end - 2, idx) + "[Change name]")
    print(getColor(end - 1, idx) + "[Change description]")
    print(getColor(end, idx) + "[Back]")
  _menu()
  while True:
    _menu()
    time.sleep(0.1)
    key = keyboard.read_key(False)
    if key == "w" or key == keyboard.KEY_UP:
      if idx > 0:
        idx -= 1
    elif key == "s" or key == keyboard.KEY_DOWN:
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
          if key == "enter":
            break
          elif key == "backspace":
            name = name[:-1]
            os.system("cls")
            print("Task name:", name, end="", flush=True)
          elif key == "space":
            name += " "
            print(" ", end="", flush=True)
          elif len(key) > 1:
            pass
          else:
            print(key, end="", flush=True)
            name += key
        task.setDesc(name)
        break
      elif idx == end - 2:
        name = ""
        os.system("cls")
        print("Task name: ", end="", flush=True)
        while True:
          time.sleep(0.1)
          key = keyboard.read_key(False)
          if key == "enter":
            break
          elif key == "backspace":
            name = name[:-1]
            os.system("cls")
            print("Task name:", name, end="", flush=True)
          elif key == "space":
            name += " "
            print(" ", end="", flush=True)
          elif len(key) > 1:
            pass
          else:
            print(key, end="", flush=True)
            name += key
        task.rename(name)
      elif idx == end:
        open(tasksFile, "w").write(yaml.dump(tasks))
        showMore(task, tasks)
        break


def showMore(task, tasks):
  idx = -1
  end = 2

  def _menu():
    os.system("cls")
    print(task.name)
    if task.desc:
      print(task.desc)
    print(getColor(end - 3, idx) + "[Delete]")
    print(getColor(end - 2, idx) + "[Mark]")
    print(getColor(end - 1, idx) + "[Edit]")
    print(getColor(end, idx) + "[Back]")
  while True:
    _menu()
    time.sleep(0.1)
    key = keyboard.read_key(False)
    if key == "w" or key == keyboard.KEY_UP:
      if idx > -1:
        idx -= 1
    elif key == "s" or key == keyboard.KEY_DOWN:
      if idx < end:
        idx += 1
    elif key == "enter":
      if idx == end - 1:
        edit(task, tasks)
        break
      elif idx == end - 2:
        task.toggle()
      elif idx == end - 3:
        tasks.remove(task)
        open(tasksFile, "w").write(yaml.dump(tasks))
        main()
        break
      elif idx == end:
        open(tasksFile, "w").write(yaml.dump(tasks))
        main()
        break


def main():
  tasks = yaml.load(open(tasksFile), Loader=yaml.Loader)
  idx = 0
  while True:
    menu(idx, tasks)
    time.sleep(0.1)
    key = keyboard.read_key(False)
    if key == "w" or key == keyboard.KEY_UP:
      if idx > 0:
        idx -= 1
    elif key == "s" or key == keyboard.KEY_DOWN:
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
          if key == "enter":
            break
          elif key == "backspace":
            name = name[:-1]
            os.system("cls")
            print("Task name:", name, end="", flush=True)
          elif key == "space":
            name += " "
            print(" ", end="", flush=True)
          elif len(key) > 1:
            pass
          else:
            print(key, end="", flush=True)
            name += key
        tasks.append(Task(name))
        open(tasksFile, "w").write(yaml.dump(tasks))
      elif idx == end + 1:
        open(tasksFile, "w").write(yaml.dump(tasks))
        print(colors.reset)
        raise SystemExit
      else:
        showMore(tasks[idx], tasks)
        break


main()
