from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox as mb
from sql import SignUp, SignIn, Tool
import sql
import xml.etree.ElementTree as ET
import os
import main

signin = SignIn()
signup = SignUp()
tool = Tool()

class SignWindow:
    def __init__(self, master):
        self.username = StringVar()
        self.password = StringVar()
        self.username_reg = StringVar()
        self.password_reg = StringVar()

        self.root = master
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x = (self.screen_width - 300) // 2
        self.y = (self.screen_height - 200) // 2
        self.root.geometry(f'{300}x{200}+{self.x}+{self.y}')
        self.root.title('Agenda 1.0.0')
        self.root.resizable(False, False)


        self.login_frame = Frame(self.root)
        self.register_frame = Frame(self.root)
        self.register_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.login_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.register_frame.place_forget()
        self.loginWindow()
        self.registerWindow()


    def registerCheck(self):
        if self.username_reg.get() == '' or self.password_reg.get() == '':
            mb.showinfo('提示', '用户名和密码不能为空')
        else:
            if signup.IsExistUser(self.username_reg.get()):
                mb.showinfo('注册', '用户已存在')
            else:
                if signup.register(self.username_reg.get(), self.password_reg.get()):
                    signup.init(self.username_reg.get())
                    mb.showinfo('注册', f'注册成功\n用户名: {self.username_reg.get()}\n密码: {self.password_reg.get()}\n请务必牢记！')
                    self.username_reg.set('')
                    self.password_reg.set('')
                    self.switchToLoginWindow()
                else:
                    mb.showinfo('注册', '注册失败')

    def switchToLoginWindow(self):
        self.register_frame.place_forget()
        self.login_frame.place(x=0, y=0, relwidth=1, relheight=1)

    def registerWindow(self):
        ttk.Label(self.register_frame, text='注册 Agenda 账号', font=("微软雅黑", 11)).place(relx=0.5, y=20, anchor='n')
        ttk.Button(self.register_frame, text='注 册', width=10, cursor="hand2", command=self.registerCheck).place(x=230, y=155, anchor='n', height=25)
        ttk.Button(self.register_frame, text='返 回', width=10, cursor="hand2", command=self.switchToLoginWindow).place(x=70, y=155, anchor='n', height=25)
        ttk.Label(self.register_frame, text='用户名', font=("微软雅黑", 8)).place(x=100, y=50, anchor='n', height=25)
        ttk.Label(self.register_frame, text='密码', font=("微软雅黑", 8)).place(x=94, y=95, anchor='n', height=25)
        ttk.Entry(self.register_frame, textvariable=self.username_reg, cursor="xterm").place(relx=0.5, y=70, anchor='n', width="110p", height="25")
        ttk.Entry(self.register_frame, textvariable=self.password_reg, show='*', cursor="xterm").place(relx=0.5, y=115, anchor='n', width="110p", height="25")

    def loginCheck(self) -> None:
        if self.username.get() == '' or self.password.get() == '':
            mb.showinfo('提示', '用户名和密码不能为空')
        else:
            if signin.IsExistUser(self.username.get()):
                if signin.login(self.username.get(), self.password.get()):
                    mb.showinfo('登录', f'登录成功\n欢迎 {self.username.get()}')
                    self.register_frame.destroy()
                    self.login_frame.destroy()
                    sql.username = self.username.get()
                    App = main.Application(self.root)
                    print(App.certification)
                else:
                    mb.showinfo('登录', '密码错误')
            else:
                mb.showinfo('登录', '该用户不存在')

    def switchToRegisterWindow(self):
        self.login_frame.place_forget()
        self.register_frame.place(x=0, y=0, relwidth=1, relheight=1)

    def loginWindow(self):
        ttk.Label(self.login_frame, text='使用 Agenda 账号登录', font=("微软雅黑", 11)).place(relx=0.5, y=20, anchor='n')
        ttk.Button(self.login_frame, text='登 录', width=10, cursor="hand2", command=self.loginCheck).place(x=230, y=155, anchor='n', height=25)
        ttk.Button(self.login_frame, text='注 册', width=10, cursor="hand2", command=self.switchToRegisterWindow).place(x=70, y=155, anchor='n', height=25)
        ttk.Label(self.login_frame, text='用户名', font=("微软雅黑", 8)).place(x=100, y=50, anchor='n', height=25)
        ttk.Label(self.login_frame, text='密码', font=("微软雅黑", 8)).place(x=94, y=95, anchor='n', height=25)
        ttk.Entry(self.login_frame, textvariable=self.username, cursor="xterm").place(relx=0.5, y=70, anchor='n', width="110p", height="25")
        ttk.Entry(self.login_frame, textvariable=self.password, show='*', cursor="xterm").place(relx=0.5, y=115, anchor='n', width="110p", height="25")
        ttk.Button(self.login_frame, text='ASI', command=self.ASI).place(x=275 , y=10, anchor='n', width="25p", height=25)


    def ASI(self):
        if os.path.exists('license.xml'):
            tree = ET.parse('license.xml')
            root = tree.getroot()
            username_xml = root[0][0][0].text
            key_xml = root[0][0][1].text
            # print(username_xml, password_xml)
            if tool.IsKey(username_xml, key_xml):
                mb.showinfo('ASI', f'登录成功\n欢迎 {self.username.get()}')
                self.register_frame.destroy()
                self.login_frame.destroy()
                sql.username = username_xml
                App = main.Application(self.root)
                print(App.certification)
            else:
                mb.showinfo('ASI', '验证失败')

        else:
            print("'license.xml' was not found.")



if __name__ == '__main__':
    try:
        tk = Tk()
        SignWindow(tk)
        tk.mainloop()
    except Exception as e:
        time = datetime.now()
        strtime = time.strftime("%Y%m%d-%H%M%S")
        with open(f'{strtime}.txt', 'w') as f:
            f.write(f'{strtime}\n\n-------------------\n\n')
            f.write(str(e))
    finally:
        sql.connect.close()
