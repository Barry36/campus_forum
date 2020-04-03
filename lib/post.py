def show_posts(self, user_info):
    command = input("Hi, there are some new posts since you last login. Do you want to see them?(y/n)")
    if command == "y":
    
    # Following Tags Update
      tag_following_query = "SELECT User_post.post_timestamp, User_post.post_ID FROM \
      (SELECT account_ID, lastLoginTime FROM Account WHERE account_ID = %s) as a \
      INNER JOIN Follow_Tag ON Follow_Tag.account_ID = a.account_ID \
      INNER JOIN Post_Tag ON Follow_Tag.tag_Name = Post_Tag.tag_Name \
      INNER JOIN User_post ON User_post.post_ID = Post_Tag.post_ID;"

      show_update_msg(self, user_info, tag_following_query, "Tag")
      
    # Following User Update
      user_following_query = \
      "SELECT User_post.post_timestamp, User_post.post_ID, a.account_ID, Follower.account_ID as followed_ID FROM \
      (SELECT account_ID, lastLoginTime FROM Account WHERE account_ID = %s) as a \
      INNER JOIN Follower ON Follower.follower_ID = a.account_ID \
      INNER JOIN User_post ON User_post.account_ID = Follower.account_ID;"
      
      show_update_msg(self, user_info, user_following_query, "People")

    elif command == "n":
      pass
    else:
      print("Wrong command. Please enter y or n.")
      show_posts(self, user_info)


# Helper functions 
def show_update_msg(self, user_info, query, str):
    query = query % user_info["id"]
    self.cursor.execute(query)
    query_res = self.cursor.fetchall()
    filtered_list = list(filter(lambda x: x[0] > user_info["lastLoginTime"], query_res))
    if len(filtered_list) == 0:
        print(("No updates from %s you are following") %str)
    else:    
        print(("Posts from %s you are following: ") %str)
        show_msg_content(self, filtered_list)
        print(("------------------ End of following %s post -----------------------") %str)


# Show post content of user following tags/people
def show_msg_content(self, filtered_list):
    if len(filtered_list) == 0:
        print("No new post.")
        print("---------------------------------------------------")
    for row in filtered_list:
        self.cursor.execute("select post_ID, message, thumbs, is_read,account_name from User_post INNER JOIN Account USING (account_ID) where '%s' = User_post.post_ID;" % row[1])
        follow_post_message = self.cursor.fetchall()
        print("Post_ID: ", follow_post_message[0][0])
        print("Posted By: ", follow_post_message[0][4])
        print("Message: ", follow_post_message[0][1])
        print("Thumbs: ", follow_post_message[0][2])
        print("Is_read: ", follow_post_message[0][3])
        print("--------------- ******** -----------------------")
        self.cursor.execute("UPDATE User_post SET is_read = 1 WHERE '%s' = User_post.post_ID;" % row[1])
        self.dbconnection.commit()