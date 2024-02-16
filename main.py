import json
import os
import re
'''
Инициализация программы

Инициализация двух важных переменных, описание класса для сериализации записий и функция для первого открытия файла с данными

'''

maxId = 0
line_count = 0
class Human():
    
    def __init__(self,*args, **kwargs ):
        '''
        При создании обьекта присваиваем ему параметры хранения
        Если параметр id не передан, то он береться из максималььного id, иначе присваиваеться тот который передали
        '''
        global maxId
        self.id = kwargs.get('id', "not set")
        if self.id == 'not set':
            self.id = maxId+1
            maxId=maxId+1
        self.name=kwargs.get('name', "not set")
        self.surname=kwargs.get('surname', "not set")
        self.father_name=kwargs.get('father_name', "not set")
        self.work=kwargs.get('work', "not set")
        self.phone_work=kwargs.get('phone_work', "not set")
        self.phone_mobile=kwargs.get('phone_mobile', "not set")
        

    def toJSON(self):
        '''
        выдаем обьект человека в формате JSON
        '''
        return json.dumps(self, default=lambda o: o.__dict__)


    def __str__(self):
        '''
        Выдает строку для вывода записи
        '''
        return f'id: {self.id}, Имя: {self.name}, фамилия:  {self.surname}, отчество: {self.father_name},\
организация: {self.work}, рабочий телефон: {self.phone_work}, мобильный телефон: {self.phone_mobile}'


def getFile():
    '''
    начальная инициализация файла

    открываем или создаем файл "file.txt"
    Если он есть, то читаем с него maxId и кол-во строк
    Если создали, то пишем туда 0 как maxID
    '''
    global maxId
    global line_count
    with open("file.txt", "r+") as f:
        line = f.readline()
        if line =="":
            f.write('0\n')
            line_count = sum(1 for line in f)
        else:
            maxId=int(line)
            line_count = sum(1 for line in f)

'''
Создание людей

Функция записи в файл нового человека и функция создания нового человека
'''

def writeFile(**kwargs):
    '''
    Запись нового человека в файл

    записываем в конец строку с данными
    Затем обновляем maxID в файле
    Затем обновляем счетчик строк в программе
    '''
    with open("file.txt", "a", encoding='utf8') as f:
        f.write(str(kwargs.get('human').toJSON())+'\n')
    with open("file.txt", "r+", encoding='utf8') as f:
        f.write(str(maxId)+'')
    with open("file.txt", "r", encoding='utf8') as f:
        global line_count
        line_count = sum(1 for line in f)   
        
def createHuman():
    '''
    основная функция создания записи
    создаем обьект записи и отдаем его в функцию записи в файл
    '''  
    print('Создание записи!')
    name=input('Введите имя: ')
    surname = input("Введите фамилию: ")
    father_name = input("Введите отчество: ")
    work = input("Введите организацию: ")
    phone_work=input("Введите рабочий телефон: ")
    phone_mobile=input("Введите мобильный телефон: ")
    h1 = Human(name=name,surname=surname,father_name=father_name,work=work,phone_work=phone_work,phone_mobile=phone_mobile)
    writeFile(human=h1)
    print("Создано!\n\n")

'''
вывод людей

функция для создания страниц по номеру и функция для вызова и вывода страниц
'''

def getPageFromFile(**kwargs):
    '''
    Функция получения страницы с записями из файла

    читаем файл построчно, если строка по номеру попадает в номер страницы добавляеться в список который возвращаеться
    '''
    with open('file.txt','r', encoding='utf8') as file:
        l = []
        count=0
        
        for line in file:
            if count==0:
                count+=1
            elif kwargs.get('page')*5+1<=count<=kwargs.get('page')*5+5:
                l.append(line)
                count+=1
            elif count<=kwargs.get('page')*5:
                count+=1
            else:
                break
        return l
    
