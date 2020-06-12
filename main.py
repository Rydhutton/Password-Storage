import acc as Account
from cryptography.fernet import Fernet
import base64
import pickle
import time
from tkinter import *


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


def gui():

	#TO DO
	#Format site info into something more readable
	#Fill out try/except statements for incorrect logins/usernames

	#https://www.youtube.com/watch?v=YXPyB4XeYLA

	root = Tk()

	def login_click():
		#attempt to login here
		#login_label = Label(root, text="success")
		#login_label.pack()
		acc = load_account(acc_entry.get())
		pwd = pwd_entry.get()
		acc.login(pwd)
		login_info_label = Label(root, text="Success")
		login_info_label.grid(row=1, column=4)
		info_label = Label(root, text=acc.sites)
		info_label.grid(row=1, column=1)



	acc_label = Label(root, text="Account")
	acc_entry = Entry(root, width=25, borderwidth=5)
	pwd_label = Label(root, text="Password")
	pwd_entry = Entry(root, width=25, borderwidth=5)
	sites_label = Label(root, text="Sites")

	login_button = Button(root, text="Login", command=login_click, fg="black", bg="gray")

	acc_label.grid(row=0, column=0)
	acc_entry.grid(row=0, column=1)
	pwd_label.grid(row=0, column=2)
	pwd_entry.grid(row=0, column=3)
	sites_label.grid(row=1, column=0)

	login_button.grid(row=0, column=4)

	root.mainloop()

def main():
	
	a = load_account("rhutton")
	b = load_account("vhugo")
	c = load_account("sinclair")

	pw = input("password:\n")

	a.login(pw)
	b.login(pw)
	c.login(pw)

if __name__ == "__main__":
	gui()