class User:

    def __init__(self, email):
        self.email = email

    def get_id(self):
        return self.email

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

        # We only create the user object when the correct username and password
        # combination is entered, so if the user object exists, it'll be
        # authenticated.
    def is_authenticated(self):
        return True
