class AppContext:
    def __init__(self):
        self.main_page = None
        self.current_user = None
        self.users = dict()
        pass

context = AppContext()