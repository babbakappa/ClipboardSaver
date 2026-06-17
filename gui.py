from tkinter import ttk
import tkinter as tk
from tkinter import messagebox as msgbx
from tkinter import filedialog
import core
import pyperclip

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.x = 400
        self.y = 600
        self.root.geometry(f"{self.x}x{self.y}")
        self.ver = "1.2"
        self.root.title(f"ClipboardSaver {self.ver}")
        self.root.resizable(False, False)
        self.CPObject = core.Clipboard()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.DEFAULT_TXT_FONT = "Segoe UI"
        icon_image = tk.PhotoImage(file="resources/icons/icon.png")
        self.root.iconphoto(True, icon_image)

        self.top_menu = tk.Menu(self.root, tearoff=0)

        self.actions_top_menu = tk.Menu(self.top_menu, tearoff=0)
        self.top_menu.add_cascade(label="Действия", font=(self.DEFAULT_TXT_FONT, 10), menu=self.actions_top_menu)
        self.actions_top_menu.add_command(label="Сохранить список", font=(self.DEFAULT_TXT_FONT, 10),
                                       command=lambda: self.save_data_to_other_file())
        self.actions_top_menu.add_command(label="Очистить список", font=(self.DEFAULT_TXT_FONT, 10),
                                          command=lambda: self.delete_data())

        self.info_top_menu = tk.Menu(self.top_menu, tearoff=0)
        self.top_menu.add_cascade(label="Информация", font=(self.DEFAULT_TXT_FONT, 10), menu=self.info_top_menu)
        self.info_top_menu.add_cascade(label="О програме", font=(self.DEFAULT_TXT_FONT, 10),  command=lambda: self.about_program())
        self.info_top_menu.add_cascade(label="Как пользоваться", font=(self.DEFAULT_TXT_FONT, 10), command=lambda: self.how_to_use())

        self.root.config(menu=self.top_menu)

    def launch(self):
        self.root.mainloop()

    def copy_selected(self, event=None):
        selection = self.list_of_copied.curselection()
        if selection:
            index = selection[0]
            text = self.list_of_copied.get(index)
            self.CPObject.copy_to_clipboard(text)

    def add_widgets(self):
        self.top_label = ttk.Label(master=self.root, text="Список скопированного:", font=(self.DEFAULT_TXT_FONT, 20))
        self.top_label.place(x=10, y=10)

        self.list_of_copied = tk.Listbox(font=(self.DEFAULT_TXT_FONT, 16))
        self.list_of_copied.place(x=10, y=50, height=self.y - 60, width=self.x - 20)

        self.list_of_copied.bind("<Double-Button-1>", self.copy_selected)

    def update_list(self):
        text_in_clipboard = pyperclip.paste()
        if text_in_clipboard and text_in_clipboard != "":
            existing_texts = [elem for elem in self.CPObject.memory]
            if text_in_clipboard not in existing_texts:
                self.CPObject.memory.append(text_in_clipboard)
                self.list_of_copied.insert(tk.END, text_in_clipboard)

        self.root.after(500, self.update_list)

    def add_data_from_file(self):
        data = self.CPObject.load_data_from_memory()
        for elem in data:
            self.CPObject.memory.append(elem)
            self.list_of_copied.insert(tk.END, elem)
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
            if filepath == "":
                return
            file = open(filepath, "w")
            for elem in self.CPObject.memory:
                file.write(str(elem) + "\n")
            file.close()
            msgbx.showinfo("Информация", "Список сохранен")
        except Exception as error:
            msgbx.showerror("Ошибка!", f"{error}")

    def about_program(self):
        abwin = tk.Toplevel(self.root)
        abwin.geometry("400x300")
        abwin.title("О програме")

        info_txt = f"ClipboardSaver {self.ver} - это программа для сохранения истории скопированных текстов. " \
                   f"Она может быть полезна если вы работаете с текстами и вам нужно несколько раз что-то копировать," \
                   f" а постояно переключаться между вкладками лень.\n" \
                   f"Исходный код доступен всем, программу можно изменять и выкладывать модифицированные версии - я " \
                   f"не против этого."

        info_label = tk.Label(master=abwin, text=info_txt, font=(self.DEFAULT_TXT_FONT, 10), wraplength=350)
        info_label.place(relx=0.5, rely=0.4, anchor="center")

    def how_to_use(self):
        htuwin = tk.Toplevel(self.root)
        htuwin.geometry("400x300")
        htuwin.title("Как пользоваться")

        info_txt = '"Очистить список" - очищение и удаление списка. Если у вас было что-то скопировано, ' \
                   'то последний скопированный текст автоматически доабвится обратно в список' \
                   '\n"Сохранить список" - сохранение списка в файл\n' \
                   'Дважды ПКМ - копирование текста'

        info_label = tk.Label(master=htuwin, text=info_txt, font=(self.DEFAULT_TXT_FONT, 10), wraplength=350)
        info_label.place(relx=0.5, rely=0.2, anchor="center")