def listHumans():
    """
    функция вывода постранично
    запускаем вывод эелемнтов, полученных с предыдущей функции
    """
    page=0
    print('Постраничный вывод\nДля выхода ввдеите q')
    print("Для следющей страницы введите n\nДля предыдущей страницы p")
    k=''
    while True:
        
        if page<1 and k=='p':
            print('Это первая страница')
        elif page>line_count//5 -1 and k=='n':
            print('Это последняя страница')
        elif k=='n':
            page+=1
        elif k=='p':
            page-=1
        elif k=='q':
            break
        print(f'Страница: {page}')
        l=getPageFromFile(page=page)
        for i in l:
            print(Human(**json.loads(i)))

        
        k=input()

'''
Изменение записи
'''
def findFromFile(**kwargs):
    """
    Поиск человка в файле

    ищем по id, возвращаем обьект записи 
    """
    id = kwargs.get('id', '*')
    with open("file.txt", "r", encoding='utf8') as f:
        flag=True       
        for i in f:
            if flag==True:
                flag=False
            else:
                h1 = Human(**json.loads(i))
                if h1.id == id:
                    return h1
                
                
def editHuman():
    '''
    Изменение записи
    Ищем человека по id, затем вводим новые данные, после этого перезаписываем файл с изменения в другой файл
    Затем удаляем старый файл и переименовываем второй файл.
    '''
    id = input('Введите id: ')
    h1=findFromFile(id=int(id))    
    if h1==None:
        print('Не найдено записи, возврат в меню')
    else:
        print(h1)
        name=input('Введите новое имя: ')
        surname = input("Введите новую фамилию: ")
        father_name = input("Введите новое отчество: ")
        work = input("Введите новую организацию: ")
        phone_work=input("Введите новый рабочий телефон: ")
        phone_mobile=input("Введите новый мобильный телефон: ")
        h2 = Human(id=h1.id,name=name,surname=surname,father_name=father_name,work=work,phone_work=phone_work,phone_mobile=phone_mobile)
        with open("file.txt", "r+", encoding='utf8') as f, open('temp.txt', 'w+', encoding='utf8') as f2:
            f2.write(f.readline())
            for i in range(line_count):
                k = f.readline()
                if Human(**json.loads(k)).id == h2.id:
                    f2.write(h2.toJSON())
                else:
                    f2.write(k)
        os.remove("file.txt")
        os.rename("temp.txt", 'file.txt')

'''
Функция поиска

'''

def findHuman():
    '''
    поиск в записях
    Принимаем от пользователя регулярное выражение
    ищем совпадение в строке до преобразования в обьект записи
    Если совпадение найдено, то выводим обьект записи 
    '''
    print('Вводите для поиска регулярное выражения, оно будет использовано в каждом параметре')
    try:
        reg=re.compile(input('выражение: '))
        with open("file.txt", "r", encoding='utf8') as f:
            flag=True       
            for i in f:
                if flag==True:
                    flag=False
                else:
                    if reg.search(i.lower()):
                        #print(f'строка в которой найдено совпадени: {i}')
                        print(f'Найдено совпадение {Human(**json.loads(i))} ')
    except Exception:
        print('ошибка в выражении')

    #reg = re.compile(r'\*')
    

'''
Функция приветствия для вывода инструкции для приветственного текста
'''
def hello():
    print('''Добро пожаловать в справочник!
          Доступные функции:
          1- Создание записи
          2- Постраничный вывод записей
          3- Редактирование записи
          4- Поиск в записях
          q- Выход
          h- Инструкция
          ''')



'''
Основная функция для вывода меню программы и управления
'''
def main():
    while True:
        print("Выберети функцию: ")
        f = input()
        if f =="1":
            createHuman()
        elif f == '2':
            listHumans()
        elif f == '3':
            editHuman()
        elif f=='4':
            findHuman()
        elif f=='q':
            break
        elif f =='h':
            hello()
        else:
            print('неизвестная команда, для вывода инструкции введите h')



'''
Стартовый код программы


выводит инструкцию, запускает инициализацию файла, затем запускает меню.
'''
if __name__:
    hello()
    getFile()
    main()