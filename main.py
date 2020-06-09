import acc as Account
from cryptography.fernet import Fernet
import base64
import pickle
import time


def save_account(account):
	#consider saving a new file for each account?
	if account.authenticated == True:
		account.logout()
	userfile = account.username + ".obj"
	file = open(userfile, 'wb')
	pickle.dump(account, file)
	file.close()

def load_account(account_name):
	userfile = account_name + ".obj"
	file = open(userfile, 'rb')
	accounts = pickle.load(file)
	file.close()
	return accounts

def initialize():
	msg = ["*"] * 25
	for x in msg:
		print(x, end="", flush=True)
		time.sleep(0.05)
	print("")

def main():
	
	#initialize()
	#a1 = Account.Account("rhutton", "pizza")
	#a1.login("pizza")
	#save_account(a1)
	a2 = load_account("rhutton")
	print(a2.username)
	a2.login("pizza")
	print(a2.password)


if __name__ == "__main__":
	main()