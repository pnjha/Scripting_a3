import random
import pickle
import sys
import os
import time

class Admin:        
   
	def __init__(self,Id,name,password):
		self.Id = Id
		self.name = name
		self.password = password

	def viewProducts(self):
		for product in productsList:
			print "Product Id\tProduct name\tPrice\tQuantity\tGroup\tSubGroup"
			print product.Id,"\t\t",product.name,"\t\t",product.price,"\t",product.quantity,"\t\t",product.group,"\t",product.subgroup 
			print ""

	def viewCustomerList(self):
		for	customer in registeredCustomers:
			print "Customer Id: ",customer.Id
			print "Customer Name: ",customer.name
			
			print "Cart content: "
			for product in customer.cart.productsList:
				print "Product Id\tProduct name\tPrice\tQuantity\tGroup\tSubGroup"
				print product.Id,"\t\t",product.name,"\t\t",product.price,"\t",product.quantity,"\t\t",product.group,"\t",product.subgroup 
				print ""
			print ""	
			
			print "Products bought: ",
			for product in customer.productsBought:
				print "Product Id\tProduct name\tPrice\tQuantity\tGroup\tSubGroup"
				print product.Id,"\t\t",product.name,"\t\t",product.price,"\t",product.quantity,"\t\t",product.group,"\t",product.subgroup 
				print ""
			print ""
				
			print "Payment history: "
			for payment in customer.paymentList:
				print "Payment amount\tCard Type\tCard Number"
				print payment.amount,"\t\t",payment.cardType,"\t\t",payment.cardNumber
				print ""				
			print ""
				
		print " "

	def addProduct(self,product):

		productsList.append(product)

	def deleteProduct(self,productId):
		for product in productsList:
			if product.Id == productId:
				productsList.remove(product)
				break					

		 
	def modifyProduct(self,productId):
		
		print "Press 1 to update name"
		print "Press 2 to update price"
		print "Press 3 to update quantity"
		print "Press 4 to update group"
		print "Press 5 to update subgroup"

		try:
			userInput = int(raw_input())

			for product in productsList:
				if product.Id == productId:
					if userInput == 1:
						print "Enter new name for ", product.name
						name = raw_input() 
						productsList.remove(product)
						product.name = name
						productsList.append(product)
						break

					elif userInput == 2:
						print "Enter new price for ", product.name
						price = int(raw_input()) 
						productsList.remove(product)
						product.price = price
						productsList.append(product)
						break

					elif userInput == 3:
						print "Enter new quantity for ", product.name
						quantity = int(raw_input()) 
						productsList.remove(product)
						product.quantity = quantity
						productsList.append(product)
						break

					elif userInput == 4:
						print "Enter new group for ", product.name
						group = raw_input() 
						productsList.remove(product)
						product.group = group
						productsList.append(product)
						break

					elif userInput == 5:			
						print "Enter new subgroup for ", product.name
						subgroup = raw_input()  
						productsList.remove(product)
						product.subgroup = subgroup
						productsList.append(product)
						break

		except ValueError:
			print "Invalid input"			

	def viewOrdersPlaced(self):
		for order in ordersList:
			print "Customer Id: ",order[0]
			print "Product Id: ",order[1]
			print "Product Name: ",order[2]
			print "Product Quantity: ",order[3]
			print "Product Price: ",order[4]			
			print "**************"

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
		try:
			flag = False

			print "Enter product Id "
			prodId = int(raw_input())

			print "Enter quantity"
			quantity = int(raw_input())

			for product in productsList:
				if product.Id == prodId:
					if quantity <= product.quantity:
						self.addToCart(product.Id,quantity)
						flag = True
						break
					else:
						print "Unable to process request. Quantity entered is more than stock availble"
						return

			if flag == False:
				return

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
		except ValueError:
			print "Invalid Input"

	def viewProduct(self):
		for product in productsList:
			print "Product Id\tProduct name\tPrice\tQuantity\tGroup\tSubGroup"
			print product.Id,"\t\t",product.name,"\t\t",product.price,"\t",product.quantity,"\t\t",product.group,"\t",product.subgroup 
			print ""

	def makePayment(self,payment):
		for product in self.cart.productsList:

			for prod in productsList:
				if prod.Id == product.Id:
					prod.quantity -= product.quantity

					if prod.quantity == 0:
						productsList.remove(prod)	 

			payment.amount += product.price
			self.productsBought.append(product)
			self.deleteFromCart(product.Id,product.quantity,False)
			ordersList.append((self.Id,product.Id,product.name,product.price,product.quantity))
		self.paymentList.append(payment)

		  
	def addToCart(self,productId,quantity):
		for product in productsList:
			if product.Id == productId:
				productBought = Product(product.Id,product.name,product.price,quantity,product.group,
										product.subgroup)

				self.cart.productsList.append(productBought)
				self.cart.numberOfProduct = self.cart.numberOfProduct + productBought.quantity
				self.cart.total = self.cart.total + productBought.price * productBought.quantity		
				break
		
	def viewProductsBought(self):			
		for product in self.productsBought:
			print product.Id," ",product.name," ",product.price," ",product.quantity," ",product.group," ",product.subgroup

	def viewPaymentHistory(self):
		for payment in self.paymentList:
			print payment.customerId," ",payment.name," ",payment.amount," ",payment.cardType," ",payment.cardNumber									

	def viewCart(self):
		
		print "Number of products in the cart: ",self.cart.numberOfProduct
		print "Total amount of goods in cart: ",self.cart.total
		
		for item in self.cart.productsList:
			print item.Id," ",item.name," ",item.price," ",item.quantity," ",item.group," ",item.subgroup 			


	def deleteFromCart(self,productId,quantity,Flag):
		print productId
		flag = False
		for product in self.cart.productsList:
			if product.Id == productId and product.quantity >= quantity:

				self.cart.total = self.cart.total - product.price * quantity
				self.cart.numberOfProduct = self.cart.numberOfProduct - quantity
				
				if product.quantity == quantity:
					self.cart.productsList.remove(product)
				
				else:	
					productRemoved = Product(product.Id,product.name,product.price,
												product.quantity-quantity,product.group,product.subgroup)

					self.cart.productsList.remove(product)
					self.cart.productsList.append(productRemoved)					

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
			print "Product Id\tProduct name\tPrice\tQuantity\tGroup\tSubGroup"
			print product.Id,"\t\t",product.name,"\t\t",product.price,"\t",product.quantity,"\t\t",product.group,"\t",product.subgroup 
			print ""

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
	try:
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
	except ValueError:
		print "Invalid Input"
		
