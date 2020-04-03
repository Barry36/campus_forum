def view_all_posts(self, user_info):
    self.cursor.execute("select post_ID, message, thumbs, is_read from User_post;")
    query_res = self.cursor.fetchall()
    if len(query_res) == 0:
        print("There is no posts yet!")
    else:
        for e in query_res:
            print("Post_ID: ", e[0])
            print("Message: ", e[1])
            print("Thumbs: ", e[2])
            print("Is_read: ", e[3])
            print("\n")
    print("---------------- The End of All Posts ----------------------")
    self.logged_in(user_info)
def view_posts(self, user_info):
    postID = input("Enter the post ID you would like to view: ")
    validPost = self.checkValid("user_post", "post_ID", postID)
    if validPost == [(0,)]:
      print("This is an invalid postID")
    else:
      self.cursor.execute("select post_ID, message, thumbs, is_read from User_post where '%s' = post_ID;" % postID)
      post_message = self.cursor.fetchall()
      print("Post_ID: ", post_message[0][0])
      print("Message: ", post_message[0][1])
      print("Thumbs: ", post_message[0][2])
      print("Is_read: ", post_message[0][3])
      self.cursor.execute("UPDATE user_post SET is_read = 1 WHERE '%s' = post_ID;" % postID)
      self.dbconnection.commit()
    self.logged_in(user_info)

def create_post(self, user_info):
    post_content = input("What messages would you like to post? ")
    create_post_query = "insert into user_post(account_ID, message, thumbs, is_read) values (%s, '%s', %s, %s);"
    create_post_query = create_post_query % (user_info["id"], post_content, 0, 0)
    self.cursor.execute(create_post_query)
    post_id = self.cursor.lastrowid

    post_tags = input("What tags do you want to add? Seperate your tags with space. ")
    post_tags = set(post_tags.split())
    for post_tag in post_tags:
      create_tag_query = "insert into Post_Tag(tag_name, post_ID) values ('%s', %s);" % (post_tag, post_id)
      self.cursor.execute(create_tag_query)

    self.dbconnection.commit()
    print("-----------------------------------------")
    print("Success! You have created a post!")
    print("-----------------------------------------")
    self.logged_in(user_info)
  
def create_comment(self, user_info):
    parent_ID = input("Which post would you like to comment on? Please enter post_ID ")
    validPost = self.checkValid("user_post", "post_ID", parent_ID)
    if validPost == [(0,)]:
      print("That is an invalid post ID")
    else:
      response_content = input("Wanna comment something? ")
      account_ID = int(user_info["id"])
      parent_ID = int(parent_ID)
      self.cursor.execute("INSERT INTO User_post (account_ID, message, parent_ID) VALUES (%d, '%s', %d );" % (account_ID, response_content, parent_ID))
      self.dbconnection.commit()
      print("-----------------------------------------")
      print("Success! You have created a comment!")
      print("-----------------------------------------")