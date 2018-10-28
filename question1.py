import random
import pickle
import sys


class Admin:        
   
    def __init__(self,name,Id,password):
		self.Id = Id
		self.name = name
		self.password = password

    def viewProducts(self):
    	for product in productsList:
    		print product.Id ," ",product.name," ",product.price," ",product.quantity 	

    def viewCustomerList(self):
    	for	customer in registeredCustomers:
    		print customer.Id
    		print customer.name
    		print customer.cart.productsList
    		print customer.productsBought
    		print customer.paymentList
    		print " "
    		print " "

    def addProduct(self,product):
		productsList.append(product)

    def deleteProduct(self,productId):
    	for product in productsList:
			if product.Id == productId:
				productsList.remove(product)
				break					

		 
    def modifyProduct(self,productId):
    	for product in productsList:
			if product.Id == productId:
				print "Enter new quantity for ", product.name
				quantity = int(raw_input()) 
				productsList.remove(product)
				product.quantity = quantity
				productsList.append(product)
				break
			

    def makeShipment(self):
		pass

    def confirmDelivery(self):
		pass		         

class Customer: 

	def __init__(self,Id,password,name,address,phno,cart):
		self.Id = Id
		self.password = password
		self.name = name
		self.address = address
		self.phno = phno
		self.cart = cart
		self.productsBought = []
		self.paymentList = []		

	def buyProduct(self):
	
		print "Enter product Id "
		prodId = raw_input()

		print "Enter quantity"
		quantity = int(raw_input())

		for product in productsList:
			if product.Id == prodId:
				if quantity <= product.quantity:
					self.addToCart(product,quantity)
					break
				else:
					print "Unable to process request. Quantity entered is more than stock availble"	
	
		print "Press 1 to make payment"
		print "Press any other key to continue shopping"
		
		userInput = int(raw_input())

		if userInput == 1:

			print "Enter your card type"
			cardType = raw_input()

			print "Enter card number"
			cardNumber = raw_input()

			payment = Payment(self.Id,self.name,cardType,cardNumber)
			self.makePayment(payment)
	
	def viewProduct(self):
		for product in productsList:
			print product.Id ," ",product.name," ",product.price," ",product.quantity
	  
	def makePayment(self,payment):
		for product in self.cart.productsList:
			payment.amount += product.price
			self.productsBought.append(product)
			self.deleteFromCart(product.Id)
		self.paymentList.append(payment)	
		  
	def addToCart(self,productId,quantity):
		for product in productsList:
			if product.Id == productId:
				productBought = Product(product.Id,product.name,product.price,quantity,product.group,
										product.subgroup)
				product.quantity -= quantity
				
				if product.quantity == 0:
					productsList.remove(product)

				self.cart.productsList.append(productBought)
				self.cart.numberOfProduct = self.cart.numberOfProduct + productBought.quantity
				self.cart.total = self.cart.total + productBought.price * productBought.quantity		
				break
		
	def viewCart(self):
		
		print "Number of products in the cart: ",self.cart.numberOfProduct
		print "Total amount of goods in cart: ",self.cart.total
		
		for item in self.cart.productsList:
			print item.Id," ",item.name," ",item.price," ",item.quantity," ",item.group," ",item.subgroup 			


	def deleteFromCart(self,productId):
		print productId
		flag = False
		for product in self.cart.productsList:
			if product.Id == productId:

				for item in productsList:
					if item.Id == prodId:
						item.quantity += product.quantity
						flag = True
						break
				if flag == False:
					productRemoved = Product(product.Id,product.name,product.price,product.quantity,
																	product.group,product.subgroup)
					productsList.append(productRemoved)

				self.cart.total = self.cart.total - product.price * product.quantity
				self.cart.numberOfProduct = self.cart.numberOfProduct - product.quantity
				self.cart.productsList.remove(product)
				break


class Product: 
   
    def __init__(self,Id,name,price,quantity,group,subgroup):
		self.Id = Id
		self.name = name
		self.price = price
		self.quantity = quantity
		self.group = group
		self.subgroup = subgroup

class Guest: 

    def __init__(self,guestId):
   		self.guestId = guestId

    def viewProduct(self):
		for product in productsList:
			print product.Id," ",product.name," ",product.price," ",product.quantity 	

    def getRegistered(self):
		pass		   

class Cart: 

    def __init__(self,Id,numberOfProduct,total):
   		self.Id = Id
		self.numberOfProduct = numberOfProduct
		self.productsList = []
		self.total = total

class Payment: 

    def __init__(self,customerId,name,cardType,cardNumber):
		self.customerId = customerId
		self.name = name
		self.amount = 0
		self.cardType = cardType
		self.cardNumber = cardNumber

	

def checkValidLogin(registeredCustomers,username,password):
	for customer in registeredCustomers:
		if customer.Id == username and customer.password == password:
			return True, customer
	return False,""
			
