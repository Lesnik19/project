# импоритрование библиотек
from tkinter import *
from tkinter.ttk import Combobox
import sqlite3
from tkinter.messagebox import *


class My_combobox:
    # создание выпадающего списка
    def __init__(self, list, font, x, y, width, command):
        self.list = list
        self.font = font
        self.x = x
        self.y = y
        self.width = width

        self.combobox = Combobox(values=self.list, font=self.font, state='readonly')
        self.combobox.place(x=self.x, y=self.y, width=self.width)
        self.combobox.bind('<<ComboboxSelected>>', command)


class My_button:
    # создание кнопки
    def __init__(self, text, font, x, y, width, command):
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.width = width
        self.command = command

        self.button = Button(text=self.text, font=self.font, command=self.command)
        self.button.place(x=self.x, y=self.y, width=self.width)


class My_label:
    # создание текста
    def __init__(self, text, font, x, y, color):
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.color = color

        self.label = Label(text=self.text, font=self.font, background=self.color)
        self.label.place(x=self.x, y=self.y)


class My_entry:
    # создание окошка для ввода данных
    def __init__(self, font, x, y, width):
        self.font = font
        self.x = x
        self.y = y
        self.width = width

        self.entry = Entry(font=self.font)
        self.entry.place(x=self.x, y=self.y, width=self.width)


