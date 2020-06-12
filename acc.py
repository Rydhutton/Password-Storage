from cryptography.fernet import Fernet

import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# 2 options
# 1 - we create a superclass "database" that manages all accounts and does the pickling for us
# 2 - we create all the functions within our main.py that pickles and handles all accounts

# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet


# TO DO
# Store keys separate from object files using some hashing method
# Add SQL Lite database for storing passwords


class Account:
	def __init__(self, username, password):
		self.username = username
		self.password = password.encode('utf_8')
		self.salt = os.urandom(16)
		#print(self.password)
		#self.salt = self.salt.encode('utf_8')
		self.password = self.password + self.salt
		#print(self.password)
		self.key = Fernet.generate_key()
		#self.cipher = Fernet(self.key)
		self.sites = {}
		self.authenticated = False
		self.enc()



	def enc(self):
		#will need to encrypt all info besides username and key
		cipher = Fernet(self.key)
		self.password = cipher.encrypt(self.password)
		#print(self.password)



	def dec(self):
		cipher = Fernet(self.key)
		#self.password = cipher.decrypt(self.password)



	def login(self, pwd):
		pwd = pwd.encode('utf_8')
		if self.authenticated == False:
			cipher = Fernet(self.key)
			#print(pwd)
			pwd = pwd + self.salt
			#print(pwd)
			if cipher.decrypt(self.password) == pwd:
			#if cipher.decrypt(self.password) == pwd:
				#self.password = cipher.decrypt(self.password)
				self.authenticated = True
				print("authenticated, welcome.")
			else:
				print("incorrect password")
		else:
			print("you have already authenticated")



	def logout(self):
		if self.authenticated == True:
			#self.enc()
			self.authenticated = False
			print("You have been logged out")



	def addSite(self, website, password):
		if self.authenticated == False:
			print("Please login before adding a new site")
		else:
			self.sites[website] = password



	def search(self, keyword):
		if self.authenticated == False:
			print("Please login before adding a new site")
		else:
			try:
				print(self.sites[keyword])
			except:
				print("no match found")
