import mysql.connector

class myClass:
    def __init__(self):
        #  self.connect_db()
        self.test()
    def connect_db(self):
        self.dbconnection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="AQua0917"
    )

       
        query = "select * from information_schema.tables where Table_schema = 'socialNetwork';"
        self.cursor = self.dbconnection.cursor(buffered=True)
        self.cursor.execute(query)
        check_database = self.cursor.fetchall()
        for x in range(len(check_database)):
            print(check_database[(0,)])

        if check_database == [(0,)]:
            self.executeScriptsFromFile("./create_database.sql")
        self.cursor.execute("USE socialNetwork;")
        # if check_database == [(0,)]:
        #     print("yoo")
        # else:
        #     print("hey")

    def start_app(self):

        self.connect_db()
        self.login_or_register()
    def test(self):
        postID = 123
        print(("Success! You have thumbed up the post: %s ") % str(postID))
# main method
if __name__ == "__main__":
  app = myClass()
#   app.start_app()