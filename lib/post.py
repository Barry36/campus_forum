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
      show_posts(self, user_info)