class AppContext:
    def __init__(self):
        self.main_page = None
        self.current_user = None
        self.users = dict()
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

  def isEmpty(self):
    return len(self.stack) == 0

  def size(self):
    return len(self.stack)
  

nav_history = Stack()
context = AppContext()
