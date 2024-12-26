import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas #Python library used to create PDF documents programmatically.
#canvas module in reportlab.pdfgen is used to draw and write content (like text, shapes, and images) onto a blank PDF page.
import pyttsx3
import speech_recognition as sr


root = tk.Tk()
root.title("Advanced Notepad")
root.geometry("800x600")


TextArea = tk.Text(root, undo=True, wrap="word")
TextArea.pack(fill=tk.BOTH, expand=1)
file_path = None

# File Menu
def new_file():
    global file_path
    file_path = None
    TextArea.delete(1.0, tk.END)

def open_file():
    global file_path
    #("Text Files", "*.txt"): open files with the .txt extension.
    #("All Files", "*.*"): open any file regardless of the extension.
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            # 1.0: (row 1, column 0)
            TextArea.delete(1.0, tk.END)
            TextArea.insert(1.0, file.read())

def save_file():
    global file_path
    if not file_path:
        save_as()
    else:
        with open(file_path, "w") as file:
            file.write(TextArea.get(1.0, tk.END))

def save_as():
    global file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(TextArea.get(1.0, tk.END))

# Export as PDF
def export_pdf():
    pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if pdf_path:
        try:
            c = canvas.Canvas(pdf_path) #canvas.Canvas class is the main tool for creating PDF documents.
            content = TextArea.get(1.0, tk.END).strip()
            if content:
                c.drawString(100, 750, content)
                c.save()
                messagebox.showinfo("Success", f"PDF saved at {pdf_path}")
            else:
                messagebox.showwarning("Warning", "Text area is empty. Nothing to export.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Edit Menu
def cut():
    TextArea.event_generate("<<Cut>>")

def copy():
    TextArea.event_generate("<<Copy>>")

def paste():
    TextArea.event_generate("<<Paste>>")

def undo():
    try:
        TextArea.edit_undo()
    except:
        messagebox.showerror("Undo Error", "Nothing to undo!")

def redo():
    try:
        TextArea.edit_redo()
    except:
        messagebox.showerror("Redo Error", "Nothing to redo!")

# Voice-to-Text 
def voice_to_text():
    recognizer = sr.Recognizer() #sr.Recognizer(): converting speech into text by using pre-trained speech recognition models.
    with sr.Microphone() as source: # sr.Microphone():  ensures the function uses the default microphone of the system.
        messagebox.showinfo("Voice Input", "Please speak now...")
        try:
            audio = recognizer.listen(source, timeout=10)
            recognized_text = recognizer.recognize_google(audio) #recognize_google() method is used to convert the captured audio into text using Google's speech recognition service.
            TextArea.insert(tk.END, recognized_text + " ")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand the audio")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Speech recognition service error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Text-to-Speech 
def text_to_speech():
    engine = pyttsx3.init()
    content = TextArea.get(1.0, tk.END).strip()
    if content:
        engine.say(content)
        engine.runAndWait()
    else:
        messagebox.showwarning("Warning", "Text area is empty. Please type something to read aloud.")

# Toggle Dark Mode
def dark_mode():
    bg_color = TextArea.cget("background")
    if bg_color == "white":
        TextArea.config(bg="black", fg="white", insertbackground="white")
    else:
        TextArea.config(bg="white", fg="black", insertbackground="black")

def about():
    messagebox.showinfo("About", "This is a simple notepad")

# Create the Menu
menu = tk.Menu(root)
root.config(menu=menu)

# File Menu
FileMenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=FileMenu)
FileMenu.add_command(label="New", command=new_file)
FileMenu.add_command(label="Open", command=open_file)
FileMenu.add_command(label="Save", command=save_file)
FileMenu.add_command(label="Save As", command=save_as)
FileMenu.add_command(label="Export as PDF", command=export_pdf)
FileMenu.add_separator()
FileMenu.add_command(label="Exit", command=root.quit)

# Edit Menu
EditMenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=EditMenu)
EditMenu.add_command(label="Cut", command=cut)
EditMenu.add_command(label="Copy", command=copy)
EditMenu.add_command(label="Paste", command=paste)
EditMenu.add_separator()
EditMenu.add_command(label="Undo", command=undo)
EditMenu.add_command(label="Redo", command=redo)

# Tools Menu
ToolMenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Tools", menu=ToolMenu)
ToolMenu.add_command(label="Voice-to-Text", command=voice_to_text)
ToolMenu.add_command(label="Text-to-Speech", command=text_to_speech)

# View Menu
ViewMenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=ViewMenu)
ViewMenu.add_command(label="Toggle Dark Mode", command=dark_mode)

# Help Menu
HelpMenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help" , menu=HelpMenu)
HelpMenu.add_command(label="About Notepad", command=about)


# Run the Application
root.mainloop()
