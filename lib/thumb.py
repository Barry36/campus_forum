def thumbup(self, user_info):
    postID = input("Enter the post ID you would like to thumb up: ")
    validPost = self.checkValid("user_post", "post_ID", postID)
    if validPost == [(0,)]:
      print("This is an invalid postID")
    else:
      self.cursor.execute("UPDATE User_post SET thumbs = thumbs+1 WHERE '%s' = User_post.post_ID;" % postID)
      self.dbconnection.commit()
      print("hey")
      print(postID)
      thumbs_cnt = thumb_count(self, postID)

      print("---------------------------------------------------")
      print(("Success! You have thumbed up the post with postID: %s ") % postID)
      print(("The total thumbs of this post is: %s") % thumbs_cnt)
      print("---------------------------------------------------")
    self.logged_in(user_info)

def thumbdown(self, user_info):
    postID = input("Enter the post ID you would like to thumbdown: ")
    validPost = self.checkValid("user_post", "post_ID", postID)
    if validPost == [(0,)]:
      print("That is an invalid post ID")
    else:
      self.cursor.execute("UPDATE User_post SET thumbs = thumbs-1 WHERE '%s' = User_post.post_ID;" % postID)
      self.dbconnection.commit()
      thumbs_cnt = thumb_count(self, postID)
      
      print("---------------------------------------------------")
      print(("Success! You have thumbed down the post with postID: %s ") % postID)
      print(("The total thumbs of this post is: %s") % thumbs_cnt)
      print("---------------------------------------------------")
    self.logged_in(user_info)

# helper function
def thumb_count(self, postID):
    self.cursor.execute("SELECT thumbs from user_post where post_ID = '%s';" % postID)
    thumbs_cnt_res = self.cursor.fetchall()
    
    return thumbs_cnt_res[0][0]