from lib import helper
class myClass:
    def fxn(self, str):
      return "My name is %s" %str

if __name__ == "__main__":
  str = "afiasjf"
  app = myClass()
  res = app.fxn(str)
  print(res)