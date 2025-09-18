import tkinter as tk
from tkinter import messagebox # It needs to be imported as it's another module (not a class)
import random
import pyperclip

COLOR_WHITE = "#ffffff"
WEBSITE_PREFIX = "https://"
USERNAME_EXAMPLE = "your_email@example.com"
FILE_PATH = "data.txt"

window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# ------------------------------------------------------------------------------------------------------------------------------------- Functions
def clear_fields():
    input_password.delete(0, tk.END)

    input_username.delete(0, tk.END)
    input_username.insert(0, USERNAME_EXAMPLE)

    input_website.delete(0, tk.END)
    input_website.insert(tk.END, WEBSITE_PREFIX)
    input_website.focus()


def validate_fields(website, username, password):
    if website == "" or website == WEBSITE_PREFIX:
        messagebox.showwarning(title="Invalid Website!", message="Please enter a Website!")
        input_website.focus()
    elif username == "" or username == USERNAME_EXAMPLE:
        messagebox.showwarning(title="Invalid Username!", message="Please enter a Username!")
        input_username.focus()
    elif password == "":
        messagebox.showwarning(title="Invalid Password!", message="Please enter a Password!")
        input_password.focus()
    else:
        return True

    return False


def save():
    website = input_website.get()
    username = input_username.get()
    password = input_password.get()

    if not validate_fields(website, username, password):
        return

    confirmation = messagebox.askokcancel(title=website, message=f"These are the details entered: \n\n * Email: {username} \n * Password: {password} \n\nIs it ok to save?")
    if not confirmation:
        return

    records = []
    found = False

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            for row in file:
                row = row.strip()
                if not row:  # Skip empty lines
                    continue
                row_website, row_username, row_password = row.split(" | ")
                if row_website == website and row_username == username:
                    messagebox.showinfo(title="Entry already exists", message="This account already exists! \n\nThe password will be updated...")
                    records.append(f"{website} | {username} | {password}")
                    found = True
                else:
                    records.append(row)
    except FileNotFoundError:  # In case the file doesn't exist
        pass

    if not found: #Then just append it to the file
        with open("data.txt", "a") as file:
            file.write(f"{website} | {username} | {password}\n")
    else: # Overwrite the file's content with the new records
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            file.write("\n".join(records) + "\n")

    clear_fields()


def generate_password(): # Password generator project, adapted from day 5

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_numbers = random.randint(2, 4)
    nr_symbols = random.randint(2, 4)

    list_of_characters  = [random.choice(letters) for _ in range(nr_letters)]
    list_of_characters += [random.choice(numbers) for _ in range(nr_numbers)]
    list_of_characters += [random.choice(symbols) for _ in range(nr_symbols)]

    random.shuffle(list_of_characters)
    password = "".join(list_of_characters)

    input_password.delete(0, tk.END)
    input_password.insert(0, password)

    # Copy password to clipboard
    pyperclip.copy(password)

# ---------------------------------------------------------------------------------------------------------------------------------------- Canvas
canvas = tk.Canvas(width=200, height=200)
img_background = tk.PhotoImage(file="logo.png")
canvas.create_image( 100, 100, image=img_background) # The first two numbers are the x and y position of the canvas
canvas.grid(row=0, column=0, columnspan=3)

# --------------------------------------------------------------------------------------------------------------------------------------- Website
label_website = tk.Label(text="Website:")
label_website.grid(row=1, column=0, pady=5)

input_website = tk.Entry(width=39)
input_website.grid(row=1, column=1, columnspan=2, sticky=tk.W)

# -------------------------------------------------------------------------------------------------------------------------------------- Username
label_username = tk.Label(text="Email/Username:")
label_username.grid(row=2, column=0, pady=5)

input_username = tk.Entry(width=39)
input_username.grid(row=2, column=1, columnspan=2, sticky=tk.W)

# -------------------------------------------------------------------------------------------------------------------------------------- Password
label_password = tk.Label(text="Password:")
label_password.grid(row=3, column=0, pady=5)

input_password = tk.Entry(width=21)
input_password.grid(row=3, column=1, sticky=tk.W)

button_generate = tk.Button(text="Generate password", command=generate_password)
button_generate.grid(row=3, column=2, sticky=tk.W, pady=5)

# ------------------------------------------------------------------------------------------------------------------------------------------- Add

button_add = tk.Button(text="Add", width=33, command=save)
button_add.grid(row=4, column=1, columnspan=2, sticky=tk.W)

# -----------------------------------------------------------------------------------------------------------------------------------------------
clear_fields()
window.mainloop()