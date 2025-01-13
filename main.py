import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class Func:
    def __init__(self, funcName = "", carNames = [], third = [], fourth = [], fifth = [], sixth = [], myBytes = []):
        self.funcName = funcName
        self.carNames = carNames
        self.third = third
        self.fourth = fourth
        self.fifth = fifth
        self.sixth = sixth
        self.myBytes = myBytes

    def getRow(self):
        return [self.funcName, " ".join(self.carNames), " ".join(self.third), " ".join(self.fourth), " ".join(self.fifth), " ".join(self.sixth),
               " ".join(self.myBytes)]
def remove_outer_parentheses(s):
    s = s.strip()
    if s.startswith('(') and s.endswith(')'):
        return s[1:-1]
    return s

#Здесь крч читаем исходный файл со всеми функциями
data = [] #сюда будем складывать все изначальные функции наши

with open('file.txt', 'r') as file:
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace(' ', '-', 1)
        params = lines[i].split('-')
        for j in range(len(params)):
            params[j] = remove_outer_parentheses(params[j])
        data.append(Func(params[0], params[1].split(','), params[2].split(','),
                         params[3].split(','), params[4].split(','), params[5].split(','),
                         params[6].split(' ')))

#for func in data:
#    print("test\n", func.funcName, func.carNames, func.third, func.fourth, func.fifth, func.sixth, func.myBytes)

def isConsists(dataArr, findArr):
    if (findArr[0] != ''):
        for i in range(len(findArr)):
            if findArr[i] in dataArr:
                return True
        return False
    return True

def isMatch(dataFunc, findFunc):
    return dataFunc.funcName == findFunc.funcName and isConsists(dataFunc.carNames, findFunc.carNames) and isConsists(dataFunc.third, findFunc.third) and isConsists(dataFunc.fourth, findFunc.fourth) and isConsists(dataFunc.fifth, findFunc.fifth) and isConsists(dataFunc.sixth, findFunc.sixth) and dataFunc.myBytes == findFunc.myBytes

def findInData(func):
    for i in range(len(data)):
        if isMatch(data[i], func):
            return i
    return -1

def replaceBytes(index, rules):
    rulesList = rules.split(',')
    for i in range(len(rulesList)):
        rule = rulesList[i].split('=')
        if '-' in rule[0]:
            a = int(rule[0].split('-')[0]) - 1
            b = int(rule[0].split('-')[1])
            for j in range(a, b):
                data[index].myBytes[j] = rule[1]
        else:
            data[index].myBytes[int(rule[0]) - 1] = rule[1]

#Дальше мы короче
#LSU (Peugeot,Citroen)-()-()-(BOSCH(ME7.9.5))-()-(01 00 00 00 00 00 00 00 00 01 01 01 01 01 01 01 00 00 00 00 01 01 01 03 00 00 01 00 00 00 01 01 00 03 00 06 00 04 AF AF 33)-(1-33=00,34=03,35=00,36=06,37=00,38=04,39=AF,40=AF,41=33)
# 1-33=00,34=03,35=00,36=06,37=00,38=04,39=AF,40=AF,41=33
def process_file(fileName):
    with open(fileName) as file:
        lines = file.readlines()
        funcToFind = Func()
        replaceRules = ""
        for i in range(len(lines)):
            if (lines[i][0].isalpha()):
                lines[i] = lines[i].replace(' ', '-', 1)
                params = lines[i].split('-', 7)
                for j in range(len(params)):
                    params[j] = remove_outer_parentheses(params[j])
                funcToFind = Func(params[0], params[1].split(','), params[2].split(','),
                                 params[3].split(','), params[4].split(','), params[5].split(','),
                                 params[6].split(' '))
                replaceRules = params[7]
            else:
                params = (lines[i].strip()).split('-', 1)
                for j in range(len(params)):
                    params[j] = remove_outer_parentheses(params[j])
                funcToFind.myBytes = params[0].split(' ')
                replaceRules = params[1]
            replaceRules = remove_outer_parentheses(replaceRules)
            ind = findInData(funcToFind)
            if ind != -1:
                replaceBytes(ind, replaceRules)
    fill_table()

def clear_table():
    for item in tree.get_children():
        tree.delete(item)
def fill_table():
    # Заполняем таблицу данными
    clear_table()
    for func in data:
        tree.insert("", tk.END, values=func.getRow())

def choose_file():
    # Открываем диалоговое окно для выбора файла
    file_path = filedialog.askopenfilename()

    # Выводим выбранный путь к файлу (или пустую строку, если ничего не выбрано)
    if file_path:
        label.config(text="Выбранный файл: " + file_path)
        process_file(file_path)
    else:
        label.config(text="Файл не выбран")

for func in data:
    print("yeah\n", func.funcName, func.carNames, func.third, func.fourth, func.fifth, func.sixth, func.myBytes)

root = tk.Tk()
root.title("Replacing")
root.geometry("800x800")

columns = ("Function name", "Car name", "3", "4", "5", "6", "bytes")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Определяем заголовки
for col in columns:
    tree.heading(col, text=col)

fill_table()

tree.column("Function name", width = 100)
tree.column("Car name", width = 100)
tree.column("3", width = 100)
tree.column("4", width = 100)
tree.column("5", width = 100)
tree.column("6", width = 100)
tree.column("bytes", width = 650)


scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

h_scrollbar = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=tree.xview)
tree.configure(xscroll=h_scrollbar.set)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Размещаем таблицу
tree.pack(expand=True, fill=tk.BOTH)

label = tk.Label(root, text="")
label.pack(pady=10)

button = tk.Button(root, text="Выбрать файл", command=choose_file)
button.pack(pady=10)

root.mainloop()