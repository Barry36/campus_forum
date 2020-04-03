import mysql.connector

class myClass:
    def __init__(self):
        self.connect_db()
    def connect_db(self):
        self.dbconnection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="AQua0917"
    )
        self.cursor = self.dbconnection.cursor(buffered=True)
        self.cursor.execute("USE socialNetwork;")
        self.cursor.execute("SELECT count(*) FROM Account where account_Name = 'bawang2';")
        valid_username = self.cursor.fetchall()

        for i in range(len(valid_username)):
            print(valid_username[i][0])
        if valid_username != [(0,)]:
            print("This username already exists")
        else:
            print("hey")
    def start_app(self):
        self.connect_db()
        self.login_or_register()
# main method
if __name__ == "__main__":
  app = myClass()
#   app.start_app()