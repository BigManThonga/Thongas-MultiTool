import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import fitz  # PyMuPDF

class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer")
        self.root.geometry("800x600")

        # Initialize variables
        self.pdf_document = None
        self.current_page = 0
        self.current_image = None

        # Create GUI components
        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.open_button = tk.Button(self.controls_frame, text="Open PDF", command=self.open_pdf)
        self.open_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.prev_button = tk.Button(self.controls_frame, text="Previous", command=self.show_prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.next_button = tk.Button(self.controls_frame, text="Next", command=self.show_next_page)
        self.next_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Bind resize event
        self.root.bind("<Configure>", self.on_resize)

    def open_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            self.load_pdf(file_path)

    def load_pdf(self, file_path):
        try:
            self.pdf_document = fitz.open(file_path)
            self.current_page = 0
            self.show_page(self.current_page)
        except Exception as e:
            self.canvas.delete("all")
            self.canvas.create_text(400, 300, text=f"Error: {e}", fill="white", font=("Arial", 16))

    def show_page(self, page_num):
        if self.pdf_document:
            page = self.pdf_document[page_num]
            pix = page.get_pixmap()

            # Convert the page to an image
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            self.current_image = image
            self.redraw_image()

    def redraw_image(self):
        if self.current_image:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Calculate the scaling factor to maintain aspect ratio
            img_width, img_height = self.current_image.size
            scale = min(canvas_width / img_width, canvas_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            # Resize the image
            resized_image = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(resized_image)

            # Clear the canvas and redraw the image
            self.canvas.delete("all")
            x_offset = (canvas_width - new_width) // 2
            y_offset = (canvas_height - new_height) // 2
            self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=self.img_tk)

    def on_resize(self, event):
        # Redraw the current image on resize
        self.redraw_image()

    def show_prev_page(self):
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def show_next_page(self):
        if self.pdf_document and self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.show_page(self.current_page)


if __name__ == "__main__":
    root = tk.Tk()
    viewer = PDFViewer(root)
    root.mainloop()
