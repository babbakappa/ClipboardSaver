import pyperclip
import os

class Clipboard:
    def __init__(self):
        self.memory = []

    def get_data_from_clipboard(self):
        data = pyperclip.paste()
        if data != "":
            self.memory.append(data)

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
            file = open("resources/memory/" + elem, "r", newline="")
            data = file.read()
            array_content.append(data)
            file.close()
        return array_content

    def save_data_to_memory(self):
        for i in range(len(self.memory)):
            file = open(f"resources/memory/mem-{i}.txt", "w", newline="")
            file.write(self.memory[i])
            file.close()

    def delete_data_memory(self):
        self.memory.clear()
        files_list = os.listdir("resources/memory")
        for elem in files_list:
            file_path = os.path.join("resources/memory", elem)
            os.unlink(file_path)