from lib import helper
class myClass:
    str = "Barry"
    def myFunction(self):
        print(helper.do_something(self))


if __name__ == "__main__":
  app = myClass()
  app.myFunction()
  print("hey")