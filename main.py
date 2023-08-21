from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import sqlite3

from define import *




def main():
    window = Tk()
    window.title(TITLE)
    window.geometry(GEOMETRY)
    window.resizable(width=FALSE, height=FALSE)

## ====================== 프로그램 ====================== ##

    # toplevelAdd 윈도우 창 함수
    def toplevelAddFunc():
        toplevelAdd = Toplevel(window)
        toplevelAdd.geometry(ADD_GEOMETRY)
        toplevelAdd.resizable(width=FALSE, height=FALSE)

        ## ===== toplevelAdd 프로그램 ===== ##
        def addFileOpenfunc():
            filePath = filedialog.askopenfilename()
            filePathList = filePath.split('/')
            fileName = filePathList[-1]
            strVarAddLabelFilePath.set(filePath)
            strVarAddLabelFileName.set(fileName)

        def addFileAddFunc():
            addFilePath = strVarAddLabelFilePath.get()
            addFileName = strVarAddLabelFileName.get()

            addMon = boolVarAddCheckboxMon.get()
            addTue = boolVarAddCheckboxTue.get()
            addWed = boolVarAddCheckboxWed.get()
            addThu = boolVarAddCheckboxThu.get()
            addFri = boolVarAddCheckboxFri.get()

            addHour = strVarAddComboboxHour.get()
            AddMinute = strVarAddComboboxMinute.get()


        ## ===== toplevelAdd 정의 ===== ##

        # 타입
        strVarAddLabelFilePath = StringVar()
        strVarAddLabelFileName = StringVar()

        boolVarAddCheckboxMon = BooleanVar()
        boolVarAddCheckboxMon.set(False)
        boolVarAddCheckboxTue = BooleanVar()
        boolVarAddCheckboxTue.set(False)
        boolVarAddCheckboxWed = BooleanVar()
        boolVarAddCheckboxWed.set(False)
        boolVarAddCheckboxThu = BooleanVar()
        boolVarAddCheckboxThu.set(False)
        boolVarAddCheckboxFri = BooleanVar()
        boolVarAddCheckboxFri.set(False)

        strVarAddComboboxHour = StringVar()
        strVarAddComboboxHour.set('0')
        strVarAddComboboxMinute = StringVar()
        strVarAddComboboxMinute.set('0')

        # 프레임
        addFrameFilePath = Frame(toplevelAdd)
        addFrameFileName = Frame(toplevelAdd)
        addFrameFileAdd = Frame(toplevelAdd)
        addFrameWeek = Frame(toplevelAdd)
        addFrameTime = Frame(toplevelAdd)
        addFrameAdd = Frame(toplevelAdd)
        
        #위젯
        addLabelFilePath = Label(addFrameFilePath, text=LABEL_FILE_PATH, width=9, anchor="e")
        addLabelFilePathString = Label(addFrameFilePath, textvariable=strVarAddLabelFilePath, wraplength=260)

        addLabelFileName = Label(addFrameFileName, text=LABEL_FILE_NAME, width=9, anchor="e")
        addLabelFileNameString = Label(addFrameFileName, textvariable=strVarAddLabelFileName, wraplength=260)

        addButtonOpenFile = Button(addFrameFileAdd, text=BUTTON_OPEN_FILE, command=addFileOpenfunc)

        addLabelWeek = Label(addFrameWeek, text=LABEL_WEEK)
        addCheckbuttonMon = Checkbutton(addFrameWeek, text=CHECKBUTTON_MON, variable=boolVarAddCheckboxMon)
        addCheckbuttonTue = Checkbutton(addFrameWeek, text=CHECKBUTTON_TUE, variable=boolVarAddCheckboxTue)
        addCheckbuttonWed = Checkbutton(addFrameWeek, text=CHECKBUTTON_WED, variable=boolVarAddCheckboxWed)
        addCheckbuttonThu = Checkbutton(addFrameWeek, text=CHECKBUTTON_THU, variable=boolVarAddCheckboxThu)
        addCheckbuttonFri = Checkbutton(addFrameWeek, text=CHECKBUTTON_FRI, variable=boolVarAddCheckboxFri)

        addLabelTime = Label(addFrameTime, text=LABEL_TIME)
        addComboboxHour = Combobox(addFrameTime, width=COMBOBOX_WIDTH, textvariable=strVarAddComboboxHour, values=COMBOBOX_HOUR)
        addLabelHour = Label(addFrameTime, text=LABEL_HOUR)
        addComboboxMinute = Combobox(addFrameTime, width=COMBOBOX_WIDTH, textvariable=strVarAddComboboxMinute, values=COMBOBOX_MINUTE)
        addLabelMinute = Label(addFrameTime, text=LABEL_MINUTE)

        addButtonAdd = Button(addFrameAdd, text=BUTTON_ADD, command=addFileAddFunc)


        ## ===== toplevelAdd 배치 ===== ##
        addFrameFilePath.pack(side=TOP)
        addFrameFileName.pack(side=TOP)
        addFrameFileAdd.pack(side=TOP)
        addFrameWeek.pack(side=TOP)
        addFrameTime.pack(side=TOP)
        addFrameAdd.pack(side=TOP)

        addLabelFilePath.pack(side=LEFT)
        addLabelFilePathString.pack(side=LEFT)

        addLabelFileName.pack(side=LEFT)
        addLabelFileNameString.pack(side=LEFT)

        addButtonOpenFile.pack()

        addLabelWeek.pack(side=LEFT)
        addCheckbuttonMon.pack(side=LEFT)
        addCheckbuttonTue.pack(side=LEFT)
        addCheckbuttonWed.pack(side=LEFT)
        addCheckbuttonThu.pack(side=LEFT)
        addCheckbuttonFri.pack(side=LEFT)

        addLabelTime.pack(side=LEFT)
        addComboboxHour.pack(side=LEFT)
        addLabelHour.pack(side=LEFT)
        addComboboxMinute.pack(side=LEFT)
        addLabelMinute.pack(side=LEFT)

        addButtonAdd.pack()

## ====================== 정의 ====================== ##

    # 프레임 정의
    frameButtons = Frame(window)

    # frameButtons 프레임 위젯 정의
    buttonAdd = Button(frameButtons, text=BUTTON_ADD, command=toplevelAddFunc)
    buttonDelete = Button(frameButtons, text=BUTTON_DELETE, state="disable", command=None)
    buttonReload = Button(frameButtons, text=BUTTON_RELOAD, command=None)



## ====================== 배치 ====================== ##

    # 프레임 배치
    frameButtons.pack(side=TOP)

    # frameButtons 프레임 위젯 배치
    buttonAdd.pack(side=LEFT, padx=10, pady=5, ipadx=15, ipady=3)
    buttonDelete.pack(side=LEFT, padx=10, pady=5, ipadx=15, ipady=3)
    buttonReload.pack(side=LEFT, padx=10, pady=5, ipadx=15, ipady=3)


    window.mainloop()


## 전역 변수 ##


# sql DB 및 테이블 생성, 존재 유무
connect = sqlite3.connect("audiolist.db")
cursor = connect.cursor()

cursor.execute('SELECT * from sqlite_master WHERE type="table" AND name="audiolisttable"')
row = cursor.fetchall()
if not row:
    connect.execute('CREATE TABLE audiolisttable(id INTEGER PRIMARY KEY, path TEXT, name TEXT, vol INTEGER, mon INTEGER, tue INTEGER, wed INTEGER, thu INTEGER, fri INTEGER, hour INTEGER, minute INTEGER)') 

#connect.commit()
connect.close()

if __name__=="__main__":
    main()