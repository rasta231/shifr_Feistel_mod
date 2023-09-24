import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from main import CustomEncryptor


class Interface:
    def __init__(self):
        secret = '3f788083-77d3-4502-9d71-21319f1792b6'
        root = tk.Tk()
        root.geometry("500x500")
        root.title('laba1')
        self.states()
        self.flag = False
        self.flag_status = False
        self.widgets(self.state_dict)
        root.mainloop()

    def widgets(self, state_dict):
        self.label_var = tk.StringVar()
        self.label_var_1 = tk.StringVar()
        # Фрейм 1
        self.frame = ttk.Frame(borderwidth=1, relief='solid', padding=[8, 10])
        self.label = ttk.Label(self.frame, text="Введите текст")
        self.label.grid(sticky='n', padx=20, pady=10, row=1, column=1)
        self.entry = ttk.Entry(self.frame)
        self.entry.grid(sticky='nw', padx=20, row=2, column=1)
        self.label_key = ttk.Label(self.frame, text="Введите ключ")
        self.label_key.grid(sticky='n', padx=20, pady=10, row=3, column=1)
        self.entry_key = ttk.Entry(self.frame)
        self.entry_key.grid(sticky='nw', padx=20, row=4, column=1)
        self.button = ttk.Button(self.frame, text='ОК', command=self.getting)
        self.button.grid(sticky='nwse', padx=20, pady=20, row=5, column=1)
        ######
        self.label_2 = ttk.Label(self.frame, text='Ввод через файл')
        self.label_2.grid(sticky='n', padx=20, pady=10, row=1, column=2)
        self.but = ttk.Button(self.frame, text='Открыть файлы', command=self.OpenFile)
        self.but.grid(sticky='n', padx=20, pady=10, row=3, column=2)
        self.enabled_checkbutton = ttk.Checkbutton(self.frame, textvariable=state_dict['enabled'],
                                                   variable=state_dict['enabled'] if self.flag else None,
                                                   offvalue=state_dict['enabled_off'],
                                                   onvalue=state_dict['enabled_on'])
        self.enabled_checkbutton.grid(sticky='n', padx=20, pady=10, row=2, column=2)
        self.button_usage = ttk.Button(self.frame, text='Шифровать', command=self.encr)
        self.button_usage.grid(row=6, column=1, sticky='n', padx=20, pady=10, )
        self.button_usage1 = ttk.Button(self.frame, text='Де Шифровать', command=self.decrpt)
        self.button_usage1.grid(row=6, column=2, sticky='n', padx=20, pady=10, )
        self.frame.grid(sticky='nwse', row=1, column=1, padx=(20, 220), pady=10)
        # Фрейм 4

        self.frame_for_text = ttk.Frame(borderwidth=1, relief='solid', padding=[8, 10])

        self.label_plane_text = ttk.Label(self.frame_for_text, text="Исходный текст")
        self.label_plane_text.grid(row=1, column=1)

        self.label_plane_text_2 = ttk.Label(self.frame_for_text, textvariable=self.label_var_1)
        self.label_plane_text_2.grid(row=2, column=1)

        self.label_text_out_lb = ttk.Label(self.frame_for_text, text='Расшифрованый текст')
        self.label_text_out_lb.grid(row=2, column=3)

        self.label_text_out = ttk.Label(self.frame_for_text, textvariable=self.label_var)
        self.label_text_out.grid(row=2, column=2)

        self.frame_for_text.grid(row=2, column=1, sticky='w', pady=10, padx=80)

    def OpenFile(self):
        filepath = filedialog.askopenfilename(initialdir="C:\\Users\\RTX\\pc_sec")
        last = (filepath[-3:])
        if last == 'txt':
            try:
                with open(filepath, 'r') as file:
                    sp = [i.strip() for i in file.readlines()]
                print(sp)
                self.state_dict['enabled'].set("Считано")  # Обновляем значение переменной
                self.flag_status = True
            except:
                messagebox.showerror('Ошибка')
                self.state_dict['enabled'].set("Не считано")  # Обновляем значение переменной
        else:
            messagebox.showerror('Ошибка')
            self.state_dict['enabled'].set("Не считано")  # Обновляем значение переменной

    def states(self):
        self.state_dict = {
            'enabled_on': "Считано",
            'enabled_off': "Не считано",
            'enabled': tk.StringVar(value="Не считано"),
        }

    def getting(self):
        self.flag_status = False
        text = self.entry.get()
        key = self.entry_key.get()
        self.label_var_1.set(text)
        return text, key

    def show(self):
        key = 'hello'
        secret = '3f788083-77d3-4502-9d71-21319f1792b6'
        custom_encryptor = CustomEncryptor(key, secret)
        plaintext = self.getting()

        encrypted_text = custom_encryptor.encrypt_message(plaintext, 'cbc')
        print(encrypted_text)

        decrypted_text = custom_encryptor.decrypt_cipher(encrypted_text, 'cbc')
        print(decrypted_text)

    def encr(self):
        self.data = self.getting()
        if self.flag_status == True:
            print(1)
        else:
            try:

                self.custom_encryptor = CustomEncryptor(self.getting()[1], self.getting()[0])
                self.encrypted_text = self.custom_encryptor.encrypt_message(self.getting()[0], 'cbc')
                print(self.encrypted_text)
                self.label_var.set(self.encrypted_text)
            except:
                messagebox.showerror('Ошибка')

    def decrpt(self):
        self.data = self.getting()
        if self.flag_status == True:
            print(1)
        else:
            try:
                self.decrypt_text = self.custom_encryptor.decrypt_cipher(self.encrypted_text, 'cbc')
                print(self.decrypt_text)
            except:
                messagebox.showerror('Ошибка')


ex = Interface()
