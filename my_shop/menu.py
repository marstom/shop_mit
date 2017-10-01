'''
Menu for shop client.
'''

import sys
from my_shop.baza import DataSQL
from my_shop.koszyk import Cart
from my_shop.klient import Customer
from my_shop.ui import UserInterface

import os


class Menu:
    def __init__(self, db_file):
        self.ui = UserInterface()
        self.db_file = db_file
        self.customer = Customer(self.db_file, self.ui)
        self.switch = {'-1': self.ui.error_message,
                       '1': self.products_list,
                       '2': self.add_to_cart,
                       '3': self.show_cart,
                       '4': self.edit_cart,
                       '5': self.finish,
                       '6': self.help_shop,
                       '7': self.end
                       }
        self.cart = Cart(self.ui)

    def products_list(self):
        print(self.ui.messages['products_list'])
        with DataSQL(self.db_file) as db:
            products = db.product_list_string()
            print(products)

    def show_cart(self, customer=None): #todo show cart for particular customer, cart printing shall be in ui
        content = self.cart.get_cart_content()
        print(content)

    def add_to_cart(self):
        print(self.ui.messages['add_to_cart'])
        prod_id = self.ui.cart_product_id()
        with DataSQL(self.db_file) as db:
            try:
                prod = db.get_product(prod_id)
            except Exception:
                self.ui.error_message('no_such_index')
                return '-1'
        quantity = self.ui.cart_product_quantity()
        quantity = int(quantity)
        self.cart.add_product(prod, quantity)

    def edit_cart(self):
        print(self.ui.messages['edit_cart'])
        prod_name = self.ui.in_product_name()
        print(self.ui.messages['edit_cart_choose'])
        choice = self.ui.in_edit_cart()
        if choice == '1':
            self.cart.remove_product(prod_name)
        elif choice == '2':
            self.cart.update_product(prod_name)

    def finish(self):  # TODO, write to database
        print(self.ui.messages['end_or_order'])
        cust = self.customer.get_customer() #returns (int id, name, passwd)
        cart_content = self.show_cart(cust) #todo, implement show cart
        print('uzytkownik to: ', cust) #todo, move show cart method

    def help_shop(self):
        print(self.ui.messages['user_options_help_message'])

    def run(self):
        os.system('cls')  # TODO, windows->cls, unix->clear
        print(self.ui.messages['hello'])
        print(self.ui.messages['user_options_help_message'])

        while True:
            self.main_proggramm()

    def main_proggramm(self):
        choice_id = self.ui.validate_input(self.ui.input_main_menu(),
                                           self.switch.keys())
        choice = self.switch[choice_id]
        choice()

    def end(self):
        sys.exit(0)


def main(path):
    m = Menu(path)
    m.run()


if __name__ == '__main__':
    main('shop_data_base.db')
