# We'll create a MockDBHelper class again and also create a con guration
# le to indicate that this should be used locally when we test our
# application and don't have access to the database. It needs to have a
# function that takes a username and password and checks whether these
# exist in the database and are associated with each other.

import datetime

# This dect acts as the database storage.

MOCK_USERS = [{"email": "test@example.com",
               "salt": "8Fb23mMNHD5Zb8pr2qWA3PE9bH0=",
               "hashed": "1736f83698df3f8153c1fbd6ce2840f8aace4f200771a46672635374073cc876cf0aa6a31f780e576578f791b5555b50df46303f0c3a7f2d21f91aa1429ac22e"}]

MOCK_TABLES = [{"_id": "1",
                "number": "1",
                "owner": "test@example.com",
                "url": "mockurl"}]

MOCK_REQUESTS = [{"_id": "1",
				  "table_number": "1",
				  "table_id": "1",
				  "time": datetime.datetime.now()}]


class MockDBHelper:

    def get_user(self, email):
        user = [x for x in MOCK_USERS if x.get("email") == email]
        if user:
            return user[0]
        return None

    def add_user(self, email, salt, hashed):
        MOCK_USERS.append({"email": email, "salt": salt, "hashed": hashed})

    def add_table(self, number, owner):
        MOCK_TABLES.append({"_id": number, "number": number, "owner": owner})
        return number

    def update_table(self, _id, url):
    	for table in MOCK_TABLES:
    		if table.get("_id") == _id:
    			table["url"] = url
    			break

    def delete_table(self, table_id):
    	for i, table in enumerate(MOCK_TABLES):
    		if table.get("_id") == table_id:
    			del MOCK_TABLES[i]
    			break

    def get_tables(self, owner_id):
    	return MOCK_TABLES

    def get_table(self, table_id):
    	for table in MOCK_TABLES:
    		if table.get("_id") == table_id:
    			return table

    def add_request(self, table_id, time):
    	table = self.get_table(table_id)
    	MOCK_REQUESTS.append({"_id": table_id,
    						  "owner": table.get("owner"),
    						  "table_number": table.get("number"),
    						  "table_id": table_id,
    						  "time": time})
    	return True

    def delete_request(self, request_id):
    	for i, req in enumerate(MOCK_REQUESTS):
    		if req.get("_id") == request_id:
    			del MOCK_REQUESTS[i]
    			break

    def get_requests(self, owner_id):
    	return MOCK_REQUESTS

    def print_users(self):
        for x in MOCK_USERS:
            print(x.get('email'))
