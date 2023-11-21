import os
import sys

if hasattr(sys, '_MEIPASS'):
    os.environ['KIVY_NO_CONSOLELOG'] = '1'

import kivy
from kivy.config import Config
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.app import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty


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



# Designate our .kv design file
Builder.load_file(resource_path("calc.kv"))



class CalcLayout(Widget):

    expression = StringProperty('')
    def __init__(self, **kwargs):
        super(CalcLayout, self).__init__(**kwargs)
        self.expression = ''
        self.new_operad = True
        self.new_expression = True
        self.error = False   
    
        
        
        
    def clear(self):
        self.ids.input.text = '0'
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
            self.expression = ''
        

        if self.new_operad:
            self.ids.input.text = digit
            self.new_operad = False
        else:
            self.ids.input.text = digit if self.ids.input.text == '0' else self.ids.input.text + digit
        
        
                      
    
            
            
    # create decimal function
    def dot_press(self):
        if self.error:
            self.clear()
        if self.new_expression:
            self.new_expression = False
            self.ids.input.text = ''
            self.expression = ''
            self.new_operad = False
            
        if not self.ids.input.text:
             self.ids.input.text = '0.'
        elif '.' not in self.ids.input.text:
                self.ids.input.text += '.'
            
            
    
    def flip_sign(self):
        if self.error:
            self.clear()
        if self.ids.input.text.startswith('-'):
            self.ids.input.text = self.ids.input.text[1:]
        elif self.ids.input.text != '0':
            self.ids.input.text = f'-{self.ids.input.text}' 
            
        
    def operator_press(self, operator):
        if self.error:
            self.clear()
        if self.new_expression:
            self.new_expression = False
            self.expression = ''
        self.expression += f'{self.ids.input.text}{operator}'
        self.calculate()    
            
        
        
    def equals(self):
        print('equals')
        if not self.new_expression:
            self.expression += self.ids.input.text
            self.calculate()
            self.expression = f'{self.expression} = {self.ids.input.text}'
            self.new_expression = True
    
            
            
    def calculate(self):
       
        try:
           
            exp = self.expression
            if exp.endswith(('-', '+', 'x', '÷')):
                exp = exp[:-1]
            exp = exp.replace('÷','/')
            exp = exp.replace('x','*')
            result = decimal.Decimal(eval(exp))
            result = result.quantize(decimal.Decimal('0.00000000000'))
            result = self.format_result(result)
            self.ids.input.text= str(result)
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
        except SyntaxError :
            self.ids.input.text =  "Invalid Input"
            self.new_expression = True
            self.new_operad = True
            self.error = True
        except Exception as e:
            print(e)
            self.ids.input.text =  "Nunkown error"
            self.new_expression = True
            self.new_operad = True
            self.error = True
        
    def format_result(self, result: decimal.Decimal ):
        r = str(result).rstrip('0')
        if r.endswith('.'):
            r = r[:-1]
        if len(r) > 13:
            result = result.normalize()
            self.ids.input.font_size = 32
            self.ids.expression.font_size = 16
        else:
            result = r
            self.ids.input.font_size = 64
            self.ids.expression.font_size = 32

        return result


    
class ClacApp(App):
    def build(self): 
        # Set the app size
        Window.size = (500, 800)

        return CalcLayout()
    
   
    

if __name__ == "__main__":
    ClacApp().run() 