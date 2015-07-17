__author__ = 'Jeremy'


class ManagerBean:
    def __init__(self, manager_model):
        self.name = manager_model.name
        self.userName = manager_model.user_name
        self.token = manager_model.token