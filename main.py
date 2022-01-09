from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- SEARCH WEBSITE INFO ------------------------------ #
def search():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    else:
        website = website_entry.get()
        if website in data:
            password_window = Toplevel(window)
            password_window.title(website)
            email_user = data[website]['email_user']
            password = data[website]['password']
            text = Text(password_window, height=5, width=70)
            text.insert(END, f"email: {email_user}\npassword: {password}")
            text.config(state=DISABLED)
            text.grid(row=0, column=0)
            password_window.grab_set()
            # messagebox.showinfo(title=website, message=f"email: {email_user}"
            #                                            f"\npassword: {password}")
        else:
            messagebox.showerror(title="Error", message=f"No Details For {website} Exists")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for char in range(nr_letters)]
    password_list += [random.choice(symbols) for char in range(nr_symbols)]
    password_list += [random.choice(numbers) for char in range(nr_numbers)]

    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_button_pressed():
    website = website_entry.get()
    email_user = email_user_entry.get()
    password = password_entry.get()
    new_data = {
        website:
            {
                "email_user": email_user,
                "password": password
            }
    }
    if len(website) == 0 or len(email_user) == 0 or len(password) == 0:
        messagebox.showinfo(title="oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            email_user_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()
            messagebox.showinfo(title="Well Done", message="You managed to add a new account")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_user_label = Label(text="Email/Username:")
email_user_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

website_entry = Entry()
website_entry.focus()
website_entry.grid(column=1, row=1, sticky=EW)

email_user_entry = Entry()
email_user_entry.grid(column=1, row=2, columnspan=2, sticky=EW)

password_entry = Entry()
password_entry.grid(column=1, row=3, sticky=EW)

generate_pass_button = Button(text="Generate Password", command=generate_password)
generate_pass_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=add_button_pressed)
add_button.grid(column=1, row=4, columnspan=2, sticky=EW)

search_button = Button(text="Search", command=search)
search_button.grid(column=2, row=1, sticky=EW)

window.mainloop()
