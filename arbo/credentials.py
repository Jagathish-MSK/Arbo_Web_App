from pymongo import MongoClient
import ssl
client = MongoClient("mongodb+srv://admin:admin@cluster0.vil4a.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl_cert_reqs = ssl.CERT_NONE)
db = client.get_database('arbo_db')
table = db.registration_details

def name_check(name):
    query = {'name': name}
    total_names = table.find(query)
    for x in total_names:
        temp = x
        if temp['name'] == name:
            return True
        else:
            return False

def email_check(email):
    query = {'email': email}
    total_emails = table.find(query)
    for x in total_emails:
        temp = x
        if temp['email'] == email:
            return True
        else:
            return False

def login_validate(user_name, password):
    query = {'name': user_name, 'password': password}
    total_names = table.find(query)
    for x in total_names:
        temp = x
        if temp['name'] == user_name and temp['password'] == password:
            return True
    else:
        return False

def register(name, email, password):
    collection = {'name': name, 'email': email, 'password': password}
    table.insert_one(collection)
    return True