def checkValidUserName(registeredCustomers,username):
	for customer in registeredCustomers:
		if customer.Id == username:
			return False
	return True

def addToCustomerList(registeredCustomers,customer):

	registeredCustomers.append(customer)

def createNewUser(registeredCustomers,username,password):
	print "Enter your name: "
	name = raw_input()
	print "Enter your address: "
	address = raw_input()
	print "Enter your phone no: "
	phno = raw_input()

	userCart = Cart(username,0,0)

	customer = Customer(username,password,name,address,phno,userCart)
	addToCustomerList(registeredCustomers,customer)
	return customer

def printProductList(productsList):
	for product in productsList:
		print product.name ," : " ,product.price, " ",product.quantity	

def checkValidAdminLogin(adminAccounts,username,password):
	for admin in adminAccounts:
		if admin.Id == username and admin.password == password:
			return True , admin
	return False, ""

def printCustomerList(registeredCustomers):
	for customer in registeredCustomers:
		print customer.username ," : " ,customer.password	

def adminLogin():

	global isAdmin
	global isRegisteredUser	
	global isUnregisteredUser

	print "Enter Your Username: "
	username = raw_input()
	
	print "Enter Your Password: "
	password = raw_input()

	flag , user = checkValidAdminLogin(adminAccounts,username,password)

	if flag == True:
		print "Login Successful"
		isAdmin = True
		isRegisteredUser = False
		isUnregisteredUser = False
		return user	
	else:
		print "Invalid Username or Password"

def userLogin():

	global isAdmin
	global isRegisteredUser	
	global isUnregisteredUser

	print "Enter Your Username: "
	username = raw_input()

	print "Enter Your Password: "
	password = raw_input()

	flag, user = checkValidLogin(registeredCustomers,username,password)

	if flag == True:
		print "Login Successful"
		isRegisteredUser = True
		isAdmin = False
		isUnregisteredUser = False
		return 1,user
	else:
		print "Invalid Username or Password"
		user = Guest(random.randint(1,101))
		return 2,user

		
def createNewAccount():
	
	print "Enter a unique username"
	
	
	while True:

		username = raw_input()
		flag = checkValidUserName(registeredCustomers,username)

		if flag == True:
			print "Enter Your Password"

			while True:
		
				password = raw_input()

				if len(password) > 0:
					newUser = createNewUser(registeredCustomers,username,password)
					isAdmin = False
					isRegisteredUser = True
					isUnregisteredUser = False
					return newUser
					break
				else:
					print "Password cannot be left empty"
					print "Re-enter Your Password"	
				break		
			break
		else:
			print "Username alread in use, please re-enter a unique username"		


def runAsAdmin(adminUser):
	
	while True:

		print "Press 1 to view products"
		print "Press 2 to view registered customers"
		print "Press 3 to add products"
		print "Press 4 to delete product"
		print "Press 5 to modify product"
		print "Press 6 to make shipment"
		print "Press 7 to confirm delivery"
		print "Press 8 to exit"

		userInput = int(raw_input())

		if userInput == 1:
			adminUser.viewProducts()
		
		elif userInput == 2:
			adminUser.viewCustomerList()	

		elif userInput == 3:
			print "Enter product Id"
			id_input = raw_input()
			
			print "Enter name"
			name = raw_input()
			
			print "Enter price"
			price = float(raw_input())
			
			print "Enter quantity"
			quantity = int(raw_input())
			
			print "Enter group"
			group = raw_input()
			
			print "Enter subgroup"
			subgroup = raw_input()

			product = Product(id_input,name,price,quantity,group,subgroup)

			adminUser.addProduct(product)

		elif userInput == 4:
			print "Enter product id "
			Id = raw_input()

			adminUser.deleteProduct(Id)

		elif userInput == 5:
			print "Enter product id "
			Id = raw_input()

			adminUser.modifyProduct(Id)
			
		elif userInput == 6:
			adminUser.makeShipment()
		
		elif userInput == 7:
			adminUser.confirmDelivery()	

		elif userInput == 8:

			adminFile = open('admin_file','wb')
			regUserFile = open('regUser_file','wb')
			prodListFile = open('product_file','wb')
			
			pickle.dump(adminAccounts,adminFile)
			pickle.dump(registeredCustomers,regUserFile)
			pickle.dump(productsList,prodListFile)
			
			adminFile.close()
			regUserFile.close()
			prodListFile.close()

			sys.exit()	

		else :
			print "Invalid input"		

