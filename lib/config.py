import mysql.connector
def connect_db(self):
    self.dbconnection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="AQua0917"
    )
    self.cursor = self.dbconnection.cursor(buffered=True)
    self.cursor.execute("select count(*) from information_schema.tables where Table_schema = 'socialNetwork';")
    check_database = self.cursor.fetchall()
    if check_database == [(0,)]:
        executeScriptsFromFile(self, "./create_database.sql")
        executeScriptsFromFile(self, "./populate_sample_data.sql")
    self.cursor.execute("USE socialNetwork;")
  
# helper funtions
def executeScriptsFromFile(self, filename):
      fd = open(filename, 'r')
      sqlFile = fd.read()
      fd.close()
      sqlCommands = sqlFile.split(';')
      for command in sqlCommands:
          try_sql_cmd(self, command)

def try_sql_cmd(self, cmd):
    try:
        self.cursor.execute(cmd)
    except mysql.connector.Error as err:
        print("SQL error: ", err)