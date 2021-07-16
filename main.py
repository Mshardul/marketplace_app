import sqlite3
from toSQLite import initDB
from helper.user import signIn, signUp, verifyCredentials
from helper.product import addProduct, getProductsList, modifyProduct, verifyProduct

def action_signIn():
  if (verifyCredentials(connection)):
    print('successfully signed in')
  else:
    print('the credentials are wrong')

def action_signUp():
  name = input("enter your user name: ")
  password = input("enter your password: ")
  id = signUp(connection, name, password)
  if(id):
    print('successful registration!! your id is: ', id)
  else:
    print('could not register user')

def action_addProduct():
  userId = verifyCredentials(connection)
  if (userId):
    print('credentials matched. Provide product details')
    name = input('name: ')
    category = input('category: ')
    image = input('image: ')
    price = input('price: ')
    prodId = addProduct(connection, userId, category, name, image, price)
    if (prodId):
      print('product added successfully!! product id is: ', prodId)
    else:
      print('could not add product')
  else:
    print('the credentials are wrong')

def action_modifyProduct():
  userId = verifyCredentials(connection)
  if (userId):
    print('credentials matched. Provide product details')
    prodId = input('product id: ')
    if (verifyProduct(connection, userId, prodId)):
      name = input('name: ')
      category = input('category: ')
      image = input('image: ')
      price = input('price: ')
      salePrice = input('salePrice')
      stock = input('stock')
      if (modifyProduct(connection, userId, prodId, name, category, image, price, stock, salePrice)):
        print('prodct details modified')
      else:
        print('could not modify product details')
    else:
      print('product does not exist')
  else:
    print('the credentials are wrong')

def action_listProducts():
  option = input('1. ascending by Product Name; 2. descending by Product Name')
  prodList = getProductsList(connection, option)
  if (prodList):
    print(prodList)

initDB()

# connect with the DB
connection = sqlite3.connect('assessment.db')

# operations
while(1):
  break
  print("you can work with following APIs")
  print("1. Login")
  print("2. Register")
  print("3. Add Product")
  print("4. Modify Product")
  print("5. List All Products")
  print("6. Bid on Product")
  print("5. exit")
  option = int(input())
  switch = [
    action_signIn,
    action_signUp,
    action_addProduct,
    action_modifyProduct,
    action_listProducts,
    action_bidOnProduct,
    # getHighestBid()
  ]
  switch[option-1]()

# close DB connection
connection.close()