"""
This is the solution for the COMP 437:
    -> Create a solution to implement steganography and cryptography in your own language of choice.

@author: KEVIN OMONDI OWIDI
@student id: S13/03168/18
@date: September 30/2022
"""

# Importing relevant libraries
import math
import tkinter as tk
from tkinter import ttk, WORD
from tkinter.font import Font
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import cv2

# global variables
SHIFT = 3


# Custom font
def set_font(size=14, weight="normal"):
    return Font(family="monospace",
                size=size,
                weight=weight)


# cipher message
def cipher(message) -> str:
    """
    This function converts plain text into cipher text using Ceaser cipher
    :param message: The plain text to be ciphered
    :return: A string of cipher text
    """
    shift = SHIFT

    cipher_text = ""

    for letter in message:
        if letter.isupper():
            letter_index = ord(letter) - ord("A")
            # Positive shift
            new_index = (letter_index + shift) % 26
            new_unicode = new_index + ord("A")
            new_character = chr(new_unicode)
            cipher_text = cipher_text + new_character
        elif letter.islower():
            letter_index = ord(letter) - ord("a")
            # Positive shift
            new_index = (letter_index + shift) % 26
            new_unicode = new_index + ord("a")
            new_character = chr(new_unicode)
            cipher_text = cipher_text + new_character
        else:
            # This preserves non-alphabetic character for readability
            cipher_text += letter

    return cipher_text


# decipher
def decipher(message) -> str:
    """
    This function deciphers the cipher text passed in as message parameter
    :param message: Cipher text to be deciphered
    :return: A string of plain text deciphered
    """
    shift = SHIFT

    plain_text = ""
    # Loop through every character in the text and convert it as per shift
    for letter in message:

        if letter.isupper():
            letter_index = ord(letter) - ord("A")

            # Negative shift
            new_index = (letter_index - shift) % 26
            new_unicode = new_index + ord("A")
            new_character = chr(new_unicode)
            plain_text = plain_text + new_character
        #     Since ASCII ranges with letter cases, check for lower case letters and convert appropriately
        elif letter.islower():
            letter_index = ord(letter) - ord("a")

            # Negative shift
            new_index = (letter_index - shift) % 26
            new_unicode = new_index + ord("a")
            new_character = chr(new_unicode)
            plain_text = plain_text + new_character
        else:
            # This preserves non-alphabetic character for readability
            plain_text += letter

    return plain_text


# Container canvas

class App(tk.Tk):
    """
    This is class that encapsulates the app.
    It defines basic properties such as window size, title and frames that for other subframe screens
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Steganography App")
        self.geometry('600x600')
        container = tk.Frame(self, height=600, width=500)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, EncryptPage, DecryptPage):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    """
    This function helps navigate different frames/screens
    """

    def show_frame(self, index):
        frame = self.frames[index]
        frame.tkraise()


class MainPage(tk.Frame):
    """
    Encapsulates widgets in the home/landing screen.
    It has the following widgets:
        Page header -> Informs the user on what action to take
        Do encrypt button: Load encryption screen
        Do decrypt button: Load decryption screen
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Choose to encrypt or decrypt", font=set_font(size=18, weight="bold"))
        label.pack(padx=10, pady=10)

        # We use the switch_window_button in order to call the show_frame() method as a lambda function
        encrypt_button = tk.Button(
            self,
            text="Do Encrypt",
            command=lambda: controller.show_frame(EncryptPage),
            justify="center",
            bg="grey",
            fg="white"
        )
        encrypt_button.pack(fill="both", expand=True, padx=10, pady=10)

        decrypt_button = tk.Button(
            self,
            text="Do Decrypt",
            command=lambda: controller.show_frame(DecryptPage),
            bg="black",
            fg="white"
        )
        decrypt_button.pack(fill="both", expand=True, padx=10, pady=10)


