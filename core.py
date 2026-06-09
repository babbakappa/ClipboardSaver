import pyperclip
import savedtext
import os

class Clipboard:
    def __init__(self):
        self.memory = []

    def get_data_from_clipboard(self):
        data = pyperclip.paste()
        obj = savedtext.SavedText()
        obj.add_content(data)
        if obj.content != "":
            self.memory.append(obj)

    def check_previous(self):
        if len(self.memory) != 0:
            for elem in self.memory:
                if elem.content == pyperclip.paste():
                    return True
        return False

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)

    def load_data_from_memory(self):
        array_content = []
        files_list = [f for f in os.listdir("resources/memory")]
        for elem in files_list:
            file = open("resources/memory/" + elem, "r")
            data = savedtext.SavedText()
            data.add_content(file.read())
            array_content.append(data)
            file.close()
        return array_content

    def save_data_to_memory(self):
        for i in range(len(self.memory)):
            file = open(f"resources/memory/mem-{i}.txt", "w")
            file.write(self.memory[i].content)
            file.close()

    def delete_data_memory(self):
        self.memory.clear()
        files_list = os.listdir("resources/memory")
        for elem in files_list:
            file_path = os.path.join("resources/memory", elem)
            os.unlink(file_path)