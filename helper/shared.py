import sqlite3

errorCodes = [-1, -2]

def execute(connection, command):
  try:
    cursor = connection.cursor()
    cursor.execute(command)
    connection.commit()
    return 1
  except sqlite3.Error as er:
    print('sql error!!!')
    return -1
  except Exception as e:
    print('some error occured')
    return -2

def executeAndGetResult(connection, command):
  try:
    cursor = connection.cursor()
    cursor.execute(command)
    results = cursor.fetchall()
    connection.commit()
    return results
  except sqlite3.Error as er:
    print('sql error!!!')
    return -1
  except Exception as e:
    print('some error occured')
    return -2
