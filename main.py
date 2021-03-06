import acc as Account
from cryptography.fernet import Fernet
import base64
import pickle
import time
from tkinter import *
import sqlite3
from sqlite3 import Error


def sql_init():
	db_con = sqlite3.connect('user.db')
	db = db_con.cursor()
	db.execute("""CREATE TABLE users (
		id text,
		key text
		)""")
	db_con.commit()
	db_con.close()


def sql_user_cypher(username):
	# this can be changed to whatever the end user wishes, no repetition tho.
	di = {'a':'01','b':'02','c':'03','d':'04','e':'05','f':'06','g':'07','h':'08','i':'09','j':'10',
			'k':'11','l':'12','m':'13','n':'14','o':'15','p':'16','q':'17','r':'18','s':'19','t':'20',
			'u':'21','v':'22','w':'23','x':'24','y':'25','z':'26'}
	uid = ""
	for char in username:
		uid += di[char]
	return uid


def sql_add_user(account):
	db_con = sqlite3.connect('user.db')
	db = db_con.cursor()
	uid = sql_user_cypher(account.username)
	db.execute("INSERT INTO users VALUES (?, ?)", (uid, account.key))
	db_con.commit()
	db_con.close()


def sql_load_user(uid):
	db_con = sqlite3.connect('user.db')
	db = db_con.cursor()
	db.execute("SELECT * FROM users WHERE id=?", (uid,))
	id_key = db.fetchall()
	db_con.close()
	return id_key[0][1]


def save_account(account):
	sql_add_user(account)
	if account.authenticated == True:
		account.logout(account.key)

	account.key = None

	userfile = account.username + ".obj"
	file = open(userfile, 'wb')
	pickle.dump(account, file)
	file.close()


def load_account(account_name):
	userfile = account_name + ".obj"
	file = open(userfile, 'rb')
	account = pickle.load(file)
	file.close()
	user_id = sql_user_cypher(account_name)
	key = sql_load_user(user_id)
	account.key = key
	return account


def initialize():
	msg = ["*"] * 25
	for x in msg:
		print(x, end="", flush=True)
		time.sleep(0.05)
	print("")


def gui():
	#TO DO
	#Fill out try/except statements for incorrect logins/usernames
	#Implement logout

	#https://www.youtube.com/watch?v=YXPyB4XeYLA

	root = Tk()

	root.geometry("170x250")
	root.title("Account Manager")

	def login_click():

		top = Toplevel()

		acc = load_account(acc_entry.get())
		pwd = pwd_entry.get()
		acc.login(pwd, acc.key)

		if acc.authenticated == True:
			top.title(acc.username)
			login_info_label = Label(top, text="Successfully Authenticated")
			login_info_label.grid(row=0, column=0)
			count = 1
			for site in acc.sites:
				acinfo = site + " | pwd: " + acc.sites[site]
				info_label = Label(top, text=acinfo)
				info_label.grid(row=count, column=0, padx=0)
				count += 1

			add_site_label = Label(top, text="Add Site:")
			website_entry = Entry(top, width=25, borderwidth=5)
			web_pwd_entry = Entry(top, width=25, borderwidth=5)
			add_site_label.grid(row=0, column=1)
			website_entry.grid(row=1, column=1, pady=2, padx=5)
			web_pwd_entry.grid(row=2,column=1, pady=2, padx=5)

			def add_site_click():
				website = website_entry.get()
				website_pwd = web_pwd_entry.get()
				acc.addSite(website, website_pwd)
				# save account should be when user logs out
				save_account(acc)

			add_site_button = Button(top, text="Add Site", command=add_site_click, fg="black", bg="gray")
			add_site_button.grid(row=3, column=1, pady=2)

			top.mainloop()
		else:
			top.title("Incorrect Password")
			login_info_label = Label(top, text="Incorrect Password")
			login_info_label.grid(row=0, column=0, padx=5, pady=5)


	def logout_click():
		pass


	def create_acc_click():

		top = Toplevel()
		top.title("New Account")

		ac_creation_label = Label(top, text="Create a new account: ")
		ac_creation_entry = Entry(top, width=25, borderwidth=5)
		pw_creation_entry = Entry(top, width=25, borderwidth=5)

		ac_creation_label.grid(row=1, column=0, pady=2)
		ac_creation_entry.grid(row=2, column=0, pady=2)
		pw_creation_entry.grid(row=3, column=0, pady=2)

		def new_acc_click():
			usrname = ac_creation_entry.get()
			pwd = pw_creation_entry.get()
			acc = Account.Account(usrname, pwd)
			save_account(acc)
			top.destroy()

		new_acc_button = Button(top, text="Create account", command=new_acc_click, fg="black", bg="gray")
		new_acc_button.grid(row=4, column=0, pady=10)

		top.mainloop()


	acc_label = Label(root, text="Account")
	acc_entry = Entry(root, width=25, borderwidth=5)
	pwd_label = Label(root, text="Password")
	pwd_entry = Entry(root, width=25, borderwidth=5)
	sites_label = Label(root, text="Sites")

	spacer_1 = Label(root)

	login_button = Button(root, text="Login", command=login_click, fg="black", bg="gray")
	logout_button = Button(root, text="Logout", command=logout_click, fg="black", bg="gray")
	create_acc_button = Button(root, text="Create account", command=create_acc_click, fg="black", bg="gray")

	spacer_1.grid(row=0, column=0)

	acc_label.grid(row=1, column=0,pady=2)
	acc_entry.grid(row=2, column=0, padx=5, pady=2)

	pwd_label.grid(row=3, column=0, pady=2)
	pwd_entry.grid(row=4, column=0, padx=5, pady=2)

	login_button.grid(row=5, column=0, pady=10)
	create_acc_button.grid(row=6, column=0, pady=15)

	root.mainloop()

def main():

	# used for debugging functions.
	pass


if __name__ == "__main__":
	gui()