from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
from urllib.parse import parse_qs
from passlib.hash import bcrypt

import json
import sys

from todoitems_db import ToDoDB
from sessions import SessionStore

gSessionStore = SessionStore()

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
            self.loadSession()
            self.send_response(200)
            self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

    def end_headers(self):
        self.sendCookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)
        

    def loadCookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()
        
    def sendCookie(self):
        for morsel in self.cookie.values():
            self.send_header("SET-Cookie", morsel.OutputString())

    def loadSession(self):
        self.loadCookie()
        if "sessionId" in self.cookie:
            # session id found in the cookie
            sessionId = self.cookie["sessionId"].value
            self.session = gSessionStore.getSessionData(sessionId)
            if self.session == None:
                # sessionid no longer found in session store
                # create new session
                sessionId = gSessionStore.createSession()
                self.session = gSessionStore.getSessionData(sessionId)
                self.cookie["sessionId"] = sessionId
        else:
            # no session id found in cookie
            # create a brand new session id 
            sessionId = gSessionStore.createSession()
            self.session = gSessionStore.getSessionData(sessionId)
            self.cookie["sessionId"] = sessionId

    def handleSessionCreate(self):
        length = self.headers["Content-length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        parsed_body = parse_qs(body)

        email = parsed_body["email"][0]
        password = parsed_body["password"][0]

        db = ToDoDB()
        user = db.getUserByEmail(email)

        if user == None:
            self.handle401()
            self.end_headers()
        else:
            if bcrypt.verify(password, user["password"]):
                self.session["userid"] = user["uid"]
                self.send_response(201)
                self.end_headers()
            else:
                self.handle401()

    def isLoggedIn(self):
        if "userid" in self.session:
            return True
        else:
            return False

    def handleToDoList(self):

        if self.isLoggedIn():
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            db = ToDoDB()
            todoitems = db.getAllToDoItems()
            self.wfile.write(bytes(json.dumps(todoitems), "utf-8"))
        
        else:
            self.handle401()

    def handleToDoCreate(self):
        if self.isLoggedIn():

            length = self.headers["Content-length"]

            body = self.rfile.read(int(length)).decode("utf-8")
            print("the text body:", body)
            # gives you a dictionary of that string
            parsed_body = parse_qs(body)
            print("the parsed body:", parsed_body)

            item = parsed_body["item"][0]
            # date = parsed_body["date"][0] this is a to do item
            print(item)

            db = ToDoDB()
            db.createToDoList(item) #date to do here
            self.send_response(201)
            self.end_headers()
        else:
            self.handle401()

    def handleUserCreate(self):
        length = self.headers["Content-length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        print("the body", body)
        parsed_body = parse_qs(body)
        print("the parsed body", parsed_body)

        print("creating")

        fname = parsed_body["fname"][0]
        lname = parsed_body["lname"][0]
        email = parsed_body["email"][0]
        password = parsed_body["password"][0]
        encrypted_password = bcrypt.hash(password)
        # print()

        db = ToDoDB()
        user = db.getUserByEmail(email)
        if user != None:
            self.send_response(422)
            self.end_headers()
           
        else:
            db.createUser(fname, lname, email, encrypted_password)
            self.send_response(201)
            self.end_headers()
        
        


    def handleToDoItemsRetrieve(self, id):
        if self.isLoggedIn():
            db = ToDoDB()
            item = db.getTodo(id)
            if item == None:
                self.handleNotFound()
            else:
                self.send_response(200)
                # all headers go here:
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(item), "utf-8"))
        else:
            self.handle401()

            return

    def handle401(self):
        self.send_response(401)
        self.end_headers()

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found", "utf-8"))

    def handleTodoitemDelete(self, id):
        db = ToDoDB()
        item = db.retrieveTodoitem(id)

        if item == None:
            self.handleNotFound()
        else:
            db.deleteTodoitem(id)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes ("Item deleted", "utf-8"))

    def handleTodoitemupdate(self, id):
        length = self.headers["Content-length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        print("the text body:", body)

        parsed_body = parse_qs(body)
        print("the parsed body:", parsed_body)
        # print("this is the item", item)

        item = parsed_body["item"][0]

        db = ToDoDB()
        thing = db.getTodo(id)

        if thing == None:
            self.handleNotFound()
        else:
            db.updateToDoList(item, id)
            # item = db.getToDo(id)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(thing), "utf-8"))

    

    def do_GET(self):
        self.loadSession()
        parts = self.path.split('/')[1:]
        collection = parts[0]
        if len(parts) > 1:
            id = parts[1]
        else:
            id = None
        if collection == "todoitems":
            if id == None:
                self.handleToDoList()
            else:
                self.handleToDoItemsRetrieve(id)
        else:
            self.handleNotFound()


    def do_PUT(self):
        self.loadSession()
        parts = self.path.split('/')[1:]
        collection = parts[0]
        if len(parts) > 1:
            id = parts[1]
        else:
            id = None

        if collection == "todoitems":
            if id == None:
                #if not put collection into handleToDoList()
                self.handleToDoList()
            else:
                self.handleTodoitemupdate(id)
        else:
            self.handleNotFound()


    def do_POST(self):
        self.loadSession()
        if self.path == "/todoitems":
            self.handleToDoCreate()
        elif self.path == "/users":
            self.handleUserCreate()
        elif self.path == "/sessions":
            self.handleSessionCreate()
        else:
            self.handleNotFound()


    def do_DELETE(self):
        self.loadSession()
        splitPath = self.path.split("/")[1:]
        collection = splitPath[0]
        if len(splitPath) > 1 :
            id = splitPath[1]
        else:
            id = None
        if collection == 'todoitems':
            if id == None:
                self.handleNotFound()
            else:
                self.handleTodoitemDelete(id)
        else:
            self.handleNotFound()


def run():
    # listen = ("127.0.0.1", 8080)
    # server = HTTPServer(listen, MyRequestHandler)

    db = ToDoDB()
    db.createUsersTable()
    db.createTodoitemsTable()
    db = None

    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    listen = ("0.0.0.0", port)
    server = HTTPServer(listen, MyRequestHandler)

    print("Server listening on", "{}:{}".format(*listen))
    server.serve_forever()


    # print("Listening...")
    # server.serve_forever()

run()

