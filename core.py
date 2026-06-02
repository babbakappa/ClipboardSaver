import pyperclip

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
                if elem == pyperclip.paste():
                    return True
        return False

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)

    def load_data_from_memory(self):
        try:
            file = open("filememory.txt", "r")
            data = file.readlines()
            file.close()
            data = [x.strip() for x in data]
            return data
        except FileNotFoundError:
            return []

    def save_data_to_memory(self):
        file = open("filememory.txt", "w")
        for elem in self.memory:
            file.write(str(elem) + "\n")
        file.close()

    def delete_data_memory(self):
        self.memory.clear()
        file = open("filememory.txt", "w")
        file.close()