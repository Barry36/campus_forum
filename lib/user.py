def show_all_users(self, user_info):
  self.cursor.execute("SELECT * from Account;")
  show_users = self.cursor.fetchall()
  for e in show_users:
      print("Account ID:", e[0], "; Account Name:", e[1], "; First Name:", e[3],
        "; Last Name:", e[4], "; Sex:", e[5], "; Birthdate:", e[6], "; Last Login:", e[7])

def follow_user(self, user_info):
  follow_username = input("Enter the username of the person you wish to follow: ")
  self.cursor.execute("SELECT count(*), account_ID FROM Account where account_Name = '%s' group by account_ID;" % follow_username)
  cursor_fetch_result = self.cursor.fetchall()
  if cursor_fetch_result[0][0] == 0:
    print("This user ID is invalid")
  else:
    self.cursor.execute("INSERT INTO follower ( account_ID, follower_ID ) VALUES ( '%s', '%s' );" % (cursor_fetch_result[0][1], user_info["id"]))
    self.dbconnection.commit()
    print("---------------------------------------------------")
    print(("Success! You have are now following user with user name: %s") % follow_username)
    print("---------------------------------------------------")
  self.logged_in(user_info)


def unfollow_user(self, user_info):
  unfollow_username = input("Enter the username of the person you wish to unfollow: ")
  self.cursor.execute("SELECT count(*), Account.account_ID as followed_ID FROM Account \
    INNER JOIN Follower ON Account.account_ID = Follower.account_ID \
      where Account.account_Name = '%s' group by Account.account_ID;" % unfollow_username)
  cursor_fetch_result = self.cursor.fetchall()
  if cursor_fetch_result[0][0] == 0:
    print("You are not followed to them")
  else:
    followedID = cursor_fetch_result[0][1]
    self.cursor.execute("DELETE FROM follower where follower.account_ID = %d and follower.follower_ID = %d;" % (followedID, user_info["id"]))
    self.dbconnection.commit()
    print("---------------------------------------------------")
    print(("Success! You have unfollowe user with username: %s") % unfollow_username)
    print("---------------------------------------------------")
  self.logged_in(user_info)
