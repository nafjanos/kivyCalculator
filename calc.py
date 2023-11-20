import os
import sys

if hasattr(sys, '_MEIPASS'):
    os.environ['KIVY_NO_CONSOLELOG'] = '1'

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.app import Builder
from kivy.core.window import Window
import re
import decimal



# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Set the app size
Window.size = (500, 700)

# Designate our .kv design file
Builder.load_file(resource_path("calc.kv"))

class CalcLayout(Widget):
    
    def __init__(self, **kwargs):
        super(CalcLayout, self).__init__(**kwargs)
        self.expression = ''
        self.new_operad = True
        self.new_expression = True
        self.error = False
        
        
        
        
    def clear(self):
        self.ids.input.text = '0'
        self.ids.expression.text = ''
        self.expression = ''
        self.new_expression = True
        self.new_operad = True
        self.error = False
       
       
       
    def remove(self):
        if self.error:
            self.clear()
        else:
            if self.ids.input.text :
                self.ids.input.text = self.ids.input.text[:-1]
            
            if not self.ids.input.text :
                self.ids.input.text = '0'
            
        
            
        
        
    def add_digit(self, digit):
        if self.error or self.new_expression:
            self.clear()
        
        if self.new_expression: 
            self.new_expression = False
            self.ids.expression.text = ''
            self.expression = ''
        

        if self.new_operad:
            self.ids.input.text = digit
            self.new_operad = False
        else:
            self.ids.input.text = digit if self.ids.input.text == '0' else self.ids.input.text + digit
        
        
                      
    def operator_press(self, operator):
        if self.error:
            self.clear()
        if self.new_expression:
            self.new_expression = False
            self.ids.expression.text = ''
            self.expression = ''
        print('befor: ', self.expression)
        self.ids.expression.text += f'{self.ids.input.text}{operator}'
        if '.' in self.ids.input.text:
            self.expression += f'{self.ids.input.text}{operator}'
        else:
            self.expression += f'{self.ids.input.text}{operator}'
        print('after : ', self.expression)
        self.calculate()
            
            
    # create decimal function
    def dot_press(self):
        if self.error:
            self.clear()
        if self.new_expression:
            self.new_expression = False
            self.ids.input.text = ''
            self.ids.expression.text = ''
            self.expression = ''
            self.new_operad = False
            
        if not self.ids.input.text:
             self.ids.input.text = '0.'
        else:
            if '.' not in self.ids.input.text:
                self.ids.input.text += '.'
            
            
    
    def flip_sign(self):
        if self.error:
            self.clear()
        if self.ids.input.text.startswith('-'):
            self.ids.input.text = self.ids.input.text[1:]
        elif self.ids.input.text != '0':
            self.ids.input.text = f'-{self.ids.input.text}' 
            
        
        
            
        
        
    def equals(self):
        if not self.new_expression:
            self.ids.expression.text += self.ids.input.text
            if '.' in self.ids.input.text:
                self.expression = f'{self.expression}{self.ids.input.text}'
            else:
                self.expression = f'{self.expression}{self.ids.input.text}.0' 
            self.calculate()
            self.ids.expression.text = f'{self.ids.expression.text } = {self.ids.input.text}'
            self.new_expression = True
    
            
            
    def calculate(self):
        exp = ''
        try:
            if self.expression.endswith(('-', '+', '*', '/')):
                exp = self.expression[:-1]
            else:
                exp = self.expression
            print(decimal.getcontext())
            result = decimal.Decimal(eval(exp))
            result = result.quantize(decimal.Decimal('0.00000000000'))
            self.ids.input.text = str(result.normalize())
            self.new_operad = True
        except ZeroDivisionError:
            self.ids.input.text = "Can't Divide by Zero"
            self.new_expression = True
            self.new_operad = True
            self.error = True
        except ValueError:
            self.ids.input.text =  "Value Error"
            self.new_expression = True
            self.new_operad = True
            self.error = True
        except SyntaxError:
            self.ids.input.text =  "Invalid Input"
            self.new_expression = True
            self.new_operad = True
            self.error = True
        except: 
            self.ids.input.text =  "Nunkown error"
            self.new_expression = True
            self.new_operad = True
            self.error = True
        
       
        
    
class ClacApp(App):
    def build(self): 
        #Window.clearcolor = (1,1,1,1)
        return CalcLayout()

if __name__ == "__main__":
    ClacApp().run() 