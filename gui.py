import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os

# Change this URL to your API endpoint. If running locally, for example, use "http://127.0.0.1:8000/split"
API_URL = "https://pdf-split-api.render.com/split"

def select_file():
    # Open a file dialog to select a PDF file.
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def upload_file():
    file_path = file_entry.get()
    if not file_path:
        messagebox.showerror("Error", "Please select a PDF file first.")
        return
    try:
        with open(file_path, "rb") as f:
            # Prepare the file payload for the API
            files = {"file": (os.path.basename(file_path), f, "application/pdf")}
            response = requests.post(API_URL, files=files)
            if response.status_code == 200:
                # Ask where to save the ZIP file
                save_path = filedialog.asksaveasfilename(defaultextension=".zip",
                                                         filetypes=[("ZIP files", "*.zip")],
                                                         title="Save split PDF as")
                if save_path:
                    with open(save_path, "wb") as zip_file:
                        zip_file.write(response.content)
                    messagebox.showinfo("Success", "PDF has been split successfully and saved!")
            else:
                messagebox.showerror("API Error", f"Failed to split PDF: {response.text}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Set up the main window
root = tk.Tk()
root.title("PDF Splitter GUI")

# Create and place widgets
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

file_label = tk.Label(frame, text="Select PDF file:")
file_label.grid(row=0, column=0, sticky="w")

file_entry = tk.Entry(frame, width=50)
file_entry.grid(row=1, column=0, padx=(0, 5))

browse_button = tk.Button(frame, text="Browse", command=select_file)
browse_button.grid(row=1, column=1)

upload_button = tk.Button(frame, text="Split PDF", command=upload_file)
upload_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()