def runAsGuest(guestUser):
	while True:
		print "Press 1 to view products"
		print "Press 2 to create a new account"
		print "Press 3 to exit"

		userInput = int(raw_input())

		if userInput == 1:

			guestUser.viewProduct()
		elif userInput == 2:	
			regUser = createNewAccount()
			print "New account created successfully"
			print "Please login as registered user"
			uType, user = userLogin()
			runasRegisteredUser(user)
		elif userInput == 3:

			adminFile = open('admin_file','wb')
			regUserFile = open('regUser_file','wb')
			prodListFile = open('product_file','wb')
			
			pickle.dump(adminAccounts,adminFile)
			pickle.dump(registeredCustomers,regUserFile)
			pickle.dump(productsList,prodListFile)
			
			adminFile.close()
			regUserFile.close()
			prodListFile.close()

			sys.exit()
		else:
			print "Invalid input"	

def runasRegisteredUser(registeredUser):
	
	while True:		
		print "Press 1 to buy product"
		print "Press 2 to view products"
		print "Press 3 to view cart"
		print "Press 4 to add product to cart"
		print "Press 5 to delete product from cart"
		print "Press 6 to make payment"
		print "Press 7 to exit"

		userInput = int(raw_input())

		if userInput == 1:
			registeredUser.buyProduct()
		elif userInput == 2:
			registeredUser.viewProduct()

		elif userInput == 3:
			registeredUser.viewCart()	
				
		elif userInput == 4:
			print "Enter product id "
			productId = raw_input()
			
			print "Enter quantity"
			quantity = int(raw_input())

			for product in productsList:
				if productId == product.Id :
					if quantity <= product.quantity:
						registeredUser.addToCart(productId,quantity)
					else:
						print "Unable to process request. Quantity entered is more than stock availble"	

		elif userInput == 5:
			print "Enter product id "
			productId = raw_input()
			
			registeredUser.deleteFromCart(productId)
				
		elif userInput == 6:
			print "Enter your card type"
			cardType = raw_input()

			print "Enter card number"
			cardNumber = raw_input()

			payment = Payment(registeredUser.Id,registeredUser.name,cardType,cardNumber)
			registeredUser.makePayment(payment)
		
		elif userInput == 7:

			adminFile = open('admin_file','wb')
			regUserFile = open('regUser_file','wb')
			prodListFile = open('product_file','wb')
			
			pickle.dump(adminAccounts,adminFile)
			pickle.dump(registeredCustomers,regUserFile)
			pickle.dump(productsList,prodListFile)
			
			adminFile.close()
			regUserFile.close()
			prodListFile.close()

			sys.exit()	
		else:
			print "Invalid input"	


def main():

	global isAdmin
	global isRegisteredUser	
	global isUnregisteredUser

	while True :

		print "Press 1 to login as Admin"
		print "Press 2 to login as registered user"
		print "Press 3 to create a new account"
		print "Press 4 to continue as a guest user"
		print "Press 5 to exit"
		print "Enter Your Choice: "

		userInput = int(raw_input());

		if userInput == 1 :
			user = adminLogin()
			break

		elif userInput == 2:
			uType, user = userLogin()	
			break

		elif userInput == 3:
			regUser = createNewAccount()
			print "New account created successfully"
			print "Please login as registered user"
			uType, user = userLogin()
			runasRegisteredUser(user)	

		elif userInput == 4:
			isAdmin = False
			isRegisteredUser = False
			isUnregisteredUser = True
			user = Guest(random.randint(1,101))
			break
		elif userInput == 5:

			adminFile = open('admin_file','wb')
			regUserFile = open('regUser_file','wb')
			prodListFile = open('product_file','wb')
			
			pickle.dump(adminAccounts,adminFile)
			pickle.dump(registeredCustomers,regUserFile)
			pickle.dump(productsList,prodListFile)
			
			adminFile.close()
			regUserFile.close()
			prodListFile.close()

			sys.exit()

		else:
			print "Invalid input"	

	if isAdmin == True:
		runAsAdmin(user)
	
	elif isAdmin == False and isRegisteredUser == False:
		runAsGuest(user)
	
	elif isRegisteredUser == True:
		runasRegisteredUser(user)

	else:
		print "Invalid input"	


if __name__ == "__main__":

	adminFile = open('admin_file','a')
	regUserFile = open('regUser_file','a')
	prodListFile = open('product_file','a')

	adminFile.close()
	regUserFile.close()
	prodListFile.close()


	adminFile = open('admin_file','rb')
	regUserFile = open('regUser_file','rb')
	prodListFile = open('product_file','rb')

	try:
		adminAccounts = pickle.load(adminFile)
	except EOFError:
		adminAccounts = []

	try:
		registeredCustomers = pickle.load(regUserFile)
	except EOFError:
		registeredCustomers = []

	try:
		productsList = pickle.load(prodListFile)
	except EOFError:
		productsList = []		

	
	adminFile.close()
	regUserFile.close()
	prodListFile.close()


	adminUser = Admin(1,"prakash","q")
	adminAccounts.append(adminUser)

	isAdmin = False
	isUnregisteredUser = True
	isRegisteredUser = False

	main()


