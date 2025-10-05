import tkinter as tk
from tkinter import messagebox, ttk
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("MPK Cal")
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        
        self.unit_factors = {
            "Length": {"Meter": 1.0, "Centimeter": 0.01, "Kilometer": 1000.0, "Inch": 0.0254, "Foot": 0.3048},
            "Mass": {"Kilogram": 1.0, "Gram": 0.001, "Pound": 0.453592, "Ounce": 0.0283495},
            "Volume": {"Liter": 1.0, "Milliliter": 0.001, "Gallon": 3.78541, "Pint": 0.473176}
        }
        
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.result = 0
        self.deg = True
        self.base = "DEC"  # Current number base: DEC, BIN, OCT, HEX
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.calc_frame = tk.Frame(self.notebook)
        self.conv_frame = tk.Frame(self.notebook)
        self.graph_frame = tk.Frame(self.notebook)
        self.prog_frame = tk.Frame(self.notebook)  # New programmer frame
        self.notebook.add(self.calc_frame, text="Scientific")
        self.notebook.add(self.conv_frame, text="Converter")
        self.notebook.add(self.graph_frame, text="Graphing")
        self.notebook.add(self.prog_frame, text="Programmer")  # Add programmer tab
        self.notebook.pack(expand=1, fill="both", padx=3, pady=3)
        
        self.build_calculator(self.calc_frame)
        self.build_converter(self.conv_frame)
        self.build_graph(self.graph_frame)
        self.build_programmer(self.prog_frame)  # Build programmer interface
    
    def build_calculator(self, parent):
        # Display
        self.display = tk.Entry(parent, font=("Arial", 40), justify="right", bg="white", bd=1, relief="solid")
        self.display.grid(row=0, column=0, columnspan=6, padx=3, pady=3, sticky="ew")
        
        # DEG/RAD button
        self.dr_button = tk.Button(parent, text="DEG", font=("Arial", 10), bg="lightblue", fg="black", 
                                   height=1, width=3, command=self.toggle_deg_rad)
        self.dr_button.grid(row=1, column=5, padx=1, pady=1, sticky="nsew")
        
        # Buttons configuration
        self.buttons = [
            ('C', 1, 0), ('+/-', 1, 1), ('%', 1, 2), ('/', 1, 3), ('*', 1, 4),
            ('sin', 2, 0), ('cos', 2, 1), ('tan', 2, 2), ('-', 2, 3), ('√', 2, 4),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('+', 3, 3), ('x²', 3, 4),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('1/x', 4, 3), ('log', 4, 4),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('=', 5, 3, 2),
            ('0', 6, 0, 2), ('.', 6, 2), ('^', 6, 3), ('π', 6, 4),
            ('asin', 7, 0), ('acos', 7, 1), ('atan', 7, 2), ('ln', 7, 3), ('e^x', 7, 4)
        ]
        
        self.create_buttons(parent)
        
        # Configure grid weights
        for i in range(8):
            parent.grid_rowconfigure(i, weight=1)
        for i in range(6):
            parent.grid_columnconfigure(i, weight=1)
        
        self.update_display()
    
    def build_programmer(self, parent):
        # Base selection
        base_frame = tk.Frame(parent)
        base_frame.grid(row=0, column=0, columnspan=6, sticky="ew", padx=3, pady=3)
        
        tk.Label(base_frame, text="Base:", font=("Arial", 10)).pack(side="left")
        
        self.base_var = tk.StringVar(value="DEC")
        bases = [("DEC", "DEC"), ("HEX", "HEX"), ("OCT", "OCT"), ("BIN", "BIN")]
        for text, base in bases:
            tk.Radiobutton(base_frame, text=text, variable=self.base_var, 
                          value=base, font=("Arial", 9), 
                          command=self.on_base_change).pack(side="left", padx=5)
        
        # Programmer display
        self.prog_display = tk.Entry(parent, font=("Arial", 20), justify="right", 
                                   bg="white", bd=1, relief="solid")
        self.prog_display.grid(row=1, column=0, columnspan=6, padx=3, pady=3, sticky="ew")
        
        # Bit display
        self.bit_display = tk.Label(parent, text="", font=("Arial", 20), 
                                  bg="lightgray", relief="sunken", anchor="w")
        self.bit_display.grid(row=2, column=0, columnspan=6, padx=3, pady=2, sticky="ew")
        
        # Programmer buttons
        prog_buttons = [
            ('C', 3, 0), ('<<', 3, 1), ('>>', 3, 2), ('&', 3, 3), ('|', 3, 4), ('^', 3, 5),
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('~', 4, 3), ('MOD', 4, 4), ('A', 4, 5),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('(', 5, 3), (')', 5, 4), ('B', 5, 5),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('+', 6, 3), ('-', 6, 4), ('C', 6, 5),
            ('0', 7, 0, 2), ('.', 7, 2), ('*', 7, 3), ('/', 7, 4), ('D', 7, 5),
            ('E', 8, 0), ('F', 8, 1), ('=', 8, 2, 2), ('XOR', 8, 4), ('AND', 8, 5)
        ]
        
        self.create_prog_buttons(parent, prog_buttons)
        
        # Configure grid weights
        for i in range(9):
            parent.grid_rowconfigure(i, weight=1)
        for i in range(6):
            parent.grid_columnconfigure(i, weight=1)
        
        self.update_prog_display()
    
    def create_prog_buttons(self, parent, buttons):
        for btn_data in buttons:
            text = btn_data[0]
            row = btn_data[1]
            col = btn_data[2]
            colsp = btn_data[3] if len(btn_data) > 3 else 1
            
            # Determine command and styling
            if text.isdigit() or text in 'ABCDEF.':
                cmd = lambda n=text: self.prog_add_digit(n)
                bg = "#f0f0f0"
                fg = "black"
            elif text == 'C':
                cmd = self.prog_clear
                bg = "#e74c3c"
                fg = "white"
            elif text in ['+', '-', '*', '/', 'MOD']:
                op = '%' if text == 'MOD' else text
                cmd = lambda o=op: self.prog_set_operator(o)
                bg = "#3498db"
                fg = "white"
            elif text in ['&', '|', '^', '<<', '>>', '~', 'AND', 'XOR']:
                cmd = lambda o=text: self.prog_set_bitwise_operator(o)
                bg = "#9b59b6"
                fg = "white"
            elif text == '=':
                cmd = self.prog_calculate
                bg = "#e67e22"
                fg = "white"
            elif text in ['(', ')']:
                cmd = lambda: self.prog_add_digit(text)
                bg = "#95a5a6"
                fg = "white"
            else:
                cmd = lambda: None
                bg = "#f0f0f0"
                fg = "black"
            
            height = 1
            width = 3 if colsp == 2 else 2
            btn = tk.Button(parent, text=text, font=("Arial", 10), command=cmd,
                            bg=bg, fg=fg, height=height, width=width, relief="raised", bd=1)
            btn.grid(row=row, column=col, columnspan=colsp, padx=1, pady=1, sticky="nsew")
    
    def build_converter(self, parent):
        # Category row
        tk.Label(parent, text="Category:", font=("Arial", 9)).grid(row=0, column=0, sticky="w", padx=3, pady=1)
        self.category_var = tk.StringVar(value="Length")
        cat_values = list(self.unit_factors.keys()) + ["Temperature"]
        self.cat_combo = ttk.Combobox(parent, textvariable=self.category_var, values=cat_values, state="readonly", width=10)
        self.cat_combo.grid(row=0, column=1, sticky="ew", padx=3, pady=1)
        self.cat_combo.bind("<<ComboboxSelected>>", self.update_units)
        
        # From frame (left column)
        from_frame = tk.Frame(parent)
        from_frame.grid(row=1, column=0, sticky="nsew", padx=3, pady=2)
        tk.Label(from_frame, text="From", font=("Arial", 10, "bold")).pack(pady=(0, 1))
        tk.Label(from_frame, text="Unit:", font=("Arial", 8)).pack(anchor="w", pady=0)
        self.from_var = tk.StringVar()
        self.from_combo = ttk.Combobox(from_frame, textvariable=self.from_var, state="readonly", width=15)
        self.from_combo.pack(fill="x", pady=0)
        self.from_combo.bind("<<ComboboxSelected>>", self.on_unit_change)
        tk.Label(from_frame, text="Value:", font=("Arial", 8)).pack(anchor="w", pady=0)
        self.value_entry = tk.Entry(from_frame, font=("Arial", 10), justify="right", width=15)
        self.value_entry.pack(fill="x", pady=0)
        self.value_entry.bind("<KeyRelease>", self.on_value_change)
        
        # To frame (right column)
        to_frame = tk.Frame(parent)
        to_frame.grid(row=1, column=1, sticky="nsew", padx=3, pady=2)
        tk.Label(to_frame, text="To", font=("Arial", 10, "bold")).pack(pady=(0, 1))
        tk.Label(to_frame, text="Unit:", font=("Arial", 8)).pack(anchor="w", pady=0)
        self.to_var = tk.StringVar()
        self.to_combo = ttk.Combobox(to_frame, textvariable=self.to_var, state="readonly", width=15)
        self.to_combo.pack(fill="x", pady=0)
        self.to_combo.bind("<<ComboboxSelected>>", self.on_unit_change)
        tk.Label(to_frame, text="Result:", font=("Arial", 8)).pack(anchor="w", pady=0)
        self.result_label = tk.Label(to_frame, text="0", font=("Arial", 12), bg="lightgray", relief="sunken", anchor="e", width=15)
        self.result_label.pack(fill="x", pady=0)
        
        # Swap button (below)
        self.swap_btn = tk.Button(parent, text="↔ Swap", font=("Arial", 8), command=self.swap_units, bg="lightblue", width=6)
        self.swap_btn.grid(row=2, column=0, columnspan=2, pady=3)
        
        # Configure grid weights for responsiveness
        parent.grid_rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        
        self.update_units()
    
    def build_graph(self, parent):
        # Function input - single row layout
        func_frame = tk.Frame(parent)
        func_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=3, pady=1)
        tk.Label(func_frame, text="f(x)=", font=("Arial", 9)).pack(side="left")
        self.func_entry = tk.Entry(func_frame, font=("Arial", 9), width=12)
        self.func_entry.insert(0, "x**2")
        self.func_entry.pack(side="left", fill="x", expand=True, padx=2)
        
        # X range in one row
        range_frame = tk.Frame(parent)
        range_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=3, pady=1)
        tk.Label(range_frame, text="X:", font=("Arial", 8)).pack(side="left")
        self.xmin_entry = tk.Entry(range_frame, font=("Arial", 8), width=4)
        self.xmin_entry.insert(0, "-10")
        self.xmin_entry.pack(side="left", padx=1)
        tk.Label(range_frame, text="to", font=("Arial", 8)).pack(side="left")
        self.xmax_entry = tk.Entry(range_frame, font=("Arial", 8), width=4)
        self.xmax_entry.insert(0, "10")
        self.xmax_entry.pack(side="left", padx=1)
        
        # Plot button
        self.plot_btn = tk.Button(parent, text="Plot", font=("Arial", 9), command=self.plot_function, bg="lightblue", height=1)
        self.plot_btn.grid(row=2, column=0, columnspan=4, pady=2, sticky="ew")
        
        # Canvas frame
        self.canvas_frame = tk.Frame(parent)
        self.canvas_frame.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=3, pady=3)
        
        # Configure for responsiveness
        parent.grid_rowconfigure(3, weight=1)
        parent.columnconfigure(0, weight=1)
    
    def create_buttons(self, parent):
        for btn_data in self.buttons:
            text = btn_data[0]
            row = btn_data[1]
            col = btn_data[2]
            colsp = btn_data[3] if len(btn_data) > 3 else 1
            
            # Determine command and styling
            if text.isdigit() or text == '.':
                cmd = lambda n=text: self.add_digit(n)
                bg = "#f0f0f0"
                fg = "black"
            elif text == 'C':
                cmd = self.clear
                bg = "#e74c3c"
                fg = "white"
            elif text == '+/-':
                cmd = self.toggle_sign
                bg = "#f0f0f0"
                fg = "black"
            elif text == '%':
                cmd = self.percent
                bg = "#f0f0f0"
                fg = "black"
            elif text in ['/', '*', '-', '+', '^']:
                op = '**' if text == '^' else text
                cmd = lambda o=op: self.set_operator(o)
                bg = "#3498db"
                fg = "white"
            elif text == '=':
                cmd = self.calculate
                bg = "#e67e22"
                fg = "white"
            elif text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                func = getattr(math, text)
                if text.startswith('a'):
                    cmd = lambda f=func: self.apply_inverse_trig(f)
                else:
                    cmd = lambda f=func: self.apply_trig(f)
                bg = "#95a5a6"
                fg = "white"
            elif text == 'log':
                cmd = lambda: self.apply_unary(math.log10)
                bg = "#95a5a6"
                fg = "white"
            elif text == 'ln':
                cmd = lambda: self.apply_unary(math.log)
                bg = "#95a5a6"
                fg = "white"
            elif text == 'e^x':
                cmd = lambda: self.apply_unary(math.exp)
                bg = "#95a5a6"
                fg = "white"
            elif text == '√':
                cmd = lambda: self.apply_unary(math.sqrt)
                bg = "#95a5a6"
                fg = "white"
            elif text == 'x²':
                cmd = lambda: self.apply_unary(lambda x: x * x)
                bg = "#95a5a6"
                fg = "white"
            elif text == '1/x':
                cmd = lambda: self.apply_unary(lambda x: 1 / x if x != 0 else 0)
                bg = "#95a5a6"
                fg = "white"
            elif text == 'π':
                cmd = self.set_pi
                bg = "#95a5a6"
                fg = "white"
            else:
                cmd = lambda: None
                bg = "#f0f0f0"
                fg = "black"
            
            height = 1
            width = 3 if colsp == 2 else 2
            btn = tk.Button(parent, text=text, font=("Arial", 10), command=cmd,
                            bg=bg, fg=fg, height=height, width=width, relief="raised", bd=1)
            btn.grid(row=row, column=col, columnspan=colsp, padx=1, pady=1, sticky="nsew")

    # Calculator methods
    def update_display(self):
        self.display.delete(0, tk.END)
        display_text = self.current if self.current != "0" else "0"
        self.display.insert(0, display_text)
    
    def add_digit(self, num):
        if num == '.' and '.' in self.current:
            return
        if self.current == "0" and num != '.':
            self.current = num
        else:
            self.current += num
        self.update_display()
    
    def set_operator(self, op):
        if self.current == "":
            return
        if self.previous != "":
            self.calculate()
        self.previous = self.current
        self.operator = op
        self.current = ""
    
    def calculate(self):
        if self.previous == "" or self.operator == "" or self.current == "":
            return
        
        prev = float(self.previous)
        curr = float(self.current)
        
        try:
            if self.operator == '+':
                self.result = prev + curr
            elif self.operator == '-':
                self.result = prev - curr
            elif self.operator == '*':
                self.result = prev * curr
            elif self.operator == '/':
                if curr == 0:
                    raise ZeroDivisionError
                self.result = prev / curr
            elif self.operator == '**':
                self.result = prev ** curr
            
            self.current = str(self.result)
            self.previous = ""
            self.operator = ""
        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero!")
            self.clear()
        except ValueError:
            messagebox.showerror("Error", "Invalid calculation")
            self.clear()
        
        self.update_display()
    
    def clear(self):
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.result = 0
        self.update_display()
    
    def toggle_sign(self):
        if self.current != "0":
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
            self.update_display()
    
    def percent(self):
        try:
            val = float(self.current)
            self.current = str(val / 100)
            self.update_display()
        except ValueError:
            pass
    
    def apply_unary(self, func):
        try:
            val = float(self.current)
            if val <= 0 and 'log' in func.__name__:
                raise ValueError("Log of non-positive number")
            res = func(val)
            self.current = str(res)
        except ValueError:
            messagebox.showerror("Error", "Invalid input")
            self.clear()
        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero!")
            self.clear()
        self.update_display()
    
    def apply_trig(self, func):
        try:
            val = float(self.current)
            if self.deg:
                val = math.radians(val)
            res = func(val)
            self.current = str(res)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for trig function")
            self.clear()
        self.update_display()
    
    def apply_inverse_trig(self, func):
        try:
            val = float(self.current)
            res = func(val)
            if self.deg:
                res = math.degrees(res)
            self.current = str(res)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for inverse trig function")
            self.clear()
        self.update_display()
    
    def set_pi(self):
        self.current = str(math.pi)
        self.update_display()
    
    def toggle_deg_rad(self):
        self.deg = not self.deg
        self.dr_button.config(text="DEG" if self.deg else "RAD")
    
    # Programmer calculator methods
    def on_base_change(self):
        self.base = self.base_var.get()
        self.update_prog_display()
    
    def update_prog_display(self):
        self.prog_display.delete(0, tk.END)
        if hasattr(self, 'prog_current'):
            display_text = self.prog_current if self.prog_current != "0" else "0"
            self.prog_display.insert(0, display_text)
            self.update_bit_display()
        else:
            self.prog_display.insert(0, "0")
    
    def update_bit_display(self):
        if hasattr(self, 'prog_current') and self.prog_current != "0":
            try:
                if self.base == "DEC":
                    value = int(self.prog_current)
                elif self.base == "HEX":
                    value = int(self.prog_current, 16)
                elif self.base == "OCT":
                    value = int(self.prog_current, 8)
                elif self.base == "BIN":
                    value = int(self.prog_current, 2)
                
                # Show 32-bit representation
                if value < 0:
                    bits = bin(value & 0xFFFFFFFF)[2:].zfill(32)
                else:
                    bits = bin(value)[2:].zfill(32)
                
                # Format with spaces for readability
                formatted_bits = ' '.join([bits[i:i+8] for i in range(0, 32, 8)])
                self.bit_display.config(text=f"32-bit: {formatted_bits}")
            except:
                self.bit_display.config(text="")
        else:
            self.bit_display.config(text="")
    
    def prog_add_digit(self, digit):
        if not hasattr(self, 'prog_current'):
            self.prog_current = "0"
            self.prog_previous = ""
            self.prog_operator = ""
            self.prog_result = 0
        
        current_base = self.base
        
        # Validate digit for current base
        if current_base == "BIN" and digit not in '01':
            return
        elif current_base == "OCT" and digit not in '01234567':
            return
        elif current_base == "DEC" and digit not in '0123456789':
            return
        elif current_base == "HEX" and digit not in '0123456789ABCDEF':
            return
        
        if self.prog_current == "0" and digit != '.':
            self.prog_current = digit
        else:
            self.prog_current += digit
        self.update_prog_display()
    
    def prog_set_operator(self, op):
        if not hasattr(self, 'prog_current'):
            self.prog_current = "0"
            self.prog_previous = ""
            self.prog_operator = ""
            self.prog_result = 0
        
        if self.prog_current == "":
            return
        if self.prog_previous != "":
            self.prog_calculate()
        self.prog_previous = self.prog_current
        self.prog_operator = op
        self.prog_current = ""
        self.update_prog_display()
    
    def prog_set_bitwise_operator(self, op):
        if not hasattr(self, 'prog_current'):
            self.prog_current = "0"
            self.prog_previous = ""
            self.prog_operator = ""
            self.prog_result = 0
        
        if self.prog_current == "":
            return
        if self.prog_previous != "":
            self.prog_calculate()
        self.prog_previous = self.prog_current
        self.prog_operator = op
        self.prog_current = ""
        self.update_prog_display()
    
    def prog_calculate(self):
        if not hasattr(self, 'prog_previous') or self.prog_previous == "" or self.prog_operator == "" or self.prog_current == "":
            return
        
        # Convert to decimal for calculation
        try:
            if self.base == "DEC":
                prev = int(self.prog_previous)
                curr = int(self.prog_current)
            elif self.base == "HEX":
                prev = int(self.prog_previous, 16)
                curr = int(self.prog_current, 16)
            elif self.base == "OCT":
                prev = int(self.prog_previous, 8)
                curr = int(self.prog_current, 8)
            elif self.base == "BIN":
                prev = int(self.prog_previous, 2)
                curr = int(self.prog_current, 2)
        except ValueError:
            messagebox.showerror("Error", "Invalid number for current base")
            self.prog_clear()
            return
        
        try:
            if self.prog_operator == '+':
                self.prog_result = prev + curr
            elif self.prog_operator == '-':
                self.prog_result = prev - curr
            elif self.prog_operator == '*':
                self.prog_result = prev * curr
            elif self.prog_operator == '/':
                if curr == 0:
                    raise ZeroDivisionError
                self.prog_result = prev // curr  # Integer division
            elif self.prog_operator == '%':
                if curr == 0:
                    raise ZeroDivisionError
                self.prog_result = prev % curr
            elif self.prog_operator == '&' or self.prog_operator == 'AND':
                self.prog_result = prev & curr
            elif self.prog_operator == '|':
                self.prog_result = prev | curr
            elif self.prog_operator == '^' or self.prog_operator == 'XOR':
                self.prog_result = prev ^ curr
            elif self.prog_operator == '<<':
                self.prog_result = prev << curr
            elif self.prog_operator == '>>':
                self.prog_result = prev >> curr
            elif self.prog_operator == '~':
                self.prog_result = ~prev
                self.prog_current = str(self.prog_result)
                self.prog_previous = ""
                self.prog_operator = ""
                self.update_prog_display()
                return
            
            # Convert result back to current base
            if self.base == "DEC":
                self.prog_current = str(self.prog_result)
            elif self.base == "HEX":
                self.prog_current = hex(self.prog_result & 0xFFFFFFFF)[2:].upper()
            elif self.base == "OCT":
                self.prog_current = oct(self.prog_result & 0xFFFFFFFF)[2:]
            elif self.base == "BIN":
                self.prog_current = bin(self.prog_result & 0xFFFFFFFF)[2:]
            
            self.prog_previous = ""
            self.prog_operator = ""
        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero!")
            self.prog_clear()
        except ValueError:
            messagebox.showerror("Error", "Invalid calculation")
            self.prog_clear()
        
        self.update_prog_display()
    
    def prog_clear(self):
        self.prog_current = "0"
        self.prog_previous = ""
        self.prog_operator = ""
        self.prog_result = 0
        self.update_prog_display()
    
    # Converter methods
    def update_units(self, event=None):
        cat = self.category_var.get()
        if cat == "Temperature":
            units = ["Celsius", "Fahrenheit", "Kelvin"]
        else:
            units = list(self.unit_factors[cat].keys())
        
        self.from_combo['values'] = units
        self.to_combo['values'] = units
        if units:
            self.from_var.set(units[0])
            self.to_var.set(units[1] if len(units) > 1 else units[0])
        self.convert_units()
    
    def on_value_change(self, event=None):
        self.convert_units()
    
    def on_unit_change(self, event=None):
        self.convert_units()
    
    def swap_units(self):
        from_unit = self.from_var.get()
        to_unit = self.to_var.get()
        self.from_var.set(to_unit)
        self.to_var.set(from_unit)
        value = self.value_entry.get()
        if value:
            try:
                result = float(self.result_label.cget("text"))
                self.value_entry.delete(0, tk.END)
                self.value_entry.insert(0, str(result))
            except ValueError:
                pass
        self.convert_units()
    
    def convert_units(self):
        input_val = self.value_entry.get().strip()
        if not input_val:
            self.result_label.config(text="")
            return
        try:
            value = float(input_val)
            cat = self.category_var.get()
            from_u = self.from_var.get()
            to_u = self.to_var.get()
            
            if cat == "Temperature":
                result = self.convert_temperature(from_u, to_u, value)
            else:
                factor_from = self.unit_factors[cat][from_u]
                factor_to = self.unit_factors[cat][to_u]
                result = value * (factor_from / factor_to)
            
            self.result_label.config(text=f"{result:.6g}")
        except ValueError:
            self.result_label.config(text="Error")
        except KeyError:
            self.result_label.config(text="Invalid unit")
    
    def convert_temperature(self, from_unit, to_unit, value):
        if from_unit == to_unit:
            return value
        if from_unit == "Celsius":
            if to_unit == "Fahrenheit":
                return value * 9 / 5 + 32
            elif to_unit == "Kelvin":
                return value + 273.15
        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                return (value - 32) * 5 / 9
            elif to_unit == "Kelvin":
                return (value - 32) * 5 / 9 + 273.15
        elif from_unit == "Kelvin":
            if to_unit == "Celsius":
                return value - 273.15
            elif to_unit == "Fahrenheit":
                return (value - 273.15) * 9 / 5 + 32
        return value
    
    # Graph methods
    def plot_function(self):
        try:
            expr = self.func_entry.get().strip()
            if not expr:
                raise ValueError("Enter a function")
            xmin = float(self.xmin_entry.get())
            xmax = float(self.xmax_entry.get())
            if xmin >= xmax:
                raise ValueError("X min must be less than X max")
            
            x = np.linspace(xmin, xmax, 400)
            safe_dict = {"__builtins__": {}, "x": x, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log, "exp": math.exp, "pi": math.pi}
            y = eval(expr, safe_dict)
            
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            fig = Figure(figsize=(4, 2.5))
            ax = fig.add_subplot(111)
            ax.plot(x, y, linewidth=1.5)
            ax.grid(True, alpha=0.3)
            ax.set_title(f"y = {expr}", fontsize=10)
            ax.set_xlabel("x", fontsize=8)
            ax.set_ylabel("y", fontsize=8)
            
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Plot Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()