class EncryptPage(tk.Frame):
    """
        Encapsulates widgets in the Encryption screen.
        It has the following widgets:
            Page header -> Informs user on what to do
            Pick image button-> Select an image to use for encryption
            Image Frame -> Inserts image selected into the screen
            Message box -> Captures the text to be encrypted
            Encrypt button -> Button to confirm encryption
            Hidden label -> The label pops to confirm encryption successful
            Back button -> Returns to the home page
        """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.path_image = None
        self.label = tk.Label(self, text="Pick image and enter message", font=set_font(size=18, weight="bold"))
        self.label.pack(padx=10, pady=10)

        # Pick image button
        pick_image = tk.Button(
            self,
            text="Pick Image",
            command=self.pick_image,
            justify="center",
            bg="black",
            fg="white"
        )
        pick_image.pack(fill=tk.X, padx=10, pady=10, ipady=5, ipadx=5)

        # Image frame
        self.image_frame = tk.Frame(self, height=150, width=400)
        self.image_frame.pack(fill=tk.X, padx=2, pady=2, ipady=2, ipadx=2)

        # Message label
        tk.Label(self, text="Message").pack(padx=10)
        # Text input to be encrypted
        self.message_input_box = tk.Text(self, wrap=WORD, height=5)
        self.message_input_box.pack(fill=tk.X, padx=10, pady=10, ipady=5, ipadx=5)

        # Button to confirm encryption
        encrypt_confirm = tk.Button(
            self,
            text="Encrypt",
            command=self.encrypt,
            justify="center",
            bg="black",
            fg="white"
        )
        encrypt_confirm.pack(fill=tk.X, padx=10, pady=10, ipady=5, ipadx=5)

        switch_window_button = tk.Button(
            self, text="Go Back", command=lambda: controller.show_frame(MainPage),
            justify="center",
            bg="black",
            fg="white"

        )
        switch_window_button.pack(padx=10, pady=10, ipady=5, ipadx=5, side="right")

    # Handle button action
    def pick_image(self):
        image_display_size = 300, 300
        self.path_image = filedialog.askopenfilename()
        load_image = Image.open(self.path_image)
        # set the image into the GUI
        load_image.thumbnail(image_display_size, Image.ANTIALIAS)
        # Load image np array for efficient computation
        np_load_image = np.asarray(load_image)
        np_load_image = Image.fromarray(np.uint8(np_load_image))
        render = ImageTk.PhotoImage(np_load_image)
        img = tk.Label(self.image_frame, image=render)
        img.image = render
        img.pack(padx=5, pady=5, ipady=5, ipadx=5, side="left")

    # DO encrypt the image
    def encrypt(self):
        data = self.message_input_box.get(1.0, "end-1c")
        print(f"The plain text entered is {data}")

        # Encrypt the message input using ceaser cipher
        data = cipher(data)
        print(f"The cipher text converted is {data}")

        # load the image
        img = cv2.imread(self.path_image)
        # break the image into its character level. Represent the characters in ASCII.

        data = [format(ord(i), '08b') for i in data]
        _, width, _ = img.shape
        # algorithm to encode the image
        pix_req = len(data) * 3

        row_req = pix_req / width
        row_req = math.ceil(row_req)

        count = 0
        char_count = 0

        for i in range(row_req + 1):
            while count < width and char_count < len(data):
                char = data[char_count]
                char_count += 1
                for index_k, k in enumerate(char):
                    if ((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (
                            k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                        img[i][count][index_k % 3] -= 1
                    if index_k % 3 == 2:
                        count += 1
                    if index_k == 7:
                        if char_count * 3 < pix_req and img[i][count][2] % 2 == 1:
                            img[i][count][2] -= 1
                        if char_count * 3 >= pix_req and img[i][count][2] % 2 == 0:
                            img[i][count][2] -= 1
                        count += 1
            count = 0
        # Step 6
        # Write the encrypted image into a new file
        cv2.imwrite("output.png", img)
        # Display the success label.
        success_label = tk.Label(self, text="Encryption Complete!", font=set_font())
        success_label.pack()


class DecryptPage(tk.Frame):
    """
    Encapsulates widgets in the Decryption screen.
    It has the following widgets:
        Page header -> Informs user on what to do
        Pick image button-> Select an encrypted image to decrypt
        Image Frame -> Inserts image selected into the screen
        Message box -> Displays the text to be decrypted
        Decrypt button -> Button to confirm decryption
        Back button -> Returns to the home page
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.message = None
        self.message_box = None
        self.decrypted_message = None
        self.img = None
        self.render = None
        self.np_load_image = None
        self.load_image = None
        self.path_image = None
        self.image_display_size = None
        label = tk.Label(self, text="Pick encrypted image to decrypt", font=set_font(size=18, weight="bold"))
        label.pack(padx=10, pady=10)

        # Pick image button
        pick_image = tk.Button(
            self,
            text="Pick encrypted Image",
            command=self.pick_img_onclick,
            justify="center",
            bg="black",
            fg="white"
        )
        pick_image.pack(fill=tk.X, padx=10, pady=10, ipady=5, ipadx=5)

        # Image frame
        self.image_frame = tk.Frame(self, height=150, width=400)
        self.image_frame.pack(fill=tk.X, padx=2, pady=2, ipady=2, ipadx=2)

        # Message label
        tk.Label(self, text="Decrypted Message").pack(padx=10)

        self.message_frame = tk.Frame(self, height=150, background="gray")
        self.message_frame.pack(fill=tk.X, padx=2, pady=2, ipady=2, ipadx=2)

        decrypt_btn = tk.Button(
            self, text="Decrypt Image", command=self.decrypt,
            justify="center",
            bg="black",
            fg="white"
        )
        decrypt_btn.pack(fill=tk.X, padx=10, pady=10, ipady=10, ipadx=10)

        # Go back to menu
        switch_window_button = tk.Button(
            self, text="Go Back", command=lambda: controller.show_frame(MainPage),
            justify="center",
            bg="black",
            fg="white"

        )
        switch_window_button.pack(padx=10, pady=10, ipady=10, ipadx=10, side="right")

    # Handle button action
    def pick_img_onclick(self):
        self.image_display_size = 300, 300
        self.path_image = filedialog.askopenfilename()
        self.load_image = Image.open(self.path_image)
        self.load_image.thumbnail(self.image_display_size, Image.ANTIALIAS)
        self.np_load_image = np.asarray(self.load_image)
        self.np_load_image = Image.fromarray(np.uint8(self.np_load_image))
        self.render = ImageTk.PhotoImage(self.np_load_image)
        self.img = tk.Label(self.image_frame, image=self.render)
        self.img.image = self.render
        self.img.pack(padx=5, pady=5, ipady=5, ipadx=5, side="left")

    # do decrypt
    def decrypt(self):
        img = cv2.imread(self.path_image)
        print(self.path_image)
        data = []
        stop = False
        for index_i, i in enumerate(img):
            i.tolist()
            for index_j, j in enumerate(i):
                if index_j % 3 == 2:
                    data.append(bin(j[0])[-1])
                    data.append(bin(j[1])[-1])
                    if bin(j[2])[-1] == '1':
                        stop = True
                        break
                else:
                    data.append(bin(j[0])[-1])
                    data.append(bin(j[1])[-1])
                    data.append(bin(j[2])[-1])
            if stop:
                break

        self.message = []
        for i in range(int((len(data) + 1) / 8)):
            self.message.append(data[i * 8:(i * 8 + 8)])

        self.message = [chr(int(''.join(i), 2)) for i in self.message]
        self.decrypted_message = ''.join(self.message)

        print(f"The cipher message is: {self.decrypted_message}")
        # Decrypt the ceaser cipher text

        plain_message = decipher(self.decrypted_message)
        print(f"The plain message is: {plain_message}")

        # Display the plain text
        self.message_box = tk.Label(self.message_frame, text=plain_message, bg="white",
                                    font=set_font(10, "normal"), height=5, wraplength=500)
        # To be packed inside frame when decrypt btn is pressed
        self.message_box.pack(fill=tk.X, padx=10, pady=10, ipady=5, ipadx=5)


# Function for basic initiations
def main():
    app = App()
    app.mainloop()


# This is where the program begins
if __name__ == '__main__':
    main()