def printProductList(productsList):
	for product in productsList:
		print product.name ," : " ,product.price, " ",product.quantity	

def checkValidAdminLogin(adminAccounts,username,password):
	for admin in adminAccounts:
		if admin.name == username and admin.password == password:
			return True , admin
	return False, ""

def printCustomerList(registeredCustomers):
	for customer in registeredCustomers:
		print customer.username ," : " ,customer.password	

def adminLogin():

	global isAdmin
	global isRegisteredUser	
	global isUnregisteredUser

	try:
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
			isAdmin = False
			isRegisteredUser = False
			isUnregisteredUser = True
			print "Invalid Username or Password"
			user = Guest(random.randint(1,101))
			return user

	except ValueError:
		print "Invalid Input"		

def userLogin():

	global isAdmin
	global isRegisteredUser	
	global isUnregisteredUser

	try:
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

			validFlag = False

			for product in user.cart.productsList:
				for prod in productsList:
					if prod.Id == product.Id:
						validFlag = True
						break

				if validFlag == False:
					user.cart.productsList.remove(product)

				validFlag = False	

			return 1,user
		else:
			print "Invalid Username or Password"
			user = Guest(random.randint(1,101))
			return 2,user
	except ValueError:
		print "Invalid input" 		
		
def createNewAccount():
	
	print "Enter a unique username"
	
	try:
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
	except ValueError:
		print "Invalid input"			

def runAsAdmin(adminUser):
	
	os.system('clear')

	print "********** Welcome ",adminUser.name,"***********"
	try:
		while True:

			print "Press 1 to view products"
			print "Press 2 to view registered customers"
			print "Press 3 to add products"
			print "Press 4 to delete product"
			print "Press 5 to modify product"
			print "Press 6 to view orders placed"
			print "Press 7 to make shipment"
			print "Press 8 to confirm delivery"
			print "Press 9 to logout"
			print "Press 10 to exit"

			userInput = int(raw_input())

			if userInput == 1:
				adminUser.viewProducts()
			
			elif userInput == 2:
				adminUser.viewCustomerList()	

			elif userInput == 3:
				
				id_input =  int(round(time.time()))
				
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
				Id = int(raw_input())
				
				adminUser.deleteProduct(Id)

			elif userInput == 5:
				print "Enter product id "
				Id = int(raw_input())
				
				adminUser.modifyProduct(Id)
				
			elif userInput == 6:
				adminUser.viewOrdersPlaced()	

			elif userInput == 7:
				adminUser.makeShipment()
			
			elif userInput == 8:
				adminUser.confirmDelivery()	

			elif userInput == 9:
				isAdmin = False
				isRegisteredUser = False
				isUnregisteredUser = True

				guestUser = Guest(random.randint(1,101))
				runAsGuest(guestUser)	

			elif userInput == 10:

				adminFile = open('admin_file','wb')
				regUserFile = open('regUser_file','wb')
				prodListFile = open('product_file','wb')
				ordersListFile = open('orders_file','wb')
				
				pickle.dump(adminAccounts,adminFile)
				pickle.dump(registeredCustomers,regUserFile)
				pickle.dump(productsList,prodListFile)
				pickle.dump(ordersList,ordersListFile)
				
				adminFile.close()
				regUserFile.close()
				prodListFile.close()
				ordersListFile.close()

				sys.exit()	

			else :
				print "Invalid input"		

	except ValueError:
		print "Invalid Input"			

