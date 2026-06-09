from tkinter import ttk
import tkinter as tk
from tkinter import messagebox as msgbx
from tkinter import filedialog
import core
import pyperclip
import savedtext

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.x = 400
        self.y = 650
        self.root.geometry(f"{self.x}x{self.y}")
        self.root.title("ClipboardSaver 1.1")
        self.root.resizable(False, False)
        self.CPObject = core.Clipboard()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.DEFAULT_TXT_FONT = "Segoe UI"
        icon_image = tk.PhotoImage(file="resources/icons/icon.png")
        self.root.iconphoto(True, icon_image)

    def launch(self):
        self.root.mainloop()

    def copy_selected(self, event=None):
        selection = self.list_of_copied.curselection()
        if selection:
            index = selection[0]
            text = self.list_of_copied.get(index)
            self.CPObject.copy_to_clipboard(text)

    def add_widgets(self):
        self.delete_button = tk.Button(master=self.root,
                                       text="Очистить список",
                                       font=(self.DEFAULT_TXT_FONT, 12),
                                       command=lambda: self.delete_data())
        self.delete_button.place(x=10, y=10)

        self.save_button = tk.Button(master=self.root,
                                       text="Сохранить список",
                                       font=(self.DEFAULT_TXT_FONT, 12),
                                       command=lambda: self.save_data_to_other_file())
        self.save_button.place(x=200, y=10)

        self.top_label = ttk.Label(master=self.root, text="Список скопированного:", font=(self.DEFAULT_TXT_FONT, 20))
        self.top_label.place(x=10, y=10+50)

        self.list_of_copied = tk.Listbox(font=(self.DEFAULT_TXT_FONT, 16))
        self.list_of_copied.place(x=10, y=50+50, height=self.y - 110, width=self.x - 20)

        self.list_of_copied.bind("<Double-Button-1>", self.copy_selected)

    def update_list(self):
        text_in_clipboard = pyperclip.paste()
        if text_in_clipboard and text_in_clipboard != "":
            existing_texts = [elem.content for elem in self.CPObject.memory]
            if text_in_clipboard not in existing_texts:
                obj = savedtext.SavedText()
                obj.add_content(text_in_clipboard)
                self.CPObject.memory.append(obj)
                self.list_of_copied.insert(tk.END, text_in_clipboard)

        self.root.after(500, self.update_list)

    def add_data_from_file(self):
        data = self.CPObject.load_data_from_memory()
        for elem in data:
            self.CPObject.memory.append(elem)
            self.list_of_copied.insert(tk.END, elem.content)
        self.update_list()

    def put_data_to_file(self):
        self.CPObject.save_data_to_memory()

    def on_closing(self):
        self.put_data_to_file()
        self.root.destroy()

    def delete_data(self):
        self.CPObject.delete_data_memory()
        self.list_of_copied.delete(0, tk.END)

    def save_data_to_other_file(self):
        try:
            filepath = filedialog.asksaveasfilename(
                title="Сохранить файл как",
                defaultextension=".txt",
                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
            )
            file = open(filepath, "w")
            for elem in self.CPObject.memory:
                file.write(str(elem.content) + "\n")
            file.close()
            msgbx.showinfo("Информация", "Список сохранен")
        except Exception as error:
            msgbx.showerror("Ошибка!", f"{error}")