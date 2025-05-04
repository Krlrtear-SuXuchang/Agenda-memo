from tkinter import *
from tkinter import ttk, messagebox, scrolledtext
import os
import xml.etree.ElementTree as ET
import sql
from tkcalendar import Calendar

getinfo = sql.GetInfo()
insertinfo = sql.InsertInfo()
modifyinfo = sql.ModifyInfo()
accountinfo = sql.AccountInfo()

class Application:
    def __init__(self, master):
        self.certification = 'App_Agenda-1.0.0Beta_ASI-0.1-xml-RoHeaAct'

        self.data= ''
        # 新建待办
        self.title = StringVar()
        self.datetime_YMD = StringVar()
        self.datetime_HmS = StringVar()
        self.hour = StringVar()
        self.minute = StringVar()
        self.second = StringVar()
        self.insert_statement = IntVar()
        self.insert_statement.set(1)
        self.details_get_from_input = StringVar()

        self.root = master

        self.finish_show_button_switch = IntVar()
        self.todo_show_button_switch = IntVar()
        self.finish_show_button_switch.set(1)
        self.todo_show_button_switch.set(1)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x = (self.screen_width - 938) // 2
        self.y = (self.screen_height - 603) // 2
        self.root.geometry(f'{938}x{603}+{self.x}+{self.y}')
        # self.root.minsize(1400, 900)
        self.root.title('Agenda 1.0.0')
        self.frame = ttk.Frame(self.root)
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.blank = ttk.Frame(self.frame)

        # LabelFrame
        self.agenda_frame = ttk.LabelFrame(self.frame, text='待办事项')
        self.agenda_frame.place(x=6.7, y=6.7, width=562.8, height=301.5)
        self.description_frame = ttk.LabelFrame(self.frame, text='任务明细')
        self.description_frame.place(x=6.7, y=314.9, width=924.6, height=261.3)

        # 表格
        self.tree = ttk.Treeview(self.agenda_frame, show='headings', height=7, columns=('time', 'title', 'state'))
        self.tree.column('time', width=101, stretch=NO, anchor=W)
        self.tree.column('title', width=373, stretch=NO, anchor=W)
        self.tree.column('state', width=60, stretch=NO, anchor=CENTER)

        self.tree.heading('time', text='截止日期', anchor=CENTER)
        self.tree.heading('title', text='标题', anchor=CENTER)
        self.tree.heading('state', text='状态', anchor=CENTER)

        # 表格滚动条
        self.scrollbar = Scrollbar(self.agenda_frame, orient=VERTICAL, command=self.tree.yview)
        self.scrollbar.place(x=542.7, y=3.35, width=13.4, height=274)

        self.tree.place(x=6.7, y=6.7, width=536, height=267)
        self.tree.configure(yscrollcommand=self.scrollbar.set, selectmode='browse')
        self.style = ttk.Style()
        self.style.configure('Treeview', rowheight=20.1)
        self.getTree()
        self.tree.bind("<Double-1>", self.treeviewDoubleClick)

        # 详细信息
        self.details_info = scrolledtext.ScrolledText(self.description_frame, font=('微软雅黑', 13), wrap=WORD, state='disabled')
        self.details_info.place(x=6.7, y=6.7, width=911.2, height=224.45)

        self.control_frame = ttk.LabelFrame(self.root, text="操作面板")
        self.control_frame.place(x=576.2, y=6.7, width=355.1, height=234.5)

        self.insert_button = ttk.Button(self.control_frame, text='新建待办', command=self.createAgdItem)
        self.insert_button.place(x=13.4, y=13.4, width=100.5, height=33.5)
        self.modify_button = ttk.Button(self.control_frame, text='编辑条目', command=self.modifyAgdIrem)
        self.modify_button.place(x=127.3, y=13.4, width=100.5, height=33.5)
        self.delete_button = ttk.Button(self.control_frame, text='删除条目', command=self.deleteItem)
        self.delete_button.place(x=241.2, y=13.4, width=100.5, height=33.5)
        self.load_button = ttk.Button(self.control_frame, text='打开条目', command=self.loadItem)
        self.load_button.place(x=13.4, y=67, width=100.5, height=33.5)
        self.complete_button = ttk.Button(self.control_frame, text='标为完成', command=self.markAsComplete)
        self.complete_button.place(x=127.3, y=67, width=100.5, height=33.5)
        self.todo_button = ttk.Button(self.control_frame, text='标为待办', command=self.markAsIncomplete)
        self.todo_button.place(x=241.2, y=67, width=100.5, height=33.5)
        self.hide_button = ttk.Button(self.control_frame, text='隐藏明细', command=self.selectionClear)
        self.hide_button.place(x=13.4, y=120.6, width=100.5, height=33.5)
        self.share_button = ttk.Button(self.control_frame, text='分享')
        self.share_button.place(x=127.3, y=120.6, width=100.5, height=33.5)
        self.ASI_button = ttk.Button(self.control_frame, text='生成ASI', command=self.createASI)
        self.ASI_button.place(x=241.2, y=120.6, width=100.5, height=33.5)
        self.introduction_button = ttk.Button(self.control_frame, text='使用说明', command=self.introduction)
        self.introduction_button.place(x=13.4, y=174.2, width=100.5, height=33.5)


        self.show_frame = ttk.LabelFrame(self.root, text='显示设置')
        self.show_frame.place(x=576.2, y=247.9, width=355.1, height=60.3)

        self.finish_show_button = ttk.Checkbutton(self.show_frame, text='完成', cursor='hand2', onvalue=1, offvalue=0, variable=self.finish_show_button_switch)
        self.finish_show_button.place(x=13.4, y=0, width=67, height=33.5)
        self.todo_show_button = ttk.Checkbutton(self.show_frame, text='待办', cursor='hand2', onvalue=1, offvalue=0, variable=self.todo_show_button_switch)
        self.todo_show_button.place(x=93.8, y=0, width=67, height=33.5)
        self.fresh_button = ttk.Button(self.show_frame, text='刷新表格', command=self.getTree)
        self.fresh_button.place(x=241.2, y=-2, width=100.5, height=33.5)



    def insertDetails(self, details):
        self.details_info['state'] = 'normal'
        self.details_info.delete('1.0', "end")
        pre = ('截止时间: ', '完成状态: ', '标题: ', '内容: ')
        values = [e for e in details]
        if values[3] == 0:
            values[3] = "完成"
        elif values[3] == 1:
            values[3] = "待办"
        temp = values[1]
        values[1] = values[3]
        values[3] = temp
        temp = values[2]
        values[2] = values[3]
        values[3] = temp
        for i in range(4):
            self.details_info.insert("end", pre[i] + str(values[i]))
            self.details_info.insert("end", '\n')
            # self.details_info.see("end")
        self.details_info['state'] = 'disable'

    def crossSearch(self, datetime, title):
        for row in self.data:
            currentTime = row[0]
            # print(currentTime)
            if datetime == currentTime.strftime("%m-%d %H:%M") and title == row[1]:
                print('yes')
                return row
        return ('error', 'Not Found', 'Not Found', 'Not Found')

    def treeviewDoubleClick(self, event):
        try:
            selectedItems = self.tree.selection()[0]
            datetime = self.tree.item(selectedItems)['values'][0]
            title = str(self.tree.item(selectedItems)['values'][1])
            details = self.crossSearch(datetime, title)
            # print(details)
            self.insertDetails(details)
        except IndexError:
            print("Nothing selected")

    def selectionCheck(self):
        try:
            selectedItems = self.tree.selection()[0]
            datetime = self.tree.item(selectedItems)['values'][0]
            title = str(self.tree.item(selectedItems)['values'][1])
            details = self.crossSearch(datetime, title)
            return details
        except IndexError:
            print("Nothing selected")

    def selectionClear(self):
        self.details_info['state'] = 'normal'
        self.tree.selection()
        self.details_info.delete('1.0', "end")
        self.details_info['state'] = 'disable'

    def getTree(self):
        self.tree.delete(*self.tree.get_children())
        self.data = getinfo.getTable(sql.username)
        count = len(self.data)
        for i in range(count):
            currentTime = self.data[i][0]
            rightStruct = currentTime.strftime("%m-%d %H:%M")
            temp_data = list(self.data[i])
            temp_data[0] = rightStruct
            if temp_data[3] == 0 and self.finish_show_button_switch.get() == 1:
                temp_data[3] = "完成"
                temp_data.pop(2)
                self.tree.insert('', "end", values=temp_data)
            elif temp_data[3] == 1 and self.todo_show_button_switch.get() == 1:
                temp_data[3] = "待办"
                temp_data.pop(2)
                self.tree.insert('', "end", values=temp_data)

    def createAgdItem(self) -> None:
        def datetime_picker():
            def time_check():
                try:
                    hour = int(self.hour.get())
                    minute = int(self.minute.get())
                    second = int(self.second.get())
                    if (hour < 24 and hour >= 0) and (minute < 60 and minute >= 0) and (second < 60 and second >= 0):
                        self.datetime_HmS.set(f'{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}')
                        win.destroy()
                    else:
                        pass
                except ValueError:
                    pass

            win = Toplevel(classobj)
            win.geometry(f'335x335+{(self.screen_width - 335) // 2}+{(self.screen_height - 335) // 2}')

            calendar = Calendar(win)
            calendar.place(x=0, y=0, width=335, height=268)
            hourEnter = ttk.Entry(win, textvariable=self.hour)
            hourEnter.place(x=13.4, y=284.75, width=53.6, height=33.5)
            minuteEnter = ttk.Entry(win, textvariable=self.minute)
            minuteEnter.place(x=100.5, y=284.75, width=53.6, height=33.5)
            secondEnter = ttk.Entry(win, textvariable=self.second)
            secondEnter.place(x=187.6, y=284.75, width=53.6, height=33.5)
            ttk.Label(win, text='时').place(x=73.7, y=284.75, height=33.5)
            ttk.Label(win, text='分').place(x=160.8, y=284.75, height=33.5)
            ttk.Label(win, text='秒').place(x=247.9, y=284.75, height=33.5)
            confirm_button = ttk.Button(win, text='确定', command=time_check)
            confirm_button.place(x=274.7, y=284.75, width=53.6, height=33.5)

            def get_selected_date(event):
                date = calendar.selection_get()
                self.datetime_YMD.set(date)


            calendar.bind("<<CalendarSelected>>", get_selected_date)

        def close_handler():
            self.root.attributes('-disabled', 0)
            classobj.destroy()
            self.title.set('')
            self.datetime_YMD.set('YYYY-MM-DD')
            self.datetime_HmS.set('HH-mm-SS')
            self.hour.set('')
            self.minute.set('')
            self.second.set('')
            self.insert_statement.set(1)
            self.details_get_from_input = ''

        def commit_item():
            self.details_get_from_input = input_area.get(1.0,'end')

            datetime_rst = self.datetime_YMD.get() + ' ' + self.datetime_HmS.get()
            title = self.title.get()
            state = self.insert_statement.get()
            details = self.details_get_from_input

            if self.datetime_YMD.get() == 'YYYY-MM-DD' or self.datetime_HmS == 'HH-mm-SS':
                messagebox.showinfo('截止时间', '请选择有效时间')
            elif self.title == '':
                messagebox.showinfo('标题', '标题不能为空')
            else:
                pack = (datetime_rst, title, details, state)
                insert = insertinfo.insertTable(sql.username, pack)
                if insert is True:
                    messagebox.showinfo('提交', '提交成功')
                    close_handler()
                    self.getTree()
                elif insert == (False, 'Primary key already exists'):
                    messagebox.showinfo('提交', '该时间已被占用')
                elif insert == (False, "Data too long for column 'title'"):
                    messagebox.showinfo('提交', '标题过长')



        self.root.attributes('-disabled', 1)

        classobj = Toplevel(self.root)
        classobj.protocol("WM_DELETE_WINDOW", close_handler)
        title = StringVar()
        self.datetime_YMD.set('YYYY-MM-DD')
        self.datetime_HmS.set('HH:mm:SS')


        classobj.title('创建待办')

        screen_width = classobj.winfo_screenwidth()
        screen_height = classobj.winfo_screenheight()
        x = (screen_width - 670) // 2
        y = (screen_height - 402) // 2
        classobj.geometry(f'{670}x{402}+{x}+{y}')
        classobj.resizable(False, False)


        title_label = ttk.Label(classobj, text='标题')
        title_label.place(x=13.4, y=6.7, width=67, height=33.5)
        title_entry = ttk.Entry(classobj, textvariable=self.title)
        title_entry.place(x=87.1, y=6.7, width=167.5, height=30.15)

        state_choice_1 = ttk.Checkbutton(classobj, text='待办', onvalue=1, offvalue=0, variable=self.insert_statement)
        state_choice_1.place(x=301.5, y=6.7, width=67, height=30.15)
        state_choice_2 = ttk.Checkbutton(classobj, text='完成', onvalue=0, offvalue=1, variable=self.insert_statement)
        state_choice_2.place(x=402, y=6.7, width=67, height=30.15)

        commit_button = ttk.Button(classobj, text="提 交", command=commit_item)
        commit_button.place(x=536, y=46.9, width=100.5, height=33.5)

        datetime_label = ttk.Label(classobj, text='截止时间')
        datetime_label.place(x=13.4, y=46.9, width=67, height=33.5)
        datetime_label_YMD = ttk.Label(classobj, textvariable=self.datetime_YMD)
        datetime_label_YMD.place(x=87.1, y=46.9, width=167.5, height=33.5)
        datetime_label_HmS = ttk.Label(classobj, textvariable=self.datetime_HmS)
        datetime_label_HmS.place(x=201, y=46.9, width=167.5, height=33.5)
        selectDate = ttk.Button(classobj, text='选择时间', command=datetime_picker) # here command
        selectDate.place(x=301.5, y=46.9, width=100.5, height=33.5)

        details_label = ttk.LabelFrame(classobj, text='待办明细')
        details_label.place(x=8.71, y=80.4, width=651.24, height=308.2)

        input_area = scrolledtext.ScrolledText(details_label, wrap=WORD, font=('微软雅黑', 12))
        input_area.place(x=6.7, y=6.7, width=637.84, height=268)

    def modifyAgdIrem(self) -> None:
        selectedItem = self.selectionCheck()
        if selectedItem:
            def datetime_picker():
                def time_check():
                    try:
                        hour = int(self.hour.get())
                        minute = int(self.minute.get())
                        second = int(self.second.get())
                        if (hour < 24 and hour >= 0) and (minute < 60 and minute >= 0) and (second < 60 and second >= 0):
                            self.datetime_HmS.set(f'{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}')
                            win.destroy()
                        else:
                            pass
                    except ValueError:
                        pass

                win = Toplevel(classobj)
                win.geometry(f'335x335+{(self.screen_width - 335) // 2}+{(self.screen_height - 335) // 2}')

                calendar = Calendar(win)
                calendar.place(x=0, y=0, width=335, height=268)
                hourEnter = ttk.Entry(win, textvariable=self.hour)
                hourEnter.place(x=13.4, y=284.75, width=53.6, height=33.5)
                minuteEnter = ttk.Entry(win, textvariable=self.minute)
                minuteEnter.place(x=100.5, y=284.75, width=53.6, height=33.5)
                secondEnter = ttk.Entry(win, textvariable=self.second)
                secondEnter.place(x=187.6, y=284.75, width=53.6, height=33.5)
                ttk.Label(win, text='时').place(x=73.7, y=284.75, height=33.5)
                ttk.Label(win, text='分').place(x=160.8, y=284.75, height=33.5)
                ttk.Label(win, text='秒').place(x=247.9, y=284.75, height=33.5)
                confirm_button = ttk.Button(win, text='确定', command=time_check)
                confirm_button.place(x=274.7, y=284.75, width=53.6, height=33.5)

                def get_selected_date(event):
                    date = calendar.selection_get()
                    self.datetime_YMD.set(date)


                calendar.bind("<<CalendarSelected>>", get_selected_date)

            def close_handler():
                self.root.attributes('-disabled', 0)
                classobj.destroy()
                self.title.set('')
                self.datetime_YMD.set('YYYY-MM-DD')
                self.datetime_HmS.set('HH-mm-SS')
                self.hour.set('')
                self.minute.set('')
                self.second.set('')
                self.insert_statement.set(1)
                self.details_get_from_input = ''
                self.getTree()

            def modify_item():
                self.details_get_from_input = input_area.get(1.0,'end')

                datetime_rst = self.datetime_YMD.get() + ' ' + self.datetime_HmS.get()
                title = self.title.get()
                state = self.insert_statement.get()
                details = self.details_get_from_input

                if self.datetime_YMD.get() == 'YYYY-MM-DD' or self.datetime_HmS == 'HH-mm-SS':
                    messagebox.showinfo('截止时间', '请选择有效时间')
                elif self.title == '':
                    messagebox.showinfo('标题', '标题不能为空')
                else:
                    pack = (datetime_rst, title, details, state)
                    modify = modifyinfo.ModifyTable(sql.username, pack, orintime)
                    if modify is True:
                        messagebox.showinfo('编辑', '修改成功')
                        close_handler()
                    elif modify == (False, 'Primary key already exists'):
                        messagebox.showinfo('提交', '该时间已被占用')
                    elif modify == (False, "Data too long for column 'title'"):
                        messagebox.showinfo('提交', '标题过长')

            self.title.set(selectedItem[1])
            details = selectedItem[2]
            orintime = selectedItem[0]
            self.insert_statement.set(int(selectedItem[3]))
            self.datetime_YMD.set(str(selectedItem[0])[0:10])
            self.datetime_HmS.set(str(selectedItem[0])[11:])

            self.root.attributes('-disabled', 1)

            classobj = Toplevel(self.root)
            classobj.protocol("WM_DELETE_WINDOW", close_handler)

            classobj.title('编辑条目')

            screen_width = classobj.winfo_screenwidth()
            screen_height = classobj.winfo_screenheight()
            x = (screen_width - 670) // 2
            y = (screen_height - 402) // 2
            classobj.geometry(f'{670}x{402}+{x}+{y}')
            classobj.resizable(False, False)

            title_label = ttk.Label(classobj, text='标题')
            title_label.place(x=13.4, y=6.7, width=67, height=33.5)
            title_entry = ttk.Entry(classobj, textvariable=self.title)
            title_entry.place(x=87.1, y=6.7, width=167.5, height=30.15)

            state_choice_1 = ttk.Checkbutton(classobj, text='待办', onvalue=1, offvalue=0, variable=self.insert_statement)
            state_choice_1.place(x=301.5, y=6.7, width=67, height=30.15)
            state_choice_2 = ttk.Checkbutton(classobj, text='完成', onvalue=0, offvalue=1, variable=self.insert_statement)
            state_choice_2.place(x=402, y=6.7, width=67, height=30.15)

            commit_button = ttk.Button(classobj, text="提交修改", command=modify_item)
            commit_button.place(x=536, y=46.9, width=100.5, height=33.5)

            datetime_label = ttk.Label(classobj, text='截止时间')
            datetime_label.place(x=13.4, y=46.9, width=67, height=33.5)
            datetime_label_YMD = ttk.Label(classobj, textvariable=self.datetime_YMD)
            datetime_label_YMD.place(x=87.1, y=46.9, width=167.5, height=33.5)
            datetime_label_HmS = ttk.Label(classobj, textvariable=self.datetime_HmS)
            datetime_label_HmS.place(x=201, y=46.9, width=167.5, height=33.5)
            selectDate = ttk.Button(classobj, text='选择新时间', command=datetime_picker)  # here command
            selectDate.place(x=301.5, y=46.9, width=100.5, height=33.5)

            details_label = ttk.LabelFrame(classobj, text='待办明细')
            details_label.place(x=8.71, y=80.4, width=651.24, height=308.2)

            input_area = scrolledtext.ScrolledText(details_label, wrap=WORD, font=('微软雅黑', 12))
            input_area.place(x=6.7, y=6.7, width=637.84, height=268)
            input_area.insert("end", details)
        else:
            messagebox.showinfo('编辑', '请单击选择待修改的条目')

    def markAsComplete(self) -> None:
        selectedItem = self.selectionCheck()
        if selectedItem:
            MAC = modifyinfo.markAsComplete(sql.username, selectedItem[0])
            if MAC is True:
                messagebox.showinfo('标记', '修改状态为 完成')
                self.getTree()
            else:
                messagebox.showinfo('标记', '修改失败')
                self.getTree()
        else:
            messagebox.showinfo('标记', '请单击选择待标记的条目')

    def markAsIncomplete(self) -> None:
        selectedItem = self.selectionCheck()
        if selectedItem:
            MAC = modifyinfo.markAsIncomplete(sql.username, selectedItem[0])
            if MAC is True:
                messagebox.showinfo('标记', '修改状态为 待办')
                self.getTree()
            else:
                messagebox.showinfo('标记', '修改失败')
                self.getTree()
        else:
            messagebox.showinfo('标记', '请单击选择待标记的条目')

    def loadItem(self) -> None:
        try:
            selectedItems = self.tree.selection()[0]
            datetime = self.tree.item(selectedItems)['values'][0]
            title = str(self.tree.item(selectedItems)['values'][1])
            details = self.crossSearch(datetime, title)
            # print(details)
            self.insertDetails(details)
        except IndexError:
            print("Nothing selected")
            messagebox.showinfo('加载', '请单击选择待加载的条目')

    def deleteItem(self) -> None:
        selectedItem = self.selectionCheck()
        if selectedItem:
            delete = modifyinfo.deleteItem(sql.username, selectedItem[0])
            if delete is True:
                messagebox.showinfo('删除', '删除成功')
                self.getTree()
            else:
                messagebox.showinfo('删除', '删除失败')
        else:
            messagebox.showinfo('删除', '请单击选择待删除的条目')

    def createASI(self) -> None:
        def createXML():
            root = ET.Element('license')

            child1_headinfo = ET.SubElement(root, 'headinfo')

            child2_account = ET.SubElement(child1_headinfo, 'account')

            child3_username = ET.SubElement(child2_account, 'username')
            child3_password = ET.SubElement(child2_account, 'password')
            child3_username.text = sql.username
            child3_password.text = accountinfo.getASIKey(sql.username)

            tree = ET.ElementTree(root)
            tree.write('license.xml')
            messagebox.showinfo('ASI', 'xml文件已生成在同目录下')

        isExist = os.path.exists('license.xml')
        if not isExist:
            createXML()
        else:
            def close_handler():
                self.root.attributes('-disabled', 0)
                confirmWin.destroy()

            def comfirm_handler():
                createXML()
                close_handler()

            self.root.attributes('-disabled', 1)
            confirmWin = Toplevel(self.root)
            confirmWin.protocol("WM_DELETE_WINDOW", close_handler)
            confirmWin.title("确认")
            x = (self.screen_width - 335) // 2
            y = (self.screen_height - 201) // 2
            confirmWin.geometry(f'335x201+{x}+{y}')

            ttk.Label(confirmWin, text="发现同目录下有 license.xml\n是否覆盖该文件？", font=("微软雅黑", 13)).place(anchor=CENTER, x=167.5, y=67)
            cancel_button = ttk.Button(confirmWin, text="取 消", command=close_handler)
            cancel_button.place(x=20.1, y=134, width=120.6, height=33.5)
            confirm_button = ttk.Button(confirmWin, text="确 认", command=comfirm_handler)
            confirm_button.place(x=194.3, y=134, width=120.6, height=33.5)
            cancel_button.focus()

    def introduction(self):
        introText = ('Agenda', '版本: 1.0.0beta', '内部标识: 00731f3edf6d5ce5', '作者: Krlrtear', '项目地址: https://github.com/Krlrtear-SuXuchang/Agenda-memo', '基于Python 3.12', '欢迎交流学习', '-------------------------', '>>>界面说明',
                     '1.待办事项: 展示待办事项的缩略信息，双击可查看', '2.任务明细: 当前待办的详细信息，内容修改后请重新打开条目以刷新信息', '3.操作面板: 包含对待办条目的所有操作', '4.显示设置: 筛选显示内容，更改后请刷新表格', '-------------------------',
                     '>>>操作说明', '1.1 双击待办事项界面条目可展开该条目详细信息',
                     '2.1 新建待办: 输入标题、详细信息，选择事项状态，选择事件（时间格式错误无法录入），点击提交即可',
                     '2.2 编辑条目: 单击选中待修改的条目，操作与新建待办类似（若该条目已打开，须重新打开以更新显示内容）',
                     '2.3 删除条目: 单击选中待删除的条目，点击即可删除（无确认，请谨慎操作）',
                     '2.4 打开条目: 单击选中待打开的条目，点击即可打开，与双击效果相同',
                     '2.5 标为完成: 单击选中待标记的条目，点击即可标记为完成（若该条目已打开，须重新打开以更新显示内容）',
                     '2.6 标为待办: 与2.5相似',
                     '2.7 隐藏明细: 清空任务细明显示内容（不会修改数据）',
                     '2.8 分享: 敬请期待',
                     "2.9 生成ASI: 在程序同目录下生成一'license.xml'文件，该文件包含登录信息（密码已混淆），将该文件置于程序同目录下，登录界面可点击ASI快速登录。若创建时存在相同名称文件，则询问是否覆盖",
                     '3.1 勾选“完成”“待办”筛选条目（更改后请点击刷新表格）',
                     '-------------------------', '感谢使用 Agenda')
        self.details_info['state'] = 'normal'
        self.details_info.delete('1.0', "end")
        for row in introText:
            self.details_info.insert("end", row + '\n')
        self.details_info['state'] = 'disable'






if __name__ == '__main__':
    root = Tk()
    app = Application(root)

    root.mainloop()
