def show_all_groups(self, user_info):   # show all groups
    self.cursor.execute("SELECT * from user_group;") 
    show_groups = self.cursor.fetchall()

    for e in show_groups:
        print("Group ID:", e[0],"; Group Name:", e[1],"; Description:", e[2])

def join_group(self, user_info):
    groupID = input("Enter the Group ID you would like to join: ")
    validGroup = self.checkValid("user_group", "group_ID", groupID)
    if validGroup == [(0,)]:
      print("This Group ID is invalid, please try again!")
    else:
      self.cursor.execute("INSERT INTO Group_members ( group_ID, account_ID ) VALUES ( '%s', '%s' );" % (groupID, user_info["id"]))
      self.dbconnection.commit()
      print("-----------------------------------------")
      print(("Success! You have joined the group with group_ID: %s") % groupID)
      print("-----------------------------------------")
    
    self.logged_in(user_info)

def create_group(self, user_info):
    groupName = input("Give a name of the Group: ")
    groupDesc = input("Give a description of your Group: ")
    self.cursor.execute("INSERT INTO user_group ( group_Name, description ) VALUES ( '%s', '%s' );" % (groupName, groupDesc))
    self.dbconnection.commit()
    
    print("-----------------------------------------")
    print("Success! You have created your group!")
    print("-----------------------------------------")
    self.logged_in(user_info)

