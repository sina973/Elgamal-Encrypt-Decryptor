import subprocess


def import_or_install(package):
    try:
        return __import__(package)
    except ImportError:
        subprocess.check_call(["python", "-m", "pip", "install", package])


tkinter = import_or_install("tkinter")

from tkinter import *
from tkinter import filedialog
from Elgamal import Elgamal
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk


def popup_window():             # Pop up window for configuring keys
    dictionary = {"pu": False, "pr": False, "p": False, "q": False, "g": False}

    def submit_keys():          # For submitting key locations from user entries
        state = True
        if dictionary["pr"] is False:       # For detecting that user didn't browse a file for keys
            temp = ent1.get()
            if temp != "":
                elgamal.prkey = int(temp)
            else:
                state = False

        if dictionary["pu"] is False:           # For detecting that user didn't browse a file for keys
            temp = ent2.get()
            if temp != "":
                elgamal.pukey = int(temp)
            else:
                state = False

        if dictionary["p"] is False:        # For detecting that user didn't browse a file for keys
            temp = ent3.get()
            if temp != "":
                elgamal.p = int(temp)
            else:
                state = False

        if dictionary["q"] is False:        # For detecting that user didn't browse a file for keys
            temp = ent4.get()
            if temp != "":
                elgamal.q = int(temp)
            else:
                state = False

        if dictionary["g"] is False:        # For detecting that user didn't browse a file for keys
            temp = ent5.get()
            if temp != "":
                elgamal.g = int(temp)
            else:
                state = False

        for x in dictionary.keys():         # Handle the situation that user want to submit keys but
            if x is False:                      # didn't enter a value aor browse a key file
                state = False
                messagebox.showerror("Error", "Please enter a correct number for key values needed or browse a text "
                                              "file; or just press 'generate keys' for generating keys automatically")
                win.wm_attributes("-topmost", 1)

        if state is False:
            messagebox.showerror("Error", "Please enter a correct number for key values needed or browse a correct "
                                          "text file; or just press 'generate keys' for generating keys automatically")
            win.lift()

        else:
            win.destroy()

    def PRfileDialog():             # Like "fileDialog" function, this function browse a file for private key
        filename = filedialog.askopenfilename(initialdir=elgamal.saving_path, title="Select A File",
                                              filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        if filename != "":
            ent1.configure(state="disabled")        # Disabling entry feild when browsing
        dictionary["pr"] = True
        PR_txt = read_message(filename)
        if PR_txt is not None:
            elgamal.prkey = int(PR_txt)
            print("Elgamal P: ", elgamal.prkey)
        win.lift()

    def PUfileDialog():         # Like "fileDialog" function, this function browse a file for public key
        filename = filedialog.askopenfilename(initialdir=elgamal.saving_path, title="Select A File",
                                              filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        if filename != "":
            ent2.configure(state="disabled")        # Disabling entry field when browsing
        dictionary["pu"] = True
        PU_txt = read_message(filename)
        if PU_txt is not None:
            elgamal.pukey = int(PU_txt)
            print("Elgamal P: ", elgamal.pukey)

        win.lift()

    def PQGfileDialog():      # Like "fileDialog" function, this function browse a file for P,Q, and G values
        filename = filedialog.askopenfilename(initialdir=elgamal.saving_path, title="Select A File",
                                              filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        pqg = read_message(filename)
        pqg = pqg.split(",")
        if len(pqg) < 3:
            messagebox.showerror("Error", "Please enter a correct number for P,Q and G or browse a correct text file; "
                                          "or just press 'generate keys' for generating keys automatically")

        elif filename != "":            # Disabling entry field when browsing
            ent3.configure(state="disabled")
            ent4.configure(state="disabled")
            ent5.configure(state="disabled")
            dictionary["p"] = dictionary["q"] = dictionary["g"] = True
            p = pqg[0]
            q = pqg[1]
            g = pqg[2]
            if p != "" and q != "" and g != "":
                elgamal.p = int(p)
                elgamal.q = int(q)
                elgamal.g = int(g)
            else:
                messagebox.showerror("Error", "Please browse a correct text file for P,Q and G; "
                                              "or just press 'generate keys' for generating keys automatically")
                win.lift()
            win.lift()

    def generate_keys():        # Generating keys automatically with help of "gen_keys" function in Elgamal class
        try:
            elgamal.gen_keys()
            messagebox.showinfo("Message", "Keys have been generated and saved in saving location ")
            win.destroy()
        except TypeError as e:
            messagebox.showerror("Error", "Please define a correct path for saving location "
                                          "in the 'Saving Path' section")
            win.lift()

    win = Toplevel()                # Creating a window on top for the keys
    win.wm_title("Configure Key")
    frame1 = Frame(win)
    frame1.pack(side=TOP)
    frame2 = Frame(win)
    frame2.pack()
    frame3 = Frame(win)
    frame3.pack(side=BOTTOM)

    l1 = Label(frame1, text="Enter your private Key")   # Label of the entry of private key
    l1.grid(row=0, column=0)
    ent1 = Entry(frame1)            # Entry feild for private key
    ent1.grid(row=0, column=1)
    browse1 = Button(frame1, text="Browse A File", command=PRfileDialog)    # A button for browsing a file for private
                                                                            #  key with "PRfileDialog" function
    browse1.grid(column=2, row=0)
    l2 = Label(frame1, text="Enter your public Key")    # Lablel of the entry of public key
    l2.grid(row=1, column=0)
    ent2 = Entry(frame1)            #entry feild for public key
    ent2.grid(row=1, column=1)
    browse2 = Button(frame1, text="Browse A File", command=PUfileDialog)     # A button for browsing a file for public
                                                                            # key with "PUfileDialog" function
    browse2.grid(column=2, row=1)

    l3 = Label(frame2, text="Enter a prime number as P")        # Label of the entry of P value
    l3.grid(row=0, column=0)
    ent3 = Entry(frame2)                                    # Entry field for P value
    ent3.grid(row=0, column=1)
    l4 = Label(frame2, text="Enter a prime number as Q")        # Label of the entry of Q value
    l4.grid(row=1, column=0)
    ent4 = Entry(frame2)                                    # Entry field for Q value
    ent4.grid(row=1, column=1)
    l5 = Label(frame2, text="Enter a number as G")          # Label of the entry of G value
    l5.grid(row=2, column=0)
    ent5 = Entry(frame2)                                    # Entry field for G value
    ent5.grid(row=2, column=1)
    browse3 = Button(frame2, text="Browse A File", command=PQGfileDialog)       # A button for browsing a file for P, Q,
                                                                # and G  values with "PQGfileDialog" function
    browse3.grid(column=2, row=1)

    b = Button(frame3, text="Submit Keys", command=submit_keys)         # A button for submitting keys
    b.grid(row=0)                                                       # with "submit_key" function
    ex = Button(frame3, text="Generate Keys", command=generate_keys)    # A button for generating keys with
    ex.grid(row=1)                                                      # "generate_keys" function


def popup_window2():    # A pop up window for configuring saving location
    state = False

    def submit_location():          # A function for submitting location as user entered
        if state is True:
            win.destroy()       # Check if user have browsed a file
        else:
            location = ent1.get()       # Reading from an entry for location if user haven't browse a file
            if location != "":
                elgamal.saving_path = location
            win.destroy()

    def folderDialog():         #A function for browsing a folder for saving path
        foldername = filedialog.askdirectory(initialdir="/", title="Select A Folder")
        if foldername != "":
            ent1.configure(state="disabled")
        elgamal.saving_path = foldername
        win.destroy()

    win = Toplevel()                # Creating a pop up window for configuring saving location
    win.wm_title("Configure Key")
    frame1 = Frame(win)
    frame1.pack(side=TOP)
    frame2 = Frame(win)
    frame2.pack()

    l1 = Label(frame1, text="Saving Location")      # Label for saving location entry
    l1.grid(row=0, column=0)
    ent1 = Entry(frame1)            # An entry for entering saving location folder
    ent1.grid(row=0, column=1)
    if elgamal.saving_path is not None:         # Default path for saving location
        ent1.insert(END, elgamal.saving_path)
    browse1 = Button(frame1, text="Browse A Folder", command=folderDialog)  # A button for browsing a folder
    browse1.grid(row=0, column=2)                                           # with "folderDialog" function

    b = Button(frame2, text="Submit Location", command=submit_location)     # A button for submitting the location
    b.grid(row=0)                                                           # with "folderDialog" function


def fileDialog():               # Function for browsing

                    # Using Filedialog library and "askopenfilename" function from it for browsing
    filename = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                          filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    txt = read_message(filename)        # Using "read_message" for reading from a file
    if txt is not None:
        elgamal.message = txt
    print("Original Message :", elgamal.message)


def read_message(file_path):        # Read message from a file when browsing
    try:                # Catching exception like as "File not found"
        f = open(file_path, "r")
        if f.mode == "r":
            message = f.read()
            f.close()
        return message

    except OSError as e:
        messagebox.showerror("Error", "File Not Found")
        return None


def submit_message():               # Submitting message entered from user
    message = entry1.get(1.0, END)
    if message != "\n":
        elgamal.message = message
        print("Original Message :", elgamal.message)
    else:
        messagebox.showwarning("Warning", "Please enter text or browse a text file")


def Help():                         # Function that Operate when clicking on help option on the top
    win = Toplevel()                # Creating a new window for help pop up window
    win.wm_title("Help")
    frame1 = Frame(win)
    frame1.pack(side=TOP)
    frame2 = Frame(win)
    frame2.pack()

    tab_control = ttk.Notebook(frame1)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="First Step")        # Add First step tab
    tab_control.add(tab2, text="Second Step")       # Add Second step tab
    tab_control.pack(expand=1, fill="both")

    step1 = Text(tab1)                  # Adding text for the first step
    step1.pack()
    step1.insert(END, "In the very first step you should adjust the saving location for saving encryption/decryption "
                      "files or keys.\nThen you should adjust keys needed for encryption or decryption"
                      "There are five field that you should adjust in the key section to begin the encrypt/decrypt.\n"
                      "The first field is your private key that is a big integer that you should either enter in a "
                      "text field or browse it from a text file. Second is the destination public key that you should "
                      "adjust. In the third step here, you should configure three integers as P,Q, and G that are"
                      " agreed between you and the distination you want to send this encryption or between you and "
                      "the source that you have recieved the message from.\nIf you don't have these keys, "
                      "fortunately, there is an option for you. You can press 'Generate key' button for generation "
                      "these keys automatically. They will be save in the saving location you have adjusted.")
    step1.configure(state="disable")

    step2 = Text(tab2)          #Adding text for the second step
    step2.pack()
    step2.insert(END, "When you adjusted keys needed for encryption/decryption, you do not have much left "
                      "for running this program.\nYou should provide your text for encryption/decryption. You can "
                      "either browse it from a text box or type it into the text box provided in the main "
                      "window of program. You should pay attention that if you have typed your message, you should"
                      " press 'OK' button next to the text box for saving your text as a your message.\n Then you "
                      "can either press 'Encrypt' for encryption or 'Decrypt' for decryption of your message. "
                      "By the time you did that encrypted/decrypted of your message will be saved in the location "
                      "you have entered.\n There is nothing left, you are done. Thank you for chosing this "
                      "application. We hope you enjoy it. :)")
    step2.configure(state="disable")



    b = Button(frame2, text="OK!", command=win.destroy)
    b.grid(row=0)


def Encrypt():              # Encrypt user's message using with encryption in the Elgamal class
    elgamal.encrypt()
    messagebox.showinfo("Message", "Message has been encrypted and saved in the saving location")


def Decrypt():              # Decrypt user's message using with decryption in the Elgamal class
    elgamal.decrypt()
    messagebox.showinfo("Message", "Message has been decrypted and saved in the saving location")           #Encrypt user's message using with encryption in the Elgamal class#Encrypt user's message using with encryption in the Elgamal class


elgamal = Elgamal()
window = Tk()
window.title("Encryption Program")
# window.geometry('300x200')

menu = Menu(window)                     # Configuring top menu
window.config(menu=menu)

file_menu = Menu(menu)                  # Adding "File" tab on the top in the top menu
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=fileDialog)

configure_menu = Menu(menu)             # Adding "Configure" tab on the top in the top menu
menu.add_cascade(label="Configure", menu=configure_menu)
configure_menu.add_command(label="Configure keys", command=popup_window)
configure_menu.add_command(label="Configure saving path", command=popup_window2)

menu.add_command(label="help", command=Help)        # Adding help tab in the top menu


label1 = Label(window, text="Enter your text")
label1.grid(row=0, sticky=E)
entry1 = scrolledtext.ScrolledText(window)          # Add entry for enring message from user
entry1.grid(row=0, column=1)
submit = Button(window, text="OK", command=submit_message)      # Add an "OK" button for submitting the message
submit.grid(row=0, column=2)                                    # That use submit_message function
browse = Button(window, text="Browse A File", command=fileDialog)  # Add a browse button which use fileDialog function
browse.grid(column=3, row=0)
button1 = Button(window, text="Configure keys", command=popup_window)       # Add a button for configuring keys
button1.grid(row=2, column=1)                                               # Using popup_window
button4 = Button(window, text="Saving Path", command=popup_window2)     # Add a button for saving
                                                                        # a path for saving location
button4.grid(row=3, column=1)                                               # Using popup_window2
button2 = Button(window, text="Encrypt", command=Encrypt)               # A button for encrypting process
button2.grid(row=4, column=0)
button3 = Button(window, text="Decrypt", command=Decrypt)               # A button for decrypting process
button3.grid(row=4, column=2)

window.mainloop()
