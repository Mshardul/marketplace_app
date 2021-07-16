import json
import sqlite3

def readFile(path):
  f = open(path, 'r')
  data = json.load(f)
  return data

def connectToDB(commands):
  connection = sqlite3.connect('assessment.db')
  cursor = connection.cursor()

  def executeCommand(command):
    cursor.execute(command)

  for command in commands:
    executeCommand(command)
  connection.commit()
  connection.close()

def convertNamesToSQLite():
  createTable = """
  CREATE TABLE IF NOT EXISTS Names (
    id INTEGER PRIMARY_KEY,
    name VARCHAR(100),
    password VARCHAR(100)
  );
  """
  commands = [createTable]
  data = readFile('data/names.json')
  for row in data:
    formatStr = """
    INSERT INTO Names (id, name, password) 
    VALUES ({id}, "{name}", "password");
    """
    insertRow = formatStr.format(id=row['id'], name=row['name'])
    commands.append(insertRow)
  connectToDB(commands)

def convertProductsToSQLite():
  createTable = """
  CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY_KEY,
    category VARCHAR(100),
    name VARCHAR(100),
    image VARCHAR(200),
    stock VARCHAR(5),
    price REAL,
    salePrice REAL,
    seller INTEGER,
    FOREIGN KEY (seller) REFERENCES Names(id) ON DELETE CASCADE
  );
  """
  commands = [createTable]
  data = readFile('data/products.json')
  for row in data:
    formatStr = """
    INSERT INTO Products (id, category, name, image, stock, price, salePrice, seller)
    VALUES ({id}, "{category}", "{name}", "{image}", "{stock}", {price}, {salePrice}, 1);
    """
    insertRow = formatStr.format(id=row['productId'], category=row['productCategory'], name=row['productName'], image=row['productImage'], stock=row['productStock'], price=row['productPrice'], salePrice=row['salePrice'])
    commands.append(insertRow)
  connectToDB(commands)

def addBidsTable():
  createTable = """
  CREATE TABLE IF NOT EXISTS Bids (
    id INTEGER PRIMARY_KEY,
    prodId INTEGER,
    buyerId INTEGER,
    price REAL,
    FOREIGN KEY (prodId) REFERENCES Product(id) ON DELETE CASCADE,
    FOREIGN KEY (buyerId) REFERENCES Names(id) ON DELETE CASCADE
  );
  """
  commands = [createTable]
  connectToDB(commands)
  
    
def initDB():
  convertNamesToSQLite()
  convertProductsToSQLite()
  addBidsTable()