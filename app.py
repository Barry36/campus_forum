from lib import config,login,resigeration,thumb,group,user,tag,post
import mysql.connector

class socialNetwork:
  
  # constructor method
  def __init__(self):
    config.connect_db(self)

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

  
  def start_app(self):
    config.connect_db(self)
    print("Welcome!")
    self.register_or_login()
    
# main method
if __name__ == "__main__":
  app = socialNetwork()
  app.start_app()
