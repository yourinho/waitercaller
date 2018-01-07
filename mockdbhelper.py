# We'll create a MockDBHelper class again and also create a con guration
# le to indicate that this should be used locally when we test our
# application and don't have access to the database. It needs to have a
# function that takes a username and password and checks whether these
# exist in the database and are associated with each other.

# This dect acts as the database storage.
#MOCK_USERS = {'test@example.com': '123456'}
MOCK_USERS = [{"email": "test@example.com",
               "salt": "8Fb23mMNHD5Zb8pr2qWA3PE9bH0=",
               "hashed": "1736f83698df3f8153c1fbd6ce2840f8aace4f200771a46672635374073cc876cf0aa6a31f780e576578f791b5555b50df46303f0c3a7f2d21f91aa1429ac22e"}]


class MockDBHelper:

    def get_user(self, email):
        user = [x for x in MOCK_USERS if x.get("email") == email]
        if user:
            return user[0]
        return None

    def add_user(self, email, salt, hashed):
        MOCK_USERS.append({"email": email, "salt": salt, "hashed": hashed})

    def print_users(self):
        for x in MOCK_USERS:
            print(x.get('email'))
