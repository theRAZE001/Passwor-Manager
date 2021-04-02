from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# Password Generator---------------------------------------------------------------------------------------------
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
               'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
               'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)

    password = "".join(password_list)
    # for char in password_list:
    #    password += char
    entry_password.delete(0, END)
    entry_password.insert(0, password)
    pyperclip.copy(password)


# Insert Into the txt File------------------------------------------------------------------------------------
def insert_data():
    website = (entry_website.get()).title()
    email = entry_email.get()
    password = entry_password.get()
    user_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    # string = website + " | " + email + " | " + password + "\n"
    if website != "" and email != "" and password != "":
        try:
            with open("data.json", "r") as data:  # if using string variable string !=" |  | \n"

                is_ok = messagebox.askokcancel(title=website,
                                               message=f"Are you sure you want to save the following details?\n"
                                                       f"email:{email}\n"
                                                       f" password:{password}")
                if is_ok:
                    # Reading from the json file
                    new_data = json.load(data)
                    # updating the json file
                    new_data.update(user_data)
                    with open("data.json", "w") as update:
                        # writing to the json file
                        json.dump(new_data, update, indent=4)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(user_data, file, indent=4)
        finally:
            lbl_confirm.config(text="Entry Successfully!", fg="green")
            entry_email.delete(0, END)
            entry_website.delete(0, END)
            entry_password.delete(0, END)
    else:
        messagebox.showwarning(title="warning", message="Enter all fields first!!")


# search data----------------------------------------------------------------------------------------------------
def search_data():
    try:
        with open("data.json", "r") as search:
            data_file = json.load(search)
            search_key = (entry_website.get()).title()
            if search_key in data_file:
                email = data_file[search_key]["email"]
                password = data_file[search_key]["password"]
                message = f"email : {email}\n password : {password}"
                messagebox.showinfo(title=search_key, message=message)
            else:
                messagebox.showwarning(title=search_key, message=f"oops! No data exists for {search_key}.")

    except FileNotFoundError:
        messagebox.showwarning(title="Error!", message="oops! no datafile was found.")
    finally:
        lbl_confirm.config(text="Entry Successful!")


window = Tk()
window.config(padx=30, pady=30)
window.title("Password Manager by Rakesh")
window.iconbitmap(r'favicon.ico')

padlock = PhotoImage(file="padlock.png")
canvas = Canvas(window, height=132, width=132)
canvas.create_image(66, 66, image=padlock)
canvas.grid(row=0, column=1)

# Labels
lbl_website = Label(text="Website:")
lbl_website.grid(row=1, column=0)

lbl_email = Label(text="Email/Username:")
lbl_email.grid(row=2, column=0)

lbl_password = Label(text="Password:")
lbl_password.grid(row=3, column=0)

lbl_confirm = Label(text="")
lbl_confirm.grid(row=5, column=1)

# Entry

entry_website = Entry(width=21)
entry_website.focus()
entry_website.grid(row=1, column=1)

entry_email = Entry(width=40)
entry_email.grid(row=2, column=1, columnspan=2)

entry_password = Entry(width=21)
entry_password.grid(row=3, column=1)
# Buttons

btn_generate = Button(text="Generate Password", command=generate_password)
btn_generate.grid(row=3, column=2)
btn_generate.config(padx=0)

btn_add = Button(text="Add", width=34, command=insert_data)
btn_add.grid(row=4, column=1, columnspan=2)

btn_search = Button(text="Search", width=14, command=search_data)
btn_search.grid(row=1, column=2)

window.mainloop()
