from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from backend import load_image, backend_func
import numpy as np


def loadImage(root, img_label):
    file_path = filedialog.askopenfilename(
        title="Seleziona immagine", 
        filetypes=[("Immagini", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")], 
        initialdir="./images"
    )
    
    if file_path:
        root.selected_file = file_path
        img = Image.open(file_path)
        
        img = img.resize((600, 600))
        img_tk = ImageTk.PhotoImage(img)
        
        img_label.config(image=img_tk)
        img_label.image = img_tk  


def loadImage_result(img_label_result):
    file_path = "./images/result.bmp"
    
    if file_path:
        img = Image.open(file_path)
        
        img = img.resize((600, 600))  
        img_tk = ImageTk.PhotoImage(img)
        
        img_label_result.config(image=img_tk)
        img_label_result.image = img_tk  


def startConversion(fBox, dBox, root, img_label_result):
    # Prendi i valori dai campi di testo
    f_value = int(fBox.get())
    d_value = int(dBox.get())

    print(f"Valori inseriti: {f_value}, {d_value}")

    # Verifica che i valori siano nel range corretto
    if f_value <= 0 or d_value <= 0 or d_value > 2 * f_value - 2:
        messagebox.showerror(
            "Valori non validi",
            f"Errore: f e d devono essere positivi, d deve essere minore di {2 * f_value - 2}"
        )
        return

    try:
        backend_func(root.selected_file, f_value, d_value)  # Chiama la funzione di conversione
        loadImage_result(img_label_result)  # <-- carica l'immagine generata dopo la conversione
    except Exception as e:
        print(f"Errore durante la conversione: {e}")


def main():
    root = Tk()
    root.state('zoomed')
    
    # Imposta il background nero
    #root.config(bg="grey")
    
    # Permetti il ridimensionamento della finestra
    root.resizable(True, True)

    root.grid_rowconfigure(0, weight=1)  # Permette alla riga 0 di espandersi
    root.grid_rowconfigure(1, weight=1)  # Permette alla riga 1 di espandersi
    root.grid_rowconfigure(2, weight=1)  # Permette alla riga 2 di espandersi
    root.grid_rowconfigure(3, weight=1)  # Permette alla riga 3 di espandersi
    root.grid_columnconfigure(0, weight=1)  # Permette alla colonna 0 di espandersi
    root.grid_columnconfigure(1, weight=1)  # Permette alla colonna 1 di espandersi
    root.grid_columnconfigure(2, weight=1)

    img_label = Label(root)
    img_label.grid(row=1, column=1, padx=5, pady=5)

    img_label_result = Label(root)
    img_label_result.grid(row=1, column=2, padx=5, pady=5)

    f_label = Label(root, text="Valore di f:")
    f_label.grid(row=2, column=2, padx=5, pady=5, sticky="e")

    fBox = Entry(root, width=20)
    fBox.grid(row=2, column=3, padx=5, pady=5)

    d_label = Label(root, text="Valore di d:")
    d_label.grid(row=2, column=4, padx=5, pady=5, sticky="e")

    dBox = Entry(root, width=20)
    dBox.grid(row=2, column=5, padx=5, pady=5)

    caricaImmagine = Button(root, text="Seleziona immagine", padx=50, command=lambda: loadImage(root, img_label))
    caricaImmagine.grid(row=2, column=0)

    conversionButton = Button(root, text="Converti",  padx=50, command=lambda: startConversion(fBox, dBox, root, img_label_result))
    conversionButton.grid(row=2, column=1)

    root.mainloop()


if __name__ == "__main__":
    main()
