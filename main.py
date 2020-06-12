import acc as Account
from cryptography.fernet import Fernet
import base64
import pickle
import time
from tkinter import *


def save_account(account):
	#consider saving a new file for each account?
	print(account.password)
	if account.authenticated == True:
		account.logout()
	userfile = account.username + ".obj"
	file = open(userfile, 'wb')
	pickle.dump(account, file)
	file.close()
	print(account.password)


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
	#Add in gui to create accounts
	#Implement logout

	#https://www.youtube.com/watch?v=YXPyB4XeYLA

	#logged_in = False
	#active_acc = None

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
		count = 1
		for site in acc.sites:
			acinfo = site + " | pwd: " + acc.sites[site]
			info_label = Label(root, text=acinfo)
			info_label.grid(row=count, column=1, padx=0)
			count += 1
		#logged_in = True
		#active_acc = acc
		#info_label = Label(root, text=acc.sites)
		#info_label.grid(row=1, column=1)

	def logout_click():
		#active_acc.logout()
		#logged_in = False
		pass

	def create_acc_click():
		usrname = ac_creation_entry.get()
		pwd = pw_creation_entry.get()
		acc = Account.Account(usrname, pwd)
		save_account(acc)

	acc_label = Label(root, text="Account")
	acc_entry = Entry(root, width=25, borderwidth=5)
	pwd_label = Label(root, text="Password")
	pwd_entry = Entry(root, width=25, borderwidth=5)
	sites_label = Label(root, text="Sites")

	ac_creation_label = Label(root, text="Create a new account: ")
	ac_creation_entry = Entry(root, width=25, borderwidth=5)
	pw_creation_entry = Entry(root, width=25, borderwidth=5)

	login_button = Button(root, text="Login", command=login_click, fg="black", bg="gray")
	logout_button = Button(root, text="Logout", command=logout_click, fg="black", bg="gray")
	create_acc_button = Button(root, text="Create account", command=create_acc_click, fg="black", bg="gray")

	acc_label.grid(row=0, column=0)
	acc_entry.grid(row=0, column=1)
	pwd_label.grid(row=0, column=2)
	pwd_entry.grid(row=0, column=3)
	sites_label.grid(row=1, column=0)

	login_button.grid(row=0, column=4)
	logout_button.grid(row=2, column=4)

	ac_creation_label.grid(row=4, column=4)
	ac_creation_entry.grid(row=5, column=4)
	pw_creation_entry.grid(row=6, column=4)

	create_acc_button.grid(row=7, column=4)

	root.mainloop()

def main():
	
	a = Account.Account("jsmith", "password")
	a.login("password")
	a.addSite("facebook", "password1")
	a.addSite("gmail", "password2")
	a.addSite("instagram", "password3")
	a.addSite("youtube", "password4")
	print(a.password)
	save_account(a)
	print(a.password)
	a.login("password")

if __name__ == "__main__":
	gui()