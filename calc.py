import os
import sys

import locale
locale.setlocale(locale.LC_ALL, '')

from decimal import Decimal, getcontext
getcontext().prec = 10

if hasattr(sys, '_MEIPASS'):
    os.environ['KIVY_NO_CONSOLELOG'] = '1'

from kivy.config import Config
Config.set('graphics', 'resizable', False)
# Set the icon file path
icon_path = 'icon.png'

# Set the icon in the Config
Config.set('kivy', 'window_icon', icon_path)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.app import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty


# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Designate our .kv design file
Builder.load_file(resource_path("calc.kv"))

class CalcLayout(Widget):
    DECIMAL_POINT = StringProperty(locale.localeconv()['mon_decimal_point'])
    THOUSANDS_SEP = StringProperty(locale.localeconv()['mon_thousands_sep'])
    input_max_lenght = 21
    expression = StringProperty('')
    def __init__(self, **kwargs):
        super(CalcLayout, self).__init__(**kwargs)
        self.first_operand = ''
        self.second_operand = ''
        self.operator = ''
        self.last_is_operator = False
        self.last_is_equal = False
        self.error = False
        
    
    def clear(self):
        self.first_operand = ''
        self.second_operand = ''
        self.operator = ''
        self.expression = ''
        self.last_is_operator = False
        self.last_is_equal = False
        self.error = False
        self.ids.input.text = '0'

       
    def remove(self):
        if self.error or self.last_is_equal:
            self.clear()
        elif self.ids.input.text:
            self.ids.input.text = self.ids.input.text[:-1]
            if not self.ids.input.text :
                self.ids.input.text = '0'

    def clear_input(self):
        if self.error or self.last_is_equal:
            self.clear()
        else:
            self.ids.input.text = '0'
        
            
    def dot_press(self):
        if self.error:
            self.clear()
        else:
            if self.last_is_equal:
                self.expression = ''
                self.ids.input.text = '0'
            if self.DECIMAL_POINT not in self.ids.input.text:
                self.ids.input.text += self.DECIMAL_POINT


    def flip_sign(self):
        if self.error:
            self.clear()
        elif self.last_is_equal:
            tmp = self.ids.input.text
            self.clear()
            self.ids.input.text = tmp
        else:
            if self.ids.input.text.startswith('-'):
                self.ids.input.text = self.ids.input.text[1:]
            elif self.ids.input.text != '0':
                self.ids.input.text = f'-{self.ids.input.text}'  


    def update_text(self):
        self.ids.input.font_size = min(48,max(10/(len(self.ids.input.text)+1) * 64, 25))
        if len(self.ids.input.text) > self.input_max_lenght:
            self.ids.input.text = self.ids.input.text[:-1]

        
    def digit_press(self, digit):
        if self.error:
            self.clear()
        else:
            if self.last_is_equal:
                self.ids.input.text = digit
                self.expression = ''
                self.last_is_equal = False
            elif self.last_is_operator:
                self.ids.input.text =  digit
                self.last_is_operator = False
            else:
                self.ids.input.text = digit if self.ids.input.text == '0' else self.ids.input.text + digit
                self.last_is_operator = False
        tmp =  f'{self.str_to_decimal(self.ids.input.text):n}'
        print('tmp: ', tmp)
        self.ids.input.text = tmp
        print('text : ', self.ids.input.text)

            
        

    def operator_press(self, operator):
        if self.error:
            self.clear()
        else:
            if self.last_is_equal:
                self.operator = operator
                self.first_operand = self.ids.input.text
                self.last_is_equal = False
                self.expression = f'{self.first_operand} {self.operator}'
            elif  self.last_is_operator: 
                self.operator = operator
                self.first_operand = self.ids.input.text
                self.expression = f'{self.first_operand} {self.operator}'
            else:
                if self.first_operand:
                    self.second_operand = self.ids.input.text
                    self.calculate() # result is stored in input.text
                self.operator = operator
                self.first_operand = self.ids.input.text
                self.expression = f'{self.first_operand} {self.operator}'
            self.last_is_operator = True



            

    def equals(self):
        if self.error:
            self.clear()
        else:
            self.expression = f'{self.first_operand} {self.operator} {self.ids.input.text}'
            self.second_operand = self.ids.input.text
            self.calculate()
            self.expression = self.expression + ' = ' + self.ids.input.text
            self.last_is_equal = True
    
            
            
    def calculate(self):
        if not self.operator:
            return
        try:
            if self.operator == '+':
                result = self.str_to_decimal(self.first_operand)+self.str_to_decimal(self.second_operand)
            elif self.operator == '-':
                result = self.str_to_decimal(self.first_operand)-self.str_to_decimal(self.second_operand)
            elif self.operator == 'x':
                result = self.str_to_decimal(self.first_operand)*self.str_to_decimal(self.second_operand)
            elif self.operator == '÷':
                result = self.str_to_decimal(self.first_operand)/self.str_to_decimal(self.second_operand)
        except ZeroDivisionError:
            result = 'Zero Division Error'
            self.error = True
        except:
            result = 'Error'
            self.error = True
        self.ids.input.text = self.decimal_to_str_locale(result) if not self.error else result


    def str_to_decimal(self, num_str: str) -> Decimal:
        num_str = num_str.replace(self.THOUSANDS_SEP, '').replace(self.DECIMAL_POINT, '.')
        return Decimal(num_str)
            

    def decimal_to_str_locale(self, num: Decimal) -> str:
        if len(str(f'{num:n}')) < 11:
            return f'{num:n}'
        else:
            return str(num.normalize())  

            



class ClacApp(App):
    title = "Kivy Calculator"
    def build(self): 
        Window.clearcolor = (43/255, 26/255, 36/255,1)
        Window.size = (333, 500)
        return CalcLayout()
    

if __name__ == "__main__":
    ClacApp().run() 