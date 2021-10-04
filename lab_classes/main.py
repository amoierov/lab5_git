import random
import os

class Files:
    """Класс подсчета файлов.
    Конструктор принимает путь до папки"""
    num_files = 0
    def __init__(self, path):  # Функция подсчёта количества файлов в папке "D://LABS//Python//lab3"
        print("Путь папки: ", path)
        for f in os.listdir(path):
                if (os.path.isfile(
                        os.path.join(path,
                                     f))):  # позволяет совместить несколько путей при помощи присвоенного разделителя
                    # Если файл является файлом, а не папкой, то увеличиваем счётчик на 1
                    self.num_files = self.num_files + 1

    def __repr__(self):
        """Метод перегружает функцию print"""
        return "Количество файлов - " + str(self.num_files)

class Read:
    """Класс чтения файла БД в словарь.
        Конструктор принимает путь до файла"""
    data = {
        '№': 0,
        'FIO': 0,
        'Email': 0,
        'Group': 0
    }
    Num = []
    FIO = []
    Email = []
    Group = []
    def __init__(self, path):  # Чтение из файла БД в словарь
        try:
            with open(path, "r") as f:
                f.readline()
                for line in f:
                    str = line.split(';')
                    self.Num.append(str[0])
                    self.FIO.append(str[1])
                    self.Email.append(str[2])
                    self.Group.append(str[3])
            self.data['№'] = self.Num
            self.data['FIO'] = self.FIO
            self.data['Email'] = self.Email
            self.data['Group'] = self.Group
        except FileNotFoundError:
            print("Невозможно открыть файл.")
    def __setattr__(self, attr, value):
        """Метод перегружает оператор присвоения.
            Не дает создавать атрибуты за пределами класса"""
        if attr == 'data[]':
            self.__dict__[attr] = value
        else:
            raise AttributeError
    def show(self,data):
        yield data

class BD:
    """Класс создает список из кортежей. Кортеж - запись в БД
    Конструктор принимает словарь"""
    sorted_bd = []
    def __init__(self, d):
        self.data = d
        self.sorted_bd = list(zip(self.data['№'], self.data['FIO'], self.data['Email'],
                        self.data['Group'])) #создает список из кортежей(кортеж - строка в БД)

    def __iter__(self):
        return DataIterator(self.sorted_bd)

    def __repr__(self):
        """Метод перегружает функцию print"""
        return str(self.sorted_bd)

    @staticmethod
    def average(data):
        o = 0
        for i in data['№']:
            o += int(i)
        return o / len(data['№'])
class DataIterator:
    def __init__(self, sorted_bd):
        self.sorted_bd = sorted_bd
    def __iter__(self):
        return self
    def __next__(self):
        if self.sorted_bd == []:
            raise StopIteration
        item = self.sorted_bd[0]
        del self.sorted_bd[0]
        return item

class Sort_Num(BD):
    """Класс сортирует список по номеру"""
    def __init__(self, d):
        BD.__init__(self, d)
        self.sorted_bd.sort(key=lambda x: x[0])
class Sort_FIO(BD):
    """Класс сортирует список по Фамилии"""
    def __init__(self, d):
        BD.__init__(self, d)
        self.sorted_bd.sort(key=lambda x: x[1])
class Sort_Email(BD):
    """Класс отбирает студентов с почтой gmail"""
    str = "gmail"
    def __init__(self, d):
        BD.__init__(self, d)
        for i, field in enumerate(self.sorted_bd, start=0):
            if (self.str in field[2]):
                continue
            else:
                self.sorted_bd.pop(i)


class Output:
    """Класс записывает список в файл.
    Конструктор принимает путь до файла и сам список"""
    def __init__(self, path, bd):
        self.path = path
        with open(path, "w") as f:
            f.write("№;FIO;Email;Group\n")
            for el in bd:
                f.write(str(el[0]) + ";" + str(el[1]) + ";" + str(el[2]) + ";" + str(el[3]))
    def __repr__(self):
        """Метод перегружает функцию print"""
        return "Отсортированный список записан по пути - " + self.path


data_base = Read("D://LABS//Python//lab3//data.csv")

print("Сортировка студентов по FIO - 1")
print("Сортировка студентов по номеру - 2")
print("Выборока студентов, которые пользуются почтой gmail - 3")
print("Посчитать количество папок в директории - 4")
action = input()
if action == "1":
    a = Sort_FIO(data_base.data)
elif action == "2":
    a = Sort_Num(data_base.data)
elif action == "3":
    a = Sort_Email(data_base.data)
elif action == "4":
    print(Files("D://LABS//Python//lab3"))
else:
    print("Ошибка!Введите 1-4.")


data_base.data['№'] = ['1', '2', '7', '4', '6']
if action == "1" or action == "2" or action == "3":
    print(Output("D://LABS//Python//lab4//output.txt", a.sorted_bd))
    print("Среднее арифметическое номеров студентов - " + str(BD.average(data_base.data)))
    for i in a:
        print(i)




