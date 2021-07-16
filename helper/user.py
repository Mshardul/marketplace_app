import json
from helper.shared import errorCodes, execute, executeAndGetResult

# variables
userId = 100

# helper function - just to verify user credentials
def verifyCredentials(connection):
  userId = input("enter your id: ")
  password = input("enter your password: ")
  return signIn(connection, userId, password)

# sign existing user in
def signIn(connection, userId, password):
  formatStr = """
  SELECT * FROM Names
  WHERE id={userId} AND password='{password}';
  """
  getUser = formatStr.format(userId=userId, password=password)
  rows = executeAndGetResult(connection, getUser)
  if(rows not in errorCodes):
    return len(rows)
  return 0

# register a new user
def signUp(connection, name, password):
  global userId
  userId += 1
  formatStr = """
  INSERT INTO Names (id, name, password)
  VALUES ({userId}, '{name}', '{password}');
  """
  addUser = formatStr.format(userId=userId, name=name, password=password)
  if (execute(connection, addUser) not in errorCodes):
    return userId
  return 0