def runAsGuest(guestUser):

	os.system('clear')

	print "********* Welcome Guest ************"

	try: 

		while True:
			print "Press 1 to login as admin"
			print "Press 2 to login as registered user"
			print "Press 3 to view products"
			print "Press 4 to create a new account"
			print "Press 5 to exit"

			userInput = int(raw_input())

			if userInput == 1:
				user = adminLogin()
				if isAdmin == True and isUnregisteredUser == False:
					runAsAdmin(user)

			elif userInput == 2:
				flag, user = userLogin()
				if isRegisteredUser == True and isUnregisteredUser == False:		
					runasRegisteredUser(user)

			elif userInput == 3:
				guestUser.viewProduct()

			elif userInput == 4:	
				regUser = createNewAccount()
				print "New account created successfully"
				print "Please login as registered user"
				uType, user = userLogin()
				runasRegisteredUser(user)

			elif userInput == 5:

				adminFile = open('admin_file','wb')
				regUserFile = open('regUser_file','wb')
				prodListFile = open('product_file','wb')
				ordersListFile = open('orders_file','wb')
				
				pickle.dump(adminAccounts,adminFile)
				pickle.dump(registeredCustomers,regUserFile)
				pickle.dump(productsList,prodListFile)
				pickle.dump(ordersList,ordersListFile)
				
				adminFile.close()
				regUserFile.close()
				prodListFile.close()
				ordersListFile.close()

				sys.exit()
			else:
				print "Invalid input"	
	
	except ValueError:
		print "Invalid Input"			

def runasRegisteredUser(registeredUser):
	
	os.system('clear')

	print "******** Welcome ",registeredUser.name,"************"
	
	try:

		while True:		
			print "Press 1 to buy product"
			print "Press 2 to view products"
			print "Press 3 to view cart"
			print "Press 4 to add product to cart"
			print "Press 5 to delete product from cart"
			print "Press 6 to make payment"
			print "Press 7 to view products bought"
			print "Press 8 to view payment history"
			print "Press 9 to logout"
			print "Press 10 to exit"

			userInput = int(raw_input())

			if userInput == 1:
				registeredUser.buyProduct()
			elif userInput == 2:
				registeredUser.viewProduct()

			elif userInput == 3:
				registeredUser.viewCart()	
					
			elif userInput == 4:
				print "Enter product id "
				productId = int(raw_input())
				
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
				productId = int(raw_input())
				
				print "Enter quantity"
				quantity = int(raw_input())

				registeredUser.deleteFromCart(productId,quantity,True)
					
			elif userInput == 6:
				print "Enter your card type"
				cardType = raw_input()

				print "Enter card number"
				cardNumber = raw_input()

				payment = Payment(registeredUser.Id,registeredUser.name,cardType,cardNumber)
				registeredUser.makePayment(payment)
			
			elif userInput == 7:

				registeredUser.viewProductsBought()

			elif userInput == 8:
			
				registeredUser.viewPaymentHistory()	

			elif userInput == 9:
				isAdmin = False
				isRegisteredUser = False
				isUnregisteredUser = True

				guestUser = Guest(random.randint(1,101))
				runAsGuest(guestUser)

			elif userInput == 10:

				adminFile = open('admin_file','wb')
				regUserFile = open('regUser_file','wb')
				prodListFile = open('product_file','wb')
				ordersListFile = open('orders_file','wb')
				
				pickle.dump(adminAccounts,adminFile)
				pickle.dump(registeredCustomers,regUserFile)
				pickle.dump(productsList,prodListFile)
				pickle.dump(ordersList,ordersListFile)
				
				adminFile.close()
				regUserFile.close()
				prodListFile.close()
				ordersListFile.close()

				sys.exit()	
			else:
				print "Invalid input"	
	except ValueError:
		print "Invalid input"			

def main():

	os.system('clear')

	global isAdmin
	global isRegisteredUser	
	global isUnregisteredUser

	try:

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
				ordersListFile = open('orders_file','wb')
				
				pickle.dump(adminAccounts,adminFile)
				pickle.dump(registeredCustomers,regUserFile)
				pickle.dump(productsList,prodListFile)
				pickle.dump(ordersList,ordersListFile)
				
				adminFile.close()
				regUserFile.close()
				prodListFile.close()
				ordersListFile.close()

				sys.exit()

			else:
				print "Invalid input"
	except ValueError:
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
	ordersListFile = open('orders_file','a')

	adminFile.close()
	regUserFile.close()
	prodListFile.close()
	ordersListFile.close()

	adminFile = open('admin_file','rb')
	regUserFile = open('regUser_file','rb')
	prodListFile = open('product_file','rb')
	ordersListFile = open('orders_file','rb')

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

	try:
		ordersList = pickle.load(ordersListFile)
	except EOFError:
		ordersList = []		


	
	adminFile.close()
	regUserFile.close()
	prodListFile.close()
	ordersListFile.close()

	adminUser = Admin(1,"prakash","q")
	adminAccounts.append(adminUser)

	isAdmin = False
	isUnregisteredUser = True
	isRegisteredUser = False

	main()
