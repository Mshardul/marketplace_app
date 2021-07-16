import json
from helper.shared import errorCodes, execute, executeAndGetResult
import sqlite3

# variables
prodId = 1100

def addProduct(connection, userId, category, name, image, price, stock=True, salePrice=-1):
  global prodId
  prodId = prodId + 1
  formatStr = """
  INSERT INTO Products (id, category, name, image, stock, price, salePrice, seller)
  VALUES ({prodId}, '{category}', '{name}', '{image}', '{stock}', {price}, {salePrice}, {seller});
  """
  addProd = formatStr.format(prodId=prodId, category=category, name=name, image=image, stock=stock, price=price, salePrice=salePrice, seller=userId)
  if (execute(connection, addProd) not in errorCodes):
    return prodId
  return 0

def verifyProduct(connection, userId, prodId):
  formatStr = """
  SELECT * FROM Products
  WHERE seller={userId} AND id={prodId};
  """
  getProd = formatStr.format(userId=userId, prodId=prodId)
  rows = executeAndGetResult(connection, getProd)
  if (rows not in errorCodes):
    return len(rows)
  return 0

'''
0: error
[]: product does not exist
'''
def getProductInfo(connection, prodId):
  formatStr = """
  SELECT * FROM Products
  WHERE id={prodId};
  """
  getProd = formatStr.format(prodId=prodId)
  rows = executeAndGetResult(connection, getProd)
  if (rows not in errorCodes):
    return rows
  return 0
  

def getProductsList(connection, sortOption=3, onlyInStock=False, self=False, userId=-1):

  def getAllProducts():
    return "SELECT id, category FROM Products"

  def getMyProducts(userId):
    formatStr = """
    SELECT id, category FROM Products
    WHERE seller={userId}
    """
    return formatStr.format(userId=userId)

  def getAvailableProducts():
    return "SELECT id, category FROM Products WHERE stock='True'"

  def getMyAvailableProducts(userId):
    formatStr = """
    SELECT id, category FROM Products
    WHERE seller={userId} AND stock='True'
    """
    return formatStr.format(userId=userId)

  sqlQuery = ''
  if (self):
    if (onlyInStock):
      sqlQuery = getMyAvailableProducts(userId)
    else:
      sqlQuery = getMyProducts(userId)
  else:
    if (onlyInStock):
      sqlQuery = getAvailableProducts(userId)
    else:
      sqlQuery = getAllProducts(userId)

  if (sortOption==1):
    sqlQuery += ' ORDER BY name ASC;'
  elif (sortOption==2):
    sqlQuery += ' ORDER BY name DESC;'
  else:
    sqlQuery += ';'

  rows = executeAndGetResult(connection, sqlQuery)
  if (rows not in errorCodes):
    return rows
  return 0

def modifyProduct(connection, userId, prodId, name, category, image, price, stock, salePrice):
  formatStr = """
  UPDATE Products
  SET category='{category}', name='{name}', image='{image}', stock='{stock}', price={price}, salePrice={salePrice}
  WHERE id={prodId};
  """
  updateProd = formatStr.format(category=category, name=name, image=image, stock=stock, price=price, salePrice=salePrice, prodId=prodId)
  if (execute(connection, updateProd) not in errorCodes):
    return 1
  return 0