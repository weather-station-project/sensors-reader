class Controller(object):
    """Base class for controllers"""

    def __init__(self, server, database, user, password):
        self.server = server
        self.database = database
        self.user = user
        self.password = password

    def execute(self):
        raise NotImplementedError('A sub-class must be implemented.')
