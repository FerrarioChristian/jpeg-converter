from tkinter import Button, Entry, Frame, Label, Tk, filedialog, messagebox

from PIL import Image, ImageTk

from converter import compress


def loadImage(root, img_label):
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Images", ("*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp"))],
        initialdir="./images",
    )

    if file_path:
        root.selected_file = file_path
        img = Image.open(file_path)

        img = img.resize((600, 600))
        img_tk = ImageTk.PhotoImage(img)

        img_label.config(image=img_tk)
        img_label.image = img_tk


def loadImage_result(img_label_result):
    file_path = "./results/result.bmp"

    if file_path:
        img = Image.open(file_path)

        img = img.resize((600, 600))
        img_tk = ImageTk.PhotoImage(img)

        img_label_result.config(image=img_tk)
        img_label_result.image = img_tk


def startConversion(fBox, dBox, root, img_label_result):
    if not hasattr(root, "selected_file") or root.selected_file is None:
        messagebox.showerror("Error", "Please select an image first.")
        return

    if not fBox.get().strip():
        messagebox.showerror(
            "Error", "Please enter a valid value for F (greater than 0)"
        )
        return

    f_value = int(fBox.get())

    if not dBox.get().strip():
        messagebox.showerror(
            "Error",
            f"Please enter a valid value for D (between 0 and {2 * f_value - 2})",
        )
        return

    d_value = int(dBox.get())

    print(f"Selected values: f:{f_value}, d:{d_value}")

    if f_value < 1:
        messagebox.showerror("Error", "The value of F must be greater than 0")
        return

    if d_value < 0 or d_value > 2 * f_value - 2:
        messagebox.showerror(
            "Invalid values",
            f"Error: The value of D must be between 0 and {2 * f_value - 2}",
        )
        return

    try:
        compress(
            root.selected_file, f_value, d_value
        )  # Chiama la funzione di conversione
        loadImage_result(
            img_label_result
        )  # <-- carica l'immagine generata dopo la conversione
    except Exception as e:
        print(f"An error occurred during conversion: {e}")


def launch_gui():
    root = Tk()

    root.title("Caravaggio-converter")
    root.state("zoomed")

    # Imposta il background nero
    # root.config(bg="grey")

    # Permetti il ridimensionamento della finestra
    root.resizable(True, True)

    bg_img = Image.open("./gui/resources/caravaggio.jpg")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    bg_img = bg_img.resize((screen_width, screen_height))
    bg_img_tk = ImageTk.PhotoImage(bg_img)

    # Label per lo sfondo
    bg_label = Label(root, image=bg_img_tk)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    for i in range(3):
        root.grid_columnconfigure(i, weight=1)
    for i in range(2):
        root.grid_rowconfigure(i, weight=10)
    root.grid_rowconfigure(2, weight=1)

    control_frame = Frame(root)
    control_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=10)

    for i in range(6):
        control_frame.grid_columnconfigure(i, weight=1)

    img_label = Label(root)
    img_label.grid(row=1, column=0)

    img_label_result = Label(root)
    img_label_result.grid(row=1, column=2)

    f_label = Label(control_frame, text="F value:")
    f_label.grid(row=2, column=2, sticky="e")

    fBox = Entry(control_frame, width=20)
    fBox.grid(row=2, column=3)

    d_label = Label(control_frame, text="D value:")
    d_label.grid(row=2, column=4, sticky="e")

    dBox = Entry(control_frame, width=20)
    dBox.grid(row=2, column=5)

    caricaImmagine = Button(
        control_frame,
        text="Load Image",
        padx=25,
        command=lambda: loadImage(root, img_label),
    )
    caricaImmagine.grid(row=2, column=0, padx=15)

    conversionButton = Button(
        control_frame,
        text="Compress",
        command=lambda: startConversion(fBox, dBox, root, img_label_result),
    )
    conversionButton.grid(row=2, column=1, padx=15)

    root.mainloop()


if __name__ == "__main__":
    launch_gui()
