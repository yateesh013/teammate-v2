import pymysql
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.getenv("host")
DB_NAME = os.getenv("db")
DB_USER = os.getenv("user")
DB_PASSWORD = os.getenv("password")
DB_PORT=os.getenv("port")


connection = pymysql.connect(
  db=DB_NAME,
  host=DB_HOST,
  password=DB_PASSWORD,
  port=int(DB_PORT),
  user=DB_USER,
)

def connect():
    if not connection.open:
        connection.ping(reconnect=True)


#default function
def create_default():
    connect()
    f=connection.cursor()
    query1 = "CREATE TABLE IF NOT EXISTS registration (mail VARCHAR(255) UNIQUE PRIMARY KEY, name VARCHAR(255),  password VARCHAR(255), contact VARCHAR(20))"
    query2 = "CREATE TABLE IF NOT EXISTS projects (name VARCHAR(255) PRIMARY KEY, domain VARCHAR(255), teamsize INT, techused TEXT, brief TEXT, user VARCHAR(255))"
    f.execute(query1)
    f.execute(query2)
    connection.commit()
    connection.close()
#user functions
def check_user(mail,password=0,login=False):
    connect()
    f=connection.cursor()
    query=f"select mail,password from registration where mail='{mail}'"
    f.execute(query)
    data=f.fetchall()
    connection.commit()
    connection.close()
    if not login and len(data)==0:
        return True
    elif login and len(data)!=0:
        if password ==data[0][1]:
            return True
    else:
        return False 

def add_user(data):
    connect()
    name=data["name"]
    mail=data["mail"]
    password=data["password"]
    contact=data["contact"]
    #connection=s3.connect()
    f=connection.cursor()
    verify=check_user(mail)
    if not verify:
        return False
    else:
        if not connection.open:
            connection.ping(reconnect=True)
        query, values = "INSERT INTO registration (mail, name ,password, contact) VALUES (%s, %s, %s, %s)", (mail,name, password, contact)
        f.execute(query, values)
        connection.commit()
        connection.close()
        return True

#projects functions
def check_project(name):
    #connection=s3.connect()
    connect()
    f=connection.cursor()
    query=f"select * from projects where name='{name}'"
    f.execute(query)
    data=f.fetchall()
    connection.commit()
    connection.close()
    if len(data)==0:
        return True
    else:
        return False

def add_project(data):
    #connection=s3.connect()
    connect()
    f=connection.cursor()
    check=check_project(data[0])
    if not check:
        return False
    try:
        if not connection.open:
            connection.ping(reconnect=True)

        query = "INSERT INTO projects (name, domain, teamsize, techused, brief, user) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (data[0],data[3],data[2],data[1],data[4],data[5])  # Convert list to tuple
        f.execute(query, values)
        connection.commit()
        connection.close()
        return True
    except:
        return False
    
def get_projects(mail,name=None,user=True):
    #connection=s3.connect()
    connect()
    f=connection.cursor()
    if user:
        if name is not None:
            query=f"""select * from projects where name='{name}'"""
        else:
            query=f"select * from projects where user ='{mail}'"
    
    else:
        query=f"select * from projects where user !='{mail}'"    
    f.execute(query)
    data=f.fetchall()
    connection.commit()
    connection.close()
    return data

def delete_project(name):
    #connection=s3.connect()
    connect()
    f=connection.cursor()
    query=f"delete from projects where name='{name}'"
    f.execute(query)
    connection.commit()
    connection.close()
    return True

def update_project(data):
    #connection=s3.connect()
    if not connection.open:
        connection.ping(reconnect=True)
    f=connection.cursor()
    query = "UPDATE projects SET domain=%s, teamsize=%s, techused=%s, brief=%s WHERE name=%s"
    values = (data[4], data[3], data[2], data[1], data[0])
    f.execute(query, values)
    connection.commit()
    connection.close()
    return True


#update_project(["teammates","hfdh","3","hgfdhddfe","hello"])

#print(get_projects("yateeshec013@gmail.com",user=False))
#create_default()
#print(add_user("hello","hello@gmail.com","123","8639661731"))
#print(check_user("hello@gmail.com",login=True))
#print(add_project(["p1","ec",3,"skills","hghdrtd","user"]))
#add_user(["p1","yateeshec013@gmail.com","123","565987236"])
#print(check_user("yateeshec013@gmail.com",login=True))
#print(get_projects("yateeshec013@gmail.com",name="p1"))