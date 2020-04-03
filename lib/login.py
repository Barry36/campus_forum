from lib import notification
def user_login(self):
    print("If you haven't registered yet, enter register now!")
    username = input("Username: ")
    password = input("Password: ")

    if username == "register":
      self.register_or_login()
    # check if password is correct
    self.cursor.execute("SELECT count(*), account_ID, lastLoginTime FROM Account where account_Name = '%s'  and password = '%s' group by account_ID, lastLoginTime;" % (username, password))
    cursor_fetch_result = self.cursor.fetchall()

    if len(cursor_fetch_result) !=0 and cursor_fetch_result[0][0] != 0: 
      print("Your have logged in your account!")
      
      # user logged in, get the userID and lastLoginTime
      user_info = { "id": cursor_fetch_result[0][1], "name": username, "lastLoginTime": cursor_fetch_result[0][2] }
      
      # update user last login time
      self.cursor.execute("UPDATE Account SET lastLoginTime = CURRENT_TIMESTAMP WHERE Account.account_ID = '%s';" % user_info["id"])
      self.dbconnection.commit()
     
      # show posts since user last login
      notification.update_notification(self,user_info)
      self.logged_in(user_info)
    else:
      print("Sorry, your username or password is wrong.")
      user_login(self)