import re
import math
import tkinter as tk
from typing import List

class Calculator:
    """TESTE"""
    def __init__(self, root: tk.Tk, label: tk.Label, display: tk.Entry, buttons: List[List[tk.Button]]):
        #Construtor responsável pela criação da janela virtual
        self.root = root
        self.label = label
        self.display = display
        self.buttons = buttons

    def start(self):
        self._config_buttons()
        self._config_display()
        self.root.mainloop()

    def _config_buttons(self):
        buttons = self.buttons
        for row_value in buttons:
            for button in row_value: #Matrix responsável p/ digitar um numero
                button_text = button["text"]

                if button_text == "C":
                    button.bind("<Button-1>", self.clear)
                    button.config(bg="#EA4335", fg="#fff")

                if button_text == "0123456789.+-/*()":
                    button.bind("<Button-1>", self.add_text_to_display)

                if button_text == "=":
                    button.bind("<Button-1>", self.calculate)
                    button.config(bg="#4785F4", fg="#fff")

    def _config_display(self):
        #Gera o texto na "whiteboard"
        self.display.bind("<Return>", self.calculate)
        self.display.bind("<KP_Enter>", self.calculate)

    def _fix_text(self, text):
        #Substitui tudo o que nao for 0123456789./*-+^e
        text = re.sub(r"[^\d\.\/\*\-\+\(\)\^e]", r"", text, 0)
        #Substitui operadores repetidos para apenas um operando
        text = re.sub(r"([\.\/\*\-\+\^])\1+", r"\1", text, 0)
        #Substitui () ou *() para nada (NONE)
        text = re.sub(r"\*?\(\)", "", text)

    def clear(self, event=None):
        #Deleta a operação por completa
        self.display.delete(0, "end")

    def add_text_to_display(self, event=None):
        #Insere o texto na tela
        self.display.insert("end", event.widget["text"])

    def calculate(self, event=None):
        #Gera a equação
        fixed_text = self._fix_text(self.display.get())
        equations = self._get_equations(fixed_text)

        try:
            if len(equations) == 1:
                result = eval(self._fix_text(equations[0]))
            else:
                result = eval(self._fix_text(equations[0]))
                for equation in equations[1:]:
                    result = math.pow(result, eval(self._fix_text(equation)))

            self.display.delete(0, "end")
            self.display.insert("end", result)
            self.label.config(text=f"{fixed_text} = {result}")

        except OverflowError:
            self.label.config(text="Não consegui realizar a equação")
        except Exception as e:
            print(e)
            self.label.config(text="Conta Inválida")

    def _get_equations(self, text):
        #Parte a equação exponencial em 2 equações
        return re.split(r"\^", text, 0)
