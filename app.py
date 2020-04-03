from lib import thumb,group,user,tag,notification,post
import mysql.connector

class PyMedia:
  
  # constructor method
  def __init__(self):
    self.connect_db()

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
      self.executeScriptsFromFile("./create_database.sql")
    self.cursor.execute("USE socialNetwork;")
  
  def login_or_register(self):
    cmd1 = input("Please input command 'login' or 'register', 'exit' to quit (no space): ")
    if cmd1 == "login":
      self.login()
    elif cmd1 == "register":
      self.register()
    elif cmd1 == "exit":
      exit()
    else:
      print("Wrong command.")
      self.login_or_register()

  def register(self):
    print("Please create your username and password.")
    username = input("Username: ")
    
    # check if username exist
    self.cursor.execute("SELECT count(*) FROM Account where account_Name = '%s';" % username)
    valid_username = self.cursor.fetchall()
    
    if valid_username != [(0,)]:
      print("This username already exists. Please choose another username")
      self.register()
    # else
    password = input("Password: ")
    
    # register the acount
    self.cursor.execute("INSERT INTO Account ( account_Name, password ) VALUES ( '%s', '%s' );" % (username, password))
    self.dbconnection.commit()
    
    print("You have successfully registered your account! Thank you!")
    self.login_or_register()

  def login(self):
    username = input("Username: ")
    password = input("Password: ")
    
    # @TODO: check if user exists in Account table:
    # self.cursor.execute("SELECT count(*) FROM Account where account_Name = '%s';" % (username))
    # cursor_check_username_result = self.cursor.fetchall()
    # for x in range(len(cursor_check_username_result)):
    #   print(cursor_check_username_result[x])
    # if cursor_check_username_result[x][0] == 0:
    #   print("This username is invalid! Please try again")
    # self.login()

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
      self.login()

  def logged_in(self, user_info):
    
    print("Please enter a command, type 'help' to see a list of commands.")
    command = input("Command: ")

    # Post activities, including comment and thumbup/thumbdown
    if command == "view all posts" or command == "vap":  # view all posts
      post.view_all_posts(self,user_info) 
    elif command == "view posts" or command == "vp":  # view post by userID
      post.view_posts(self,user_info) 
    elif command == "create post" or command == "cp": # create post
      post.create_post(self,user_info) 
    elif command == "create comment" or command == "cc": # create comment
      post.create_comment(self,user_info) 
    elif command == "thumbup post" or command == "up":  # thumb up a post
      thumb.thumbup(self, user_info) 
    elif command == "thumbdown post" or command == "down":  # thumb down a post
      thumb.thumbdown(self, user_info)
    
    # Group activities
    elif command == "show groups" or command == "sg": # show existing groups
      group.show_all_groups(self,user_info)
    elif command == "create group" or command == "cg":  # create group
      group.create_group(self,user_info) 
    elif command == "join group" or command == "jg":  # join a group
      group.join_group(self,user_info) 

    # User activities
    elif command == "list all users" or command == "lau":    # show all users
      user.show_all_users(self, user_info) 
    elif command == "list all following users" or command == "lafu":    # show all following users
      user.show_all_users_following(self, user_info) 
    elif command == "follow user" or command == "fu":   # follow users
      user.follow_user(self, user_info) 
    elif command == "unfollow user" or command == "uu":   # unfollow users
      user.unfollow_user(self, user_info) 

    # Tag activities
    elif command == "show all tags" or command == "stag": # show all tags
      tag.show_all_tags(self,user_info) 
    elif command == "show all followed tags" or command == "sftag": # show all tags followed by user
      tag.show_tags_followed_by_user(self, user_info)
    elif command == "follow tags" or command == "ft":     # follow tags
      tag.follow_tag(self,user_info) 
    elif command == "unfollow tags" or command == "ut":   # unfollow tags
      tag.unfollow_tag(self,user_info)
    
    
    # Admin activities
    elif command == "exit" or command == "q":
      exit()
    elif command == "help":
      print('Avaliable commands: view posts(vp), create post(cp), \n thumbup post(up), thumbdown post(down), \
        \n show groups(sg), join group(jg), \n create group(cg), list all users(lau), \n  show all tags(stag), \
        show all followed tags(sftag), \n follow user(fu), \n follow tags(ft), unfollow user(uu), \n unfollow tag(ut), create post(cp), \
        \n create response(cr)')
    else:
      print("Wrong command, please enter Help to view available commands.")
    self.logged_in(user_info)

    

  def checkValid(self, table, column_id, check_id):
    check_id = int(check_id)
    self.cursor.execute("select count(*) from `%s` where `%s` = %d " % (table, column_id, check_id))
    valid = self.cursor.fetchall()
    return valid


  # util funtions
  def executeScriptsFromFile(self, filename):
      fd = open(filename, 'r')
      sqlFile = fd.read()
      fd.close()
      sqlCommands = sqlFile.split(';')
      for command in sqlCommands:
          self.try_sql_cmd(command)

  def try_sql_cmd(self, cmd):
    try:
        self.cursor.execute(cmd)
    except mysql.connector.Error as err:
        print("SQL error: ", err)
  
  def start_app(self):
    self.connect_db()
    print("Welcome!")
    self.login_or_register()
    
# main method
if __name__ == "__main__":
  app = PyMedia()
  app.start_app()
