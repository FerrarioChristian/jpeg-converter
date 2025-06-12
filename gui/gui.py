import os
import threading
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox
import gc

from converter import compress

# Set shadcn-like dark mode appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def calc_retained_ratio(f, d):
    """Calculates the percentage of frequencies kept based on F and D."""
    kept = 0
    for i in range(f):
        for j in range(f):
            if i + j < d:
                kept += 1
    return (kept / (f * f)) * 100

def create_scaled_ctk_image(img_path, max_size=(450, 450)):
    """Loads an image and scales it to fit within max_size preserving aspect ratio."""
    img = Image.open(img_path)
    w, h = img.size
    ratio = min(max_size[0] / w, max_size[1] / h)
    new_w, new_h = int(w * ratio), int(h * ratio)
    return ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h)), (w, h)

class JpegConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("DCT Image Compressor - Case Study")
        self.geometry("1100x800")
        self.minsize(900, 700)
        
        self.selected_file = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.setup_ui()
        
    def setup_ui(self):
        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 5))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, text="DCT Compressor", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left")
        
        self.desc_label = ctk.CTkLabel(
            self.header_frame, text="A visual case study on the Discrete Cosine Transform", 
            font=ctk.CTkFont(size=14), text_color="#a0a0a0"
        )
        self.desc_label.pack(side="left", padx=15, pady=(5,0))
        
        # --- Main Image Area ---
        self.images_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.images_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
        
        self.images_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self.images_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        self.images_frame.grid_rowconfigure(0, weight=1)
        
        # Original Image Panel
        self.original_frame = ctk.CTkFrame(self.images_frame, fg_color="#121212", corner_radius=12)
        self.original_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.original_frame.grid_rowconfigure(1, weight=1)
        self.original_frame.grid_columnconfigure(0, weight=1)
        
        self.orig_header = ctk.CTkFrame(self.original_frame, fg_color="transparent")
        self.orig_header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.orig_label = ctk.CTkLabel(self.orig_header, text="Original Image", font=ctk.CTkFont(weight="bold", size=16))
        self.orig_label.pack(side="left")
        
        self.orig_info = ctk.CTkLabel(self.orig_header, text="", text_color="#888888")
        self.orig_info.pack(side="right")
        
        self.orig_img_display = ctk.CTkLabel(self.original_frame, text="No Image Selected\n\nClick 'Load Image' below", text_color="#555555")
        self.orig_img_display.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Compressed Image Panel
        self.result_frame = ctk.CTkFrame(self.images_frame, fg_color="#121212", corner_radius=12)
        self.result_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.result_frame.grid_rowconfigure(1, weight=1)
        self.result_frame.grid_columnconfigure(0, weight=1)
        
        self.res_header = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        self.res_header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.res_label = ctk.CTkLabel(self.res_header, text="Compressed Result", font=ctk.CTkFont(weight="bold", size=16))
        self.res_label.pack(side="left")
        
        self.res_info = ctk.CTkLabel(self.res_header, text="", text_color="#888888")
        self.res_info.pack(side="right")
        
        self.res_img_display = ctk.CTkLabel(self.result_frame, text="No Result Yet", text_color="#555555")
        self.res_img_display.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # --- Controls Area ---
        self.controls_frame = ctk.CTkFrame(self, fg_color="#18181b", corner_radius=12, border_width=1, border_color="#27272a")
        self.controls_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 15))
        
        self.controls_frame.grid_columnconfigure(0, weight=0)
        self.controls_frame.grid_columnconfigure(1, weight=1)
        self.controls_frame.grid_columnconfigure(2, weight=0)
        
        # Action Buttons
        self.btn_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.btn_frame.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        self.load_btn = ctk.CTkButton(
            self.btn_frame, text="Load Image", 
            fg_color="#27272a", hover_color="#3f3f46", text_color="white",
            border_width=1, border_color="#3f3f46",
            command=self.load_image
        )
        self.load_btn.pack(side="left", padx=(0, 15))
        
        self.compress_btn = ctk.CTkButton(
            self.btn_frame, text="Compress Image", 
            fg_color="#fafafa", hover_color="#e4e4e7", text_color="#09090b",
            font=ctk.CTkFont(weight="bold"),
            command=self.start_compression
        )
        self.compress_btn.pack(side="left")
        
        # Parameters
        self.params_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.params_frame.grid(row=0, column=1, padx=20, pady=15, sticky="ew")
        self.params_frame.grid_columnconfigure(4, weight=1)
        
        # Row 0: Params
        self.f_label = ctk.CTkLabel(self.params_frame, text="Block Size (F):", font=ctk.CTkFont(weight="bold"))
        self.f_label.grid(row=0, column=0, padx=(0, 10), sticky="e")
        
        self.f_var = ctk.StringVar(value="8")
        self.f_entry = ctk.CTkEntry(
            self.params_frame, textvariable=self.f_var, width=50,
            fg_color="#09090b", border_color="#27272a"
        )
        self.f_entry.grid(row=0, column=1, sticky="w")
        self.f_var.trace_add("write", self.update_d_slider_range)
        
        self.d_label = ctk.CTkLabel(self.params_frame, text="Frequencies (D):", font=ctk.CTkFont(weight="bold"))
        self.d_label.grid(row=0, column=2, padx=(15, 10), sticky="e")
        
        self.d_var = ctk.StringVar(value="14")
        self.d_entry = ctk.CTkEntry(
            self.params_frame, textvariable=self.d_var, width=40,
            fg_color="#09090b", border_color="#27272a"
        )
        self.d_entry.grid(row=0, column=4, padx=(10, 0), sticky="w")
        self.d_var.trace_add("write", self.update_d_from_entry)
        
        self.d_slider = ctk.CTkSlider(
            self.params_frame, from_=0, to=14, number_of_steps=14, width=120,
            button_color="#fafafa", button_hover_color="#e4e4e7", progress_color="#fafafa",
            command=self.d_slider_event
        )
        self.d_slider.set(14)
        self.d_slider.grid(row=0, column=3, sticky="ew")
        
        # Row 1: Stats
        self.stats_label = ctk.CTkLabel(self.params_frame, text="Retained Frequencies: 100.0%", text_color="#a0a0a0", font=ctk.CTkFont(size=12))
        self.stats_label.grid(row=1, column=0, columnspan=5, sticky="w", pady=(2, 0))
        
        # Row 2: Huffman Toggle
        self.use_huffman_var = ctk.BooleanVar(value=True)
        self.huffman_switch = ctk.CTkSwitch(
            self.params_frame, text="Huffman Size Estimation", variable=self.use_huffman_var,
            progress_color="#fafafa", button_color="#09090b", button_hover_color="#3f3f46"
        )
        self.huffman_switch.grid(row=2, column=0, columnspan=5, sticky="w", pady=(10, 0))
        
        # Row 3: Huffman Desc
        self.huffman_desc = ctk.CTkLabel(self.params_frame, text="(Simulates accurate compression entropy instead of reading raw .bmp size)", text_color="#71717a", font=ctk.CTkFont(size=11))
        self.huffman_desc.grid(row=3, column=0, columnspan=5, sticky="w", padx=(5, 0), pady=(2, 0))
        
        # Extra Features Frame
        self.extras_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.extras_frame.grid(row=0, column=2, padx=20, pady=15, sticky="e")
        
        self.error_map_btn = ctk.CTkButton(
            self.extras_frame, text="Show Error Map", 
            fg_color="#3b82f6", hover_color="#2563eb", text_color="white",
            state="disabled", command=self.show_error_map
        )
        self.error_map_btn.pack(side="top", pady=(0, 5))
        
        self.zoom_btn = ctk.CTkButton(
            self.extras_frame, text="Zoom", 
            fg_color="#6366f1", hover_color="#4f46e5", text_color="white",
            state="disabled", command=self.open_zoom
        )
        self.zoom_btn.pack(side="top", pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(self.extras_frame, text="Ready", text_color="#71717a")
        self.status_label.pack(side="bottom")

    def open_zoom(self):
        if hasattr(self, 'selected_file') and os.path.exists("./results/result.bmp"):
            try:
                top = ctk.CTkToplevel(self)
                top.title("Zoom Inspector (Nearest Neighbor)")
                top.geometry("900x950")
                
                img = Image.open("./results/result.bmp")
                w, h = img.size
                self.insp_zoomed = img.resize((w * 4, h * 4), Image.Resampling.NEAREST)
                
                self.insp_x = max(0, (self.insp_zoomed.width - 800) // 2)
                self.insp_y = max(0, (self.insp_zoomed.height - 800) // 2)
                
                self.insp_lbl = ctk.CTkLabel(top, text="", cursor="fleur")
                self.insp_lbl.pack(expand=True, fill="both", padx=20, pady=(20, 10))
                
                self.update_insp_crop()
                
                self.insp_lbl.bind("<ButtonPress-1>", self.insp_press)
                self.insp_lbl.bind("<B1-Motion>", self.insp_drag)
                
                info = ctk.CTkLabel(top, text="Zoomed 400%. Drag with mouse to pan.", text_color="#a0a0a0")
                info.pack(side="bottom", pady=5)
                
                close_btn = ctk.CTkButton(top, text="Close Window", command=top.destroy, fg_color="#ef4444", hover_color="#dc2626")
                close_btn.pack(side="bottom", pady=10)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {e}")

    def insp_press(self, event):
        self.insp_start_x = event.x
        self.insp_start_y = event.y

    def insp_drag(self, event):
        dx = self.insp_start_x - event.x
        dy = self.insp_start_y - event.y
        self.insp_x += dx
        self.insp_y += dy
        self.insp_start_x = event.x
        self.insp_start_y = event.y
        self.update_insp_crop()

    def update_insp_crop(self):
        if self.insp_x < 0: self.insp_x = 0
        if self.insp_y < 0: self.insp_y = 0
        max_x = max(0, self.insp_zoomed.width - 800)
        max_y = max(0, self.insp_zoomed.height - 800)
        if self.insp_x > max_x: self.insp_x = max_x
        if self.insp_y > max_y: self.insp_y = max_y
        
        cropped = self.insp_zoomed.crop((self.insp_x, self.insp_y, self.insp_x + 800, self.insp_y + 800))
        ctk_img = ctk.CTkImage(light_image=cropped, dark_image=cropped, size=(800, 800))
        self.insp_lbl.configure(image=ctk_img)
        self.insp_lbl.image = ctk_img

    def show_error_map(self):
        if hasattr(self, 'error_map_path') and os.path.exists(self.error_map_path):
            try:
                top = ctk.CTkToplevel(self)
                top.title("Error Map (Difference Heatmap)")
                top.geometry("650x700")
                
                img = Image.open(self.error_map_path)
                w, h = img.size
                ratio = min(600 / w, 500 / h)
                new_w, new_h = int(w * ratio), int(h * ratio)
                
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h))
                lbl = ctk.CTkLabel(top, image=ctk_img, text="")
                lbl.pack(expand=True, fill="both", padx=20, pady=(20, 5))
                
                # Dynamic Legend UI
                legend_frame = ctk.CTkFrame(top, fg_color="transparent")
                legend_frame.pack(fill="x", padx=40, pady=5)
                
                legend_frame.grid_columnconfigure((0, 2), weight=0)
                legend_frame.grid_columnconfigure(1, weight=1)
                
                min_lbl = ctk.CTkLabel(legend_frame, text="0\nNo Error", text_color="#3b82f6", font=ctk.CTkFont(weight="bold"))
                min_lbl.grid(row=0, column=0, sticky="w")
                
                import cv2, numpy as np
                arr = np.linspace(0, 255, 400).astype(np.uint8)
                arr = np.tile(arr, (20, 1))
                arr_color = cv2.applyColorMap(arr, cv2.COLORMAP_JET)
                arr_color = cv2.cvtColor(arr_color, cv2.COLOR_BGR2RGB)
                grad_img = Image.fromarray(arr_color)
                
                grad_ctk = ctk.CTkImage(light_image=grad_img, dark_image=grad_img, size=(300, 20))
                grad_lbl = ctk.CTkLabel(legend_frame, image=grad_ctk, text="")
                grad_lbl.grid(row=0, column=1, sticky="ew", padx=15)
                
                max_lbl = ctk.CTkLabel(legend_frame, text="255\nMax Error", text_color="#ef4444", font=ctk.CTkFont(weight="bold"))
                max_lbl.grid(row=0, column=2, sticky="e")
                
                close_btn = ctk.CTkButton(top, text="Close Window", command=top.destroy, fg_color="#ef4444", hover_color="#dc2626")
                close_btn.pack(pady=10)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load error map: {e}")

    def d_slider_event(self, value):
        self.d_var.set(str(int(value)))
        self.update_stats()

    def update_d_from_entry(self, *args):
        try:
            val = int(self.d_var.get())
            f_val = int(self.f_var.get())
            max_d = max(0, 2 * f_val - 2)
            if 0 <= val <= max_d:
                self.d_slider.set(val)
                self.update_stats()
        except ValueError:
            pass

    def update_d_slider_range(self, *args):
        try:
            f_val = int(self.f_var.get())
            if f_val > 0:
                max_d = max(0, 2 * f_val - 2)
                self.d_slider.configure(to=max_d, number_of_steps=max_d if max_d > 0 else 1)
                
                current_d = self.d_slider.get()
                if current_d > max_d:
                    self.d_slider.set(max_d)
                    self.d_var.set(str(max_d))
                self.update_stats()
        except ValueError:
            self.stats_label.configure(text="Invalid Block Size")
            
    def update_stats(self):
        try:
            f_val = int(self.f_var.get())
            d_val = int(self.d_var.get())
            if f_val > 0:
                ratio = calc_retained_ratio(f_val, d_val)
                self.stats_label.configure(text=f"Retained Frequencies: {ratio:.1f}%")
        except ValueError:
            pass

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Images", ("*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp"))],
            initialdir="./images",
        )
        if file_path:
            self.selected_file = file_path
            try:
                self.res_img_display.configure(image=None, text="No Result Yet")
                self.res_info.configure(text="")
                self.error_map_btn.configure(state="disabled")
                self.zoom_btn.configure(state="disabled")
                
                ctk_img, size = create_scaled_ctk_image(file_path, max_size=(450, 450))
                self.orig_img_display.configure(image=ctk_img, text="")
                self.orig_img_display.image = ctk_img
                
                file_size_kb = os.path.getsize(file_path) / 1024
                self.orig_info.configure(text=f"{size[0]}x{size[1]} • {file_size_kb:.1f} KB")
                
                self.status_label.configure(text="Image loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{e}")
                
    def load_result_image(self):
        file_path = "./results/result.bmp"
        if os.path.exists(file_path):
            try:
                ctk_img, size = create_scaled_ctk_image(file_path, max_size=(450, 450))
                self.res_img_display.configure(image=ctk_img, text="")
                self.res_img_display.image = ctk_img
            except Exception as e:
                print(f"Error loading result: {e}")

    def start_compression(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select an image first.")
            return

        try:
            f_value = int(self.f_var.get())
        except ValueError:
            messagebox.showerror("Error", "F must be an integer greater than 0.")
            return
            
        try:
            d_value = int(self.d_var.get())
        except ValueError:
            messagebox.showerror("Error", "D must be a valid integer.")
            return
        
        if f_value < 1:
            messagebox.showerror("Error", "The value of F must be greater than 0")
            return
            
        if d_value < 0 or d_value > 2 * f_value - 2:
            messagebox.showerror("Error", f"The value of D must be between 0 and {2 * f_value - 2}")
            return
            
        self.status_label.configure(text="Compressing...")
        self.compress_btn.configure(state="disabled")
        self.error_map_btn.configure(state="disabled")
        self.zoom_btn.configure(state="disabled")
        
        self.update_idletasks()
        
        threading.Thread(target=self._run_compression, args=(f_value, d_value), daemon=True).start()
        
    def _run_compression(self, f_value, d_value):
        try:
            gc.collect()
            use_huff = self.use_huffman_var.get()
            result_data = compress(self.selected_file, f_value, d_value, use_huffman=use_huff)
            self.after(0, self._compression_done, True, result_data)
        except Exception as e:
            self.after(0, self._compression_done, False, str(e))
            
    def _compression_done(self, success, result_data):
        self.compress_btn.configure(state="normal")
        if success:
            self.status_label.configure(text="Compression complete")
            self.error_map_path = result_data["error_map_path"]
            self.error_map_btn.configure(state="normal")
            self.zoom_btn.configure(state="normal")
            
            if result_data["huffman_bytes"] is not None:
                huffman_kb = result_data["huffman_bytes"] / 1024
                size_str = f"Est. Size: {huffman_kb:.1f} KB"
            else:
                bmp_kb = os.path.getsize(result_data["output_path"]) / 1024
                size_str = f"BMP Size: {bmp_kb:.1f} KB"
                
            psnr = result_data["psnr"]
            mse = result_data["mse"]
            
            self.res_info.configure(text=f"{size_str} | PSNR: {psnr:.2f}dB | MSE: {mse:.1f}")
            self.load_result_image()
        else:
            self.status_label.configure(text="Error")
            messagebox.showerror("Error", f"An error occurred during conversion:\n{result_data}")

def launch_gui():
    app = JpegConverterApp()
    app.mainloop()

if __name__ == "__main__":
    launch_gui()
