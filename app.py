from lib import login,resigeration,thumb,group,user,tag,post
import mysql.connector

class socialNetwork:
  
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
      self.executeScriptsFromFile("./populate_sample_data.sql")
      self.dbconnection.commit()
    self.cursor.execute("USE socialNetwork;")
    
    

  def register_or_login(self):
    cmd1 = input("Please input command 'login' or 'register', 'exit' to quit (no space): ")
    if cmd1 == "login":
      login.user_login(self)
    elif cmd1 == "register":
      resigeration.register(self)
    elif cmd1 == "exit":
      exit()
    else:
      print("Wrong command.")
      self.register_or_login()


  def logged_in(self, user_info):
    
    print("Please enter a command, type 'help' to see a list of commands.")
    command = input("Command: ")

    # Post activities, including comment and thumbup/thumbdown
    if command == "view all posts" or command == "vap":  # view all posts
      post.view_all_posts(self,user_info) 
    elif command == "view post" or command == "vp":  # view post by postID
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
      password = input("Admin Password: ")
      if password == "admin":
        user.show_all_users(self, user_info) 
      else: 
        print("Wrong Password contact your admin!")
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
      print("Avaliable commands: \n > view all posts(vap), view post(vp), create post(cp), \n > thumbup post(up), thumbdown post(down), \
        \n > show groups(sg), join group(jg), create group(cg), \n > show all tags(stag), show all followed tags(sftag), follow tags(ft), unfollow tags(ut), \
        \n > list all users(lau), list all following users(lafu), follow user(fu), unfollow user(uu), \
        \n create comment(cr)")
    else:
      print("Wrong command, please enter Help to view available commands.")
    self.logged_in(user_info)

  def checkValid(self, table, column_id, check_id):
    check_id = int(check_id)
    self.cursor.execute("select count(*) from `%s` where `%s` = %d " % (table, column_id, check_id))
    valid = self.cursor.fetchall()
    return valid

  # helper funtions
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
    self.register_or_login()
  

# main method
if __name__ == "__main__":
  app = socialNetwork()
  app.start_app()
