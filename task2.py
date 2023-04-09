# Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с
# информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для
# этого:
# a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар
# (item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция
# должна предусматривать запись данных в виде словаря в файл orders.json. При
# записи данных указать величину отступа в 4 пробельных символа;
# b. Проверить работу программы через вызов функции write_order_to_json() с передачей
# в нее значений каждого параметра.
import json
import locale
from datetime import datetime


class Order:

    def __init__(self, item: str, quantity: int, price: float, buyer: str, date: str):
        self.item: str = item
        self.quantity: int = quantity
        self.price: float = price
        self.buyer: str = buyer
        self.date: str = date

    def write_order_to_json(self, filepath: str = './var/orders.json'):
        system_encoding = locale.getpreferredencoding()
        with open(filepath, 'w', encoding=system_encoding) as f:
            json.dump(self.__dict__, f, indent=4)


if __name__ == '__main__':
    order = Order(item='car', quantity=10, price=300.10, buyer='user1', date=str(datetime.now()))
    order.write_order_to_json()
