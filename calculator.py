import tkinter as tk
from tkinter import ttk
import math
import re

class ScientificCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Научный Калькулятор")
        self.root.geometry("420x620")
        self.root.resizable(False, False)
        
        # Переменные
        self.expression = ""
        self.memory = 0
        
        self.create_widgets()
        
    def create_widgets(self):
        # Стиль
        style = ttk.Style()
        style.theme_use('clam')
        
        # Дисплей
        self.display = tk.Entry(self.root, font=("Arial", 24), 
                               justify="right", bd=10, relief=tk.SUNKEN)
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=15, 
                         ipadx=8, ipady=20, sticky="ew")
        self.display.insert(0, "0")
        
        # Кнопки
        buttons = [
            ('MC', 1, 0), ('MR', 1, 1), ('M+', 1, 2), ('M-', 1, 3), ('C', 1, 4),
            ('sin', 2, 0), ('cos', 2, 1), ('tan', 2, 2), ('√', 2, 3), ('x²', 2, 4),
            ('log', 3, 0), ('ln', 3, 1), ('π', 3, 2), ('e', 3, 3), ('(', 3, 4),
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('/', 4, 3), (')', 4, 4),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('*', 5, 3), ('%', 5, 4),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('-', 6, 3), ('^', 6, 4),
            ('0', 7, 0), ('.', 7, 1), ('=', 7, 2), ('+', 7, 3), ('⌫', 7, 4),
        ]
        
        # Цвета
        num_color = "#f0f0f0"
        op_color = "#ff9500"
        sci_color = "#a0a0a0"
        equal_color = "#00c853"
        
        for (text, row, col) in buttons:
            if text in '0123456789.':
                bg_color = num_color
            elif text in '+-*/':
                bg_color = op_color
            elif text == '=':
                bg_color = equal_color
            else:
                bg_color = sci_color
                
            btn = tk.Button(self.root, text=text, font=("Arial", 14, "bold"),
                          height=2, width=5, bg=bg_color, fg="black",
                          activebackground="#ddd")
            
            if text == '=':
                btn.grid(row=row, column=col, columnspan=1, padx=2, pady=2, sticky="nsew")
            else:
                btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            # Привязка команд
            if text == 'C':
                btn.config(command=self.clear)
            elif text == '⌫':
                btn.config(command=self.backspace)
            elif text == '=':
                btn.config(command=self.calculate, bg=equal_color, fg="white")
            elif text in ('sin', 'cos', 'tan', 'log', 'ln', '√', 'x²'):
                btn.config(command=lambda t=text: self.scientific_function(t))
            elif text == 'π':
                btn.config(command=lambda: self.add_to_expression(str(math.pi)))
            elif text == 'e':
                btn.config(command=lambda: self.add_to_expression(str(math.e)))
            elif text == '^':
                btn.config(command=lambda: self.add_to_expression('**'))
            elif text == '%':
                btn.config(command=lambda: self.add_to_expression('%'))
            elif text in ('MC', 'MR', 'M+', 'M-'):
                btn.config(command=lambda t=text: self.memory_function(t))
            else:
                btn.config(command=lambda t=text: self.add_to_expression(t))
        
        # Настройка весов колонок и строк
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(1, 8):
            self.root.grid_rowconfigure(i, weight=1)
        
        # Привязка клавиатуры
        self.root.bind('<Key>', self.key_press)
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
    
    def add_to_expression(self, value):
        if self.display.get() == "0" and value not in "+-*/":
            self.display.delete(0, tk.END)
        self.display.insert(tk.END, value)
    
    def clear(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, "0")
    
    def backspace(self):
        current = self.display.get()
        if len(current) > 1:
            self.display.delete(len(current)-1, tk.END)
        else:
            self.display.delete(0, tk.END)
            self.display.insert(0, "0")
    
    def scientific_function(self, func):
        try:
            value = float(self.display.get())
            result = 0
            
            if func == 'sin':
                result = math.sin(math.radians(value))
            elif func == 'cos':
                result = math.cos(math.radians(value))
            elif func == 'tan':
                result = math.tan(math.radians(value))
            elif func == 'log':
                result = math.log10(value)
            elif func == 'ln':
                result = math.log(value)
            elif func == '√':
                result = math.sqrt(value)
            elif func == 'x²':
                result = value ** 2
                
            self.display.delete(0, tk.END)
            self.display.insert(0, str(round(result, 8)))
        except:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Ошибка")
    
    def memory_function(self, operation):
        try:
            current = float(self.display.get())
            if operation == 'MC':
                self.memory = 0
            elif operation == 'MR':
                self.display.delete(0, tk.END)
                self.display.insert(0, str(self.memory))
            elif operation == 'M+':
                self.memory += current
            elif operation == 'M-':
                self.memory -= current
        except:
            pass
    
    def calculate(self):
        try:
            expression = self.display.get()
            # Замена символов
            expression = expression.replace('^', '**')
            expression = expression.replace('π', str(math.pi))
            expression = expression.replace('e', str(math.e))
            
            # Вычисление
            result = eval(expression, {"__builtins__": {}}, 
                         {"math": math, "sin": math.sin, "cos": math.cos, 
                          "tan": math.tan, "sqrt": math.sqrt, "log": math.log10})
            
            self.display.delete(0, tk.END)
            # Красивый вывод
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.display.insert(0, str(result))
        except ZeroDivisionError:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Деление на ноль")
        except:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Ошибка")
    
    def key_press(self, event):
        key = event.char
        if key in '0123456789.+-*/()':
            self.add_to_expression(key)
        elif key == '%':
            self.add_to_expression('%')
    
    def run(self):
        self.root.mainloop()


# Запуск калькулятора
if __name__ == "__main__":
    calc = ScientificCalculator()
    calc.run()