class Window:
    # создание окна
    def __init__(self):
        self.canvas = None
        # создание окна
        self.window = Tk()
        # размеры окна
        self.width = 700
        self.height = 700
        # цвет окна
        self.color = '#0066CC'  # 0520CC 007dd1 0066CC

        # задача размера окна
        self.window.geometry(f'{self.width}x{self.height}')
        # название окна
        self.window.title('Автосервис CAR-CARICH')
        # запрет на расширение размеров окна
        self.window.resizable(height=False, width=False)

        # вызов функций
        self.create_canvas()
        self.create_labels()
        self.create_entries()
        self.create_buttons()
        self.create_comboboxes()
        self.window.mainloop()

    def create_canvas(self):
        # создание холста
        self.canvas = Canvas(
            self.window,
            # размеры холста
            width=self.width,
            height=self.height,
            # цвет холста
            background=self.color)

        # формирование холста
        self.canvas.pack()

    def create_labels(self):
        # создание текста
        My_label('Автосервис CAR-CARICH', 'Arial20', 250, 50, color=self.color)

        My_label('Марка автомобиля: ', 'Arial16', 40, 150, color=self.color)
        My_label('Модель автомобиля: ', 'Arial16', 40, 200, color=self.color)
        My_label('Цвет: ', 'Arial16', 40, 250, color=self.color)
        My_label('Год производства: ', 'Arial16', 40, 300, color=self.color)
        My_label('Номер автомобиля: ', 'Arial16', 40, 350, color=self.color)
        My_label('Выберите услугу', 'Arial16', 500, 150, color=self.color)
        # создание изменяющегося текста
        self.prise_lable = My_label('Цена: ', 'Arial16', 500, 250, color=self.color)

        My_label('Имя: ', 'Arial16', 40, 500, color=self.color)
        My_label('Фамилия: ', 'Arial16', 40, 550, color=self.color)
        My_label('Телефон: ', 'Arial16', 40, 600, color=self.color)

    def create_entries(self):
        # создание окошек для ввода данных
        self.brand = My_entry(font='Arial 16', x=250, y=150, width=200)
        self.model = My_entry(font='Arial 16', x=250, y=200, width=200)
        self.car_color = My_entry(font='Arial 16', x=250, y=250, width=200)
        self.year = My_entry(font='Arial 16', x=250, y=300, width=200)
        self.number = My_entry(font='Arial 16', x=250, y=350, width=200)

        self.name = My_entry(font='Arial 16', x=150, y=500, width=200)
        self.surname = My_entry(font='Arial 16', x=150, y=550, width=200)
        self.phone_number = My_entry(font='Arial 16', x=150, y=600, width=200)

    def create_buttons(self):
        # создание кнопки
        My_button('Записать', font='Arial 16', x=500, y=500, width=100, command=self.record_information)

    def create_comboboxes(self):
        # создание выпадающего списка
        list = self.get_list_of_services()
        self.service = My_combobox(list=list, font='Arial 14', x=460, y=200, width=230, command=self.get_services_price)

    def get_services_price(self, event):
        # получение цены услуги и предъявление её пользователю
        service = self.service.combobox.get()
        connection = sqlite3.connect('carservice.db')
        cursor = connection.cursor()

        result = cursor.execute(f"SELECT price FROM services WHERE name = '{service}'")

        for row in result:
            self.price = row[0]

        cursor.close()
        connection.close()

        self.prise_lable.label.config(text='Цена: ' + str(self.price))

    def record_information(self):
        # ввод данных в БД
        print('Кнопка нажата')
        self.brand_value = self.brand.entry.get()
        self.model_value = self.model.entry.get()
        self.car_color_value = self.car_color.entry.get()
        self.year_value = self.year.entry.get()
        self.number_value = self.number.entry.get()

        self.name_value = self.name.entry.get()
        self.surname_value = self.surname.entry.get()
        self.phone_number_value = self.phone_number.entry.get()

        # уведомление о вводе данных в БД
        if self.check_all_entries_are_filled():
            self.insert_data_in_database()
            showinfo('Операция прошла успешно', 'Данные загружены!')
            self.print_file()
        else:
            showerror('Ошибка!', 'Не все данные заполнены!')

    def check_all_entries_are_filled(self):
        # проверка заполнение окошек для ввода данных
        if not self.brand_value or not self.model_value or not self.car_color_value or not self.year_value\
                or not self.number_value or not self.name_value or not self.surname_value \
                or not self.phone_number_value or not self.service.combobox.get():
            return False
        else:
            return True

    def insert_data_in_database(self):
        # заполнение БД данными пользователя
        # подключение к БД для заполнение её данными пользователя
        connection = sqlite3.connect('carservice.db')
        cursor = connection.cursor()

        cursor.execute(f"INSERT INTO cars (brand, model, color, year, number)"
                       f"VALUES ('{self.brand_value}', '{self.model_value}', '{self.car_color_value}', "
                       f"'{self.year_value}', '{self.number_value}')")

        result = cursor.execute(f"SELECT max(id) FROM cars")
        for row in result:
            car_id = row[0]

        cursor.execute(f"INSERT INTO customers (name, surname, phone_number, car_id) "
                       f"VALUES ('{self.name_value}','{self.surname_value}','{self.phone_number_value}'"
                       f", '{car_id}')")

        result = cursor.execute(f"SELECT max(id) FROM customers")
        for row in result:
            customers_id = row[0]

        result = cursor.execute(f"SELECT id FROM services WHERE name = '{self.service.combobox.get()}'")
        service_id = result.fetchone()[0]

        cursor.execute(f"INSERT INTO orders (customer_id, service_id) VALUES ('{customers_id}', '{service_id}')")

        connection.commit()

        cursor.close()
        connection.close()

    def print_file(self):
        # создание ленты заказов
        # подключение к БД для получения данных
        connection = sqlite3.connect('carservice.db')
        cursor = connection.cursor()

        result = cursor.execute(f"SELECT "
                                f"subrequest.surname, "
                                f"subrequest.name, "
                                f"subrequest.brand, "
                                f"subrequest.model, "
                                f"services.name, "
                                f"services.price "
                                f"FROM orders "
                                f"INNER JOIN services ON orders.service_id = services.id "
                                f"INNER JOIN "
                                f"(SELECT * FROM customers "
                                f"INNER JOIN cars ON customers.car_id = cars.id) AS subrequest "
                                f"ON subrequest.id = orders.id")

        table = result.fetchall()

        cursor.close()
        connection.close()

        # создание и заполнение данными файла
        file = open('car_information.txt', 'w', encoding='utf8')
        for row in table:
            file.write('---------------------- Новый заказ ----------------------' + '\n')
            file.write('Фамилия клиента: ' + row[0] + '\n')
            file.write('Имя клиента: ' + row[1] + '\n')
            file.write('Бренд автомобиля: ' + row[2] + '\n')
            file.write('Модель автомобиля: ' + row[3] + '\n')
            file.write('Выбранная услуга: ' + row[4] + '\n')
            file.write('Цена услуги: ' + str(row[5]) + '\n')
            file.write('\n')

        file.close()

    def get_list_of_services(self):
        # получение названий услуг
        # подключение БД для получение названий услуг
        list_of_services = []
        connection = sqlite3.connect('carservice.db')
        cursor = connection.cursor()

        result = cursor.execute("SELECT name FROM services")

        for row in result:
            list_of_services.append(row[0])

        cursor.close()
        connection.close()

        return list_of_services


# создание экземпляра класса окно
window = Window()
