def register(self):
    print("Please create your username and password.")
    username = input("Username: ")
    
    # check if username exist
    self.cursor.execute("SELECT count(*) FROM Account where account_Name = '%s';" % username)
    valid_username = self.cursor.fetchall()
    
    if valid_username != [(0,)]:
      print("This username already exists. Please choose another username")
      register()
    # else
    password = input("Password: ")
    
    # register the acount
    self.cursor.execute("INSERT INTO Account ( account_Name, password ) VALUES ( '%s', '%s' );" % (username, password))
    self.dbconnection.commit()
    
    print("You have successfully registered your account! Thank you!")
    self.register_or_login()