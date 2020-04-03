from lib import thumb,group,user
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
    if cmd1 == "login" or cmd1 == "lg":
      self.login()
    elif cmd1 == "register" or cmd1 == "rg":
      self.register()
    elif cmd1 == "exit" or cmd1 == "q":
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
     
      # show posts
      self.show_posts(user_info)
      self.logged_in(user_info)
    else:
      print("Sorry, your username or password is wrong.")
      self.login()

  def logged_in(self, user_info):
    
    print("Please enter a command, type 'help' to see a list of commands.")
    command = input("Command: ")

    # Post activities
    if command == "view posts" or command == "vp":  # view post by userID
      self.view_posts(user_info) 
    elif command == "create post" or command == "cp": # create post
      self.create_post(user_info) 
    elif command == "create response" or command == "cr": # create comment
      self.create_response(user_info) 
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
    elif command == "list of users" or command == "lou":    # show all users
      user.show_all_users(self, user_info) 
    elif command == "follow user" or command == "fu":   # follow users
      user.follow_user(self, user_info) 
    elif command == "unfollow user" or command == "uu":   # unfollow users
      user.unfollow_user(self, user_info) 

    # Tag activities
    elif command == " show all tags" or command == "stag":
      self.show_all_tags(user_info) # show all tags
    elif command == "follow tags" or command == "ft":
      self.follow_tag(user_info) # follow tags
    elif command == "unfollow tags" or command == "ut":
      self.unfollow_tag(user_info) # unfollow tags
    
    
    elif command == "exit" or command == "q":
      exit()
    elif command == "help":
      print('Avaliable commands: view posts(vp), create post(cp), \n thumbup post(up), thumbdown post(down), \
        \n show groups(sg), join group(jg), \n create group(cg), list of users(lou), \n  show all tags(stag), \
        follow user(fu), \n follow tags(ft), unfollow user(uu), \n unfollow tag(ut), create post(cp), \
        \n create response(cr)')
    else:
      print("Wrong command, please enter Help to view available commands.")
    self.logged_in(user_info)

  def show_posts(self, user_info):
    command = input("Hi, there are some new posts since you last login. Do you want to see them?(y/n)")
    if command == "y":
      tag_posts_query = "SELECT User_post.post_timestamp, User_post.post_ID FROM \
      (SELECT account_ID, lastLoginTime FROM Account WHERE account_ID = %s) as a \
      INNER JOIN Follow_Tag ON Follow_Tag.account_ID = a.account_ID \
      INNER JOIN Post_Tag ON Follow_Tag.tag_Name = Post_Tag.tag_Name \
      INNER JOIN User_post ON User_post.post_ID = Post_Tag.post_ID;"
      tag_posts_query = tag_posts_query % user_info["id"]
      self.cursor.execute(tag_posts_query)
      tag_posts_query_result = self.cursor.fetchall()

      follow_posts_query = \
      "SELECT User_post.post_timestamp, User_post.post_ID, a.account_ID, Follower.account_ID as followed_ID FROM \
      (SELECT account_ID, lastLoginTime FROM Account WHERE account_ID = %s) as a \
      INNER JOIN Follower ON Follower.follower_ID = a.account_ID \
      INNER JOIN User_post ON User_post.account_ID = Follower.account_ID;"
      follow_posts_query = follow_posts_query % user_info["id"]
      self.cursor.execute(follow_posts_query)
      follow_posts_query_result = self.cursor.fetchall()

      filtered_tag_posts = list(filter(lambda x: x[0] > user_info["lastLoginTime"], tag_posts_query_result))
      print("Posts from tags you have followed: ")
      if len(filtered_tag_posts) == 0:
        print("No new post.")
      for row in filtered_tag_posts:
        self.cursor.execute("select post_ID, message, thumbs, is_read from User_post where '%s' = User_post.post_ID;" % row[1])
        tag_post_message = self.cursor.fetchall()
        print("Post_ID: ", tag_post_message[0][0])
        print("Message: ", tag_post_message[0][1])
        print("Thumbs: ", tag_post_message[0][2])
        print("Is_read: ", tag_post_message[0][3])
        print("\n")
        self.cursor.execute("UPDATE User_post SET is_read = 1 WHERE '%s' = User_post.post_ID;" % row[1])
        self.dbconnection.commit()
      
      filtered_follow_posts = list(filter(lambda x: x[0] > user_info["lastLoginTime"], follow_posts_query_result))
      print("Posts from people you have followed: ")
      if len(filtered_follow_posts) == 0:
        print("No new post.")
      for row in filtered_follow_posts:
        self.cursor.execute("select post_ID, message, thumbs, is_read from User_post where '%s' = User_post.post_ID;" % row[1])
        follow_post_message = self.cursor.fetchall()
        print("Post_ID: ", follow_post_message[0][0])
        print("Message: ", follow_post_message[0][1])
        print("Thumbs: ", follow_post_message[0][2])
        print("Is_read: ", follow_post_message[0][3])
        print("\n")
        self.cursor.execute("UPDATE User_post SET is_read = 1 WHERE '%s' = User_post.post_ID;" % row[1])
        self.dbconnection.commit()

    elif command == "n":
      pass
    else:
      print("Wrong command. Please enter y or n.")
      self.show_posts(user_info)
    

  def checkValid(self, table, column_id, check_id):
    check_id = int(check_id)
    self.cursor.execute("select count(*) from `%s` where `%s` = %d " % (table, column_id, check_id))
    valid = self.cursor.fetchall()
    return valid

  def view_posts(self, user_info):
    postID = input("Enter the post ID you would like to view: ")
    validPost = self.checkValid("user_post", "post_ID", postID)
    if validPost == [(0,)]:
      print("That is an invalid postID")
    else:
      self.cursor.execute("select post_ID, message, thumbs, is_read from User_post where '%s' = User_post.post_ID;" % postID)
      post_message = self.cursor.fetchall()
      print("Post_ID: ", post_message[0][0])
      print("Message: ", post_message[0][1])
      print("Thumbs: ", post_message[0][2])
      print("Is_read: ", post_message[0][3])
      self.cursor.execute("UPDATE User_post SET is_read = 1 WHERE '%s' = User_post.post_ID;" % postID)
      self.dbconnection.commit()
    self.logged_in(user_info)



  def show_all_tags(self, user_info):
    self.cursor.execute("SELECT * from Post_Tag") # list of all tags
    show_tags = self.cursor.fetchall()
    i = 0
    while(i < len(show_tags)):
        print("Tag Name:", show_tags[i][0], "; Tagged Post ID:", show_tags[i][1])
        i += 1

  def follow_tag(self, user_info):
    tagName = input("Enter the name of the tag you wish to follow: ")
    self.cursor.execute("INSERT INTO Follow_Tag ( tag_Name, account_ID ) VALUES ( '%s', '%s' );" % (tagName, user_info["id"]))
    self.dbconnection.commit()
    print("Success!")
    self.logged_in(user_info)

  def unfollow_tag(self, user_info):
    tagName = input("Enter the name of the tag that you wish to unfollow: ")
    user_ID = int(user_info["id"])
    self.cursor.execute("select count(*) from Follow_Tag where Follow_Tag.tag_Name = '%s' and Follow_Tag.account_ID = %d" % (tagName, user_ID))
    validFollow = self.cursor.fetchall()
    if validFollow == [(0,)]:
      print("You are not followed to this tag")
    else:
      self.cursor.execute("DELETE FROM Follow_Tag where Follow_Tag.tag_Name = '%s' and Follow_Tag.account_ID = %d;" % (tagName, user_ID))
      self.dbconnection.commit()
      print("Success!")
    self.logged_in(user_info)

  def create_post(self, user_info):
    post_content = input("What content would you like to post? ")
    create_post_query = "insert into User_post(account_ID, message, thumbs, is_read) values (%s, '%s', %s, %s);"
    create_post_query = create_post_query % (user_info["id"], post_content, 0, 0)
    self.cursor.execute(create_post_query)
    post_id = self.cursor.lastrowid

    post_tags = input("What tags do you want to put? Seperate your tags with space. ")
    post_tags = set(post_tags.split())
    for post_tag in post_tags:
      create_tag_query = "insert into Post_Tag(tag_name, post_ID) values ('%s', %s);"
      create_tag_query = create_tag_query % (post_tag, post_id)
      self.cursor.execute(create_tag_query)

    self.dbconnection.commit()
    print("You have successfully created a post!")
    self.logged_in(user_info)
  
  def create_response(self, user_info):
    parent_ID = input("Which post ID would you like to reply to? ")
    validPost = self.checkValid("user_post", "post_ID", parent_ID)
    if validPost == [(0,)]:
      print("That is an invalid post ID")
    else:
      response_content = input("What is your reply message? ")
      account_ID = int(user_info["id"])
      parent_ID = int(parent_ID)
      self.cursor.execute("INSERT INTO User_post (account_ID, message, parent_ID) VALUES (%d, '%s', %d );" % (account_ID, response_content, parent_ID))
      self.dbconnection.commit()
      print("Success!")

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
