def show_all_tags(self, user_info):
    self.cursor.execute("SELECT * from Post_Tag")
    show_tags = self.cursor.fetchall()
    for e in show_tags:
        print("Tag Name:", e[0],"; Tagged Post ID:", e[1])

def show_tags_followed_by_user(self, user_info):
    user_ID = int(user_info["id"])
    self.cursor.execute("select * from Follow_Tag where account_ID = %d;" % user_ID)
    validFollow = self.cursor.fetchall()
    print("---------------------------------------------------")
    if len(validFollow) == 0:
        print("You are not following any tags!")
    else:
        # print all tags followed by the user
        for e in validFollow:
            print(("Tag you are following: %s;") %e[0])
    print("---------------------------------------------------")   
    self.logged_in(user_info)

def follow_tag(self, user_info):
    tagName = input("Enter the name of the tag you wish to follow: ")
    self.cursor.execute("INSERT INTO Follow_Tag ( tag_Name, account_ID ) VALUES ( '%s', '%s' );" % (tagName, user_info["id"]))
    self.dbconnection.commit()
    print("---------------------------------------------------")
    print(("Success! You have followed tag with tag name: %s") %tagName)
    print("---------------------------------------------------")
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
      print("---------------------------------------------------")
      print(("Success! You have unfollowed tag with tag name: %s") %tagName)
      print("---------------------------------------------------")
    self.logged_in(user_info)
    self.logged_in(user_info)