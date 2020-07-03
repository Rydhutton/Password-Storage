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
# Add SQL Lite database for storing hash key pairs
# Remove key from object class and read from db when loading account


class Account:
	def __init__(self, username, password):
		self.username = username
		self.password = password.encode('utf_8')
		self.salt = os.urandom(16)
		self.password = self.password + self.salt
		self.key = Fernet.generate_key()
		self.sites = {}
		self.authenticated = False
		cipher = Fernet(self.key)
		self.password = cipher.encrypt(self.password)



	def enc(self, cipher):
		# TO DO
		# Salt website passwords
		if self.authenticated == False:
			for key in self.sites:
				pwd = self.sites[key]
				pwd = pwd.encode('utf_8')
				self.sites[key] = cipher.encrypt(pwd)
		elif self.authenticated == True:
			for key in self.sites:
				pwd = self.sites[key]
				pwd = cipher.decrypt(pwd)
				self.sites[key] = pwd.decode('utf_8')


	def login(self, pwd, key):
		pwd = pwd.encode('utf_8')
		if self.authenticated == False:
			cipher = Fernet(key)
			pwd = pwd + self.salt
			if cipher.decrypt(self.password) == pwd:
				self.authenticated = True
				self.enc(cipher)
				print("authenticated, welcome.")
			else:
				print("incorrect password")
		else:
			print("you have already authenticated")


	def logout(self, key):
		if self.authenticated == True:
			self.authenticated = False
			self.enc(Fernet(key))
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


	def hash(self):
		pass
