def show_all_users(self, user_info):
  self.cursor.execute("SELECT * from Account;")
  show_users = self.cursor.fetchall()
  for e in show_users:
      print("Account ID:", e[0], "; Account Name:", e[1], "; First Name:", e[3],
        "; Last Name:", e[4], "; Sex:", e[5], "; Birthdate:", e[6], "; Last Login:", e[7])

def show_all_users_following(self, user_info):
  user_ID = int(user_info["id"])
  self.cursor.execute("select account_Name from Follower where follower_ID = %d;" % user_ID)
  show_following_users = self.cursor.fetchall()
  if len(show_following_users) == 0:
    print("---------------------------------------------------")
    print("You are not following any users, enter 'fu' to follow users!")
    print("---------------------------------------------------")
  else:
    print("---------------------------------------------------")
    print("You are Following below users:")
    for e in show_following_users:
      print(e[0])
    print("---------------------------------------------------")
  self.logged_in(user_info)

def follow_user(self, user_info):
  follow_username = input("Enter the username of the person you wish to follow: ")
  self.cursor.execute("SELECT account_ID, account_Name FROM Account where account_Name = '%s';" % follow_username)
  cursor_fetch_result = self.cursor.fetchall()
  if len(cursor_fetch_result) == 0:
    print("This username is invalid")
  else:
    self.cursor.execute("INSERT INTO follower ( account_ID, account_Name, follower_ID, follower_Name ) VALUES ( %d, '%s', %d, '%s' );" % (cursor_fetch_result[0][0],cursor_fetch_result[0][1], user_info["id"], user_info["name"]))
    self.dbconnection.commit()
    print("---------------------------------------------------")
    print(("Success! You are now following user with user name: %s") % follow_username)
    print("---------------------------------------------------")
  self.logged_in(user_info)


def unfollow_user(self, user_info):
  unfollow_username = input("Enter the username of the person you wish to unfollow: ")
  self.cursor.execute("SELECT count(*), Account.account_ID as followed_ID FROM Account \
    INNER JOIN Follower ON Account.account_ID = Follower.account_ID \
      where Account.account_Name = '%s' group by Account.account_ID;" % unfollow_username)
  cursor_fetch_result = self.cursor.fetchall()
  if cursor_fetch_result[0][0] == 0:
    print("You are not followed to this user!")
  else:
    followedID = cursor_fetch_result[0][1]
    self.cursor.execute("DELETE FROM Follower where follower.account_ID = %d and follower.follower_ID = %d;" % (followedID, user_info["id"]))
    self.dbconnection.commit()
    print("---------------------------------------------------")
    print(("Success! You have unfollowed user with username: %s") % unfollow_username)
    print("---------------------------------------------------")
  self.logged_in(user_info)
