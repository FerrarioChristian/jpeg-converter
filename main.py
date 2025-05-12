from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageTk
from backend import load_image
from backend import backend_func
import numpy as np


root = Tk()



def main():
    img_label = Label(root)
    img_label.grid(row=1, column=1, padx=5, pady=5)

    img_label_result = Label(root)
    img_label_result.grid(row=1, column=1, padx=5, pady=5)

    
    f_label = Label(root, text="Valore di f:")
    f_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    fBox = Entry(root, width=20)
    fBox.grid(row=3, column=1, padx=5, pady=5)

    d_label = Label(root, text="Valore di d:")
    d_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")

    dBox = Entry(root, width=20)
    dBox.grid(row=2, column=1, padx=5, pady=5)



    def loadImage():
        file_path = filedialog.askopenfilename(title="Seleziona immagine", filetypes=[("Immagini", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")], initialdir="./images")
        
        if file_path:
            root.selected_file = file_path
            img = Image.open(file_path)
            
            img = img.resize((600, 600))
            img_tk = ImageTk.PhotoImage(img)
            
            
            img_label.config(image=img_tk)
            img_label.image = img_tk  

    def loadImage_result():
        file_path = "./images/result.bmp"
        
        if file_path:
            img = Image.open(file_path)
            
            img = img.resize((600, 600))  
            img_tk = ImageTk.PhotoImage(img)
            
            img_label_result.config(image=img_tk)
            img_label_result.image = img_tk  

    def startConversion():
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
            # Carica l'immagine e chiama la funzione backend
            image = load_image(root.selected_file).astype(np.float32)
            backend_func(root.selected_file, f_value, d_value)  # Chiama la funzione di conversione
            loadImage_result()  # <-- carica l'immagine generata dopo la conversione
        except Exception as e:
            print(f"Errore durante la conversione: {e}")



            
    caricaImmagine = Button(root, text="Seleziona immagine", padx=50, command=loadImage)
    caricaImmagine.grid()

    conversionButton = Button(root, text="Converti", padx=50, command = startConversion)
    conversionButton.grid()

    root.mainloop()

if __name__ == "__main__":
    main()