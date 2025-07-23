from enum import Enum,IntEnum
class AppContext:
    def __init__(self):
        self.main_page = None
        self.current_user = None
        self.users = dict()
        self.user_logged_in = False
        pass


class Stack:
  def __init__(self):
    self.stack = []

  def push(self, element):
    self.stack.append(element)

  def pop(self):
    if self.isEmpty():
      return None
    return self.stack.pop()

  def peek(self):
    if self.isEmpty():
      return None
    return self.stack[-1]
  
  def double_peek(self):
    if len(self.stack) < 2:
      return None
    return self.stack[-2]

  def isEmpty(self):
    return len(self.stack) == 0

  def size(self):
    return len(self.stack)


nav_history = Stack()
context = AppContext()
