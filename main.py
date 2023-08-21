from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from playsound import playsound
import multiprocessing
import sqlite3
import pygame

from define import *




def main():
    window = Tk()
    window.title(TITLE)
    window.geometry(GEOMETRY)
    window.resizable(width=FALSE, height=FALSE)
    pygame.init()
    pygame.mixer.init()


## ============================================ toplevelAdd 함수 ============================================ ##

    ## toplevelAdd 윈도우 창 함수 ##
    def toplevelAddFunc():
        toplevelAdd = Toplevel(window)
        toplevelAdd.geometry(ADD_GEOMETRY)
        toplevelAdd.resizable(width=FALSE, height=FALSE)

        # X버튼 클릭 시
        def exitWindowX():
            if toplevelPlay == None:
                toplevelAdd.destroy()
                return

            if toplevelPlay.get_num_channels() > 0:
                toplevelPlay.stop()
            toplevelAdd.destroy()

        ## ===== toplevelAdd 프로그램 ===== ##

        def addFileOpenfunc():
            filePath = filedialog.askopenfilename(filetypes=(("mp3", "*.mp3"), ("wav", "*.wav")))
            filePathList = filePath.split('/')
            fileName = filePathList[-1]
            strVarAddLabelFilePath.set(filePath)
            strVarAddLabelFileName.set(fileName)
            toplevelAdd.lift()
            if fileName != "":
                addButtonPlay.configure(state="normal")
                addButtonAdd.configure(state="normal")


        def addFileAddFunc():
            addFilePath = ""
            addFileName = ""
            addVolume = 0
            addMon = 1
            addTue = 1
            addWed = 1
            addThu = 1
            addFri = 1
            addHour = 0
            addMinute = 0
            
            addFilePath = strVarAddLabelFilePath.get()
            addFileName = strVarAddLabelFileName.get()

            addVolume = intVarAddScaleVolume.get()

            if not boolVarAddCheckboxMon.get():
                addMon = 0
            if not boolVarAddCheckboxTue.get():
                addTue = 0
            if not boolVarAddCheckboxWed.get():
                addWed = 0
            if not boolVarAddCheckboxThu.get():
                addThu = 0
            if not boolVarAddCheckboxFri.get():
                addFri = 0

            addHour = int(strVarAddComboboxHour.get())
            addMinute = int(strVarAddComboboxMinute.get())

            connect = sqlite3.connect("audiolist.db")
            cursor = connect.cursor()

            cursor.execute("INSERT INTO audiolisttable (path, name, vol, mon, tue, wed, thu, fri, hour, minute) Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (addFilePath, addFileName, addVolume, addMon, addTue, addWed, addThu, addFri, addHour, addMinute))

            connect.commit()
            connect.close()

            addButtonPlay.configure(state="disable")
            addButtonAdd.configure(state="disable")
            if toplevelPlay.get_num_channels() > 0:
                toplevelPlay.stop()
            toplevelAdd.destroy()


        def addPlayAudioFunc():
            global toplevelPlay
            addFilePath = strVarAddLabelFilePath.get()
            addVolumeSize = intVarAddScaleVolume.get() * 0.01

            toplevelPlay = pygame.mixer.Sound(addFilePath)
            toplevelPlay.set_volume(addVolumeSize)
            toplevelPlay.play()

            addButtonPlay.configure(text=BUTTON_STOP, command=addStopAudioFunc)


        def addStopAudioFunc():
            global toplevelPlay

            toplevelPlay.stop()
            addButtonPlay.configure(text=BUTTON_PLAY, command=addPlayAudioFunc)

        toplevelAdd.protocol('WM_DELETE_WINDOW', exitWindowX)


        def setVolumeFunc(addVolumeSizeStr):
            addVolumeSize = float(addVolumeSizeStr) / 100
            
            if toplevelPlay.get_num_channels() > 0:
                toplevelPlay.set_volume(addVolumeSize)


        ## ===== toplevelAdd 정의 ===== ##

        # 타입
        strVarAddLabelFilePath = StringVar()
        strVarAddLabelFilePath.set("")
        strVarAddLabelFileName = StringVar()
        strVarAddLabelFileName.set("")

        intVarAddScaleVolume = IntVar()
        intVarAddScaleVolume.set(50)

        boolVarAddCheckboxMon = BooleanVar()
        boolVarAddCheckboxMon.set(True)
        boolVarAddCheckboxTue = BooleanVar()
        boolVarAddCheckboxTue.set(True)
        boolVarAddCheckboxWed = BooleanVar()
        boolVarAddCheckboxWed.set(True)
        boolVarAddCheckboxThu = BooleanVar()
        boolVarAddCheckboxThu.set(True)
        boolVarAddCheckboxFri = BooleanVar()
        boolVarAddCheckboxFri.set(True)

        strVarAddComboboxHour = StringVar()
        strVarAddComboboxHour.set('0')
        strVarAddComboboxMinute = StringVar()
        strVarAddComboboxMinute.set('0')

        # 프레임
        addFrameFilePath = Frame(toplevelAdd)
        addFrameFileName = Frame(toplevelAdd)
        addFrameFileAdd = Frame(toplevelAdd)
        addFrameVolume = Frame(toplevelAdd)
        addFrameWeek = Frame(toplevelAdd)
        addFrameTime = Frame(toplevelAdd)
        addFrameAdd = Frame(toplevelAdd)
        
        #위젯
        addLabelFilePath = Label(addFrameFilePath, text=LABEL_FILE_PATH, width=9, anchor="e")
        addLabelFilePathString = Label(addFrameFilePath, textvariable=strVarAddLabelFilePath, wraplength=260)

        addLabelFileName = Label(addFrameFileName, text=LABEL_FILE_NAME, width=9, anchor="e")
        addLabelFileNameString = Label(addFrameFileName, textvariable=strVarAddLabelFileName, wraplength=260)

        addButtonOpenFile = Button(addFrameFileAdd, text=BUTTON_OPEN_FILE, command=addFileOpenfunc)

        addLabelVolume = Label(addFrameVolume, text=LABEL_VOLUME)
        addScaleVolume = Scale(addFrameVolume, from_=0, to=100, variable=intVarAddScaleVolume, command=setVolumeFunc)
        addButtonPlay = Button(addFrameVolume, text=BUTTON_PLAY, state="disable", command=addPlayAudioFunc)

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

        addButtonAdd = Button(addFrameAdd, text=BUTTON_ADD, state="disable", command=addFileAddFunc)


        ## ===== toplevelAdd 배치 ===== ##
        addFrameFilePath.pack(side=TOP)
        addFrameFileName.pack(side=TOP)
        addFrameFileAdd.pack(side=TOP)
        addFrameVolume.pack(side=TOP)
        addFrameWeek.pack(side=TOP)
        addFrameTime.pack(side=TOP)
        addFrameAdd.pack(side=TOP)

        addLabelFilePath.pack(side=LEFT)
        addLabelFilePathString.pack(side=LEFT)

        addLabelFileName.pack(side=LEFT)
        addLabelFileNameString.pack(side=LEFT)

        addButtonOpenFile.pack()

        addLabelVolume.pack(side=LEFT)
        addScaleVolume.pack(side=LEFT)
        addButtonPlay.pack(side=LEFT)

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

## ============================================ 프로그램 ============================================ ##

    # 데이터베이스에서 가져와 출력하는 기능 만들 것
    def loadRecordsFunc():
        number = 0
        weeks = ""
        connect = sqlite3.connect("audiolist.db")
        cursor = connect.cursor()
        
        cursor.execute('SELECT * from audiolisttable')
        for rows in cursor:
            number += 1
            weeks = ""
            if rows[4] == 1:
                weeks += "월, "
            if rows[5] == 1:
                weeks += "화, "
            if rows[6] == 1:
                weeks += "수, "
            if rows[7] == 1:
                weeks += "목, "
            if rows[8] == 1:
                weeks += "금, "
            
            tempFrame = Frame(frameRecords)
            tempFrame.pack(side=TOP)
            temp = Label(tempFrame, text=str(number), width=LABEL_RECORD_TITLE_WIDTH[0], anchor="center")
            temp.grid(row=0, column=0)
            temp = Label(tempFrame, text=rows[2], width=LABEL_RECORD_TITLE_WIDTH[1], anchor="center")
            temp.grid(row=0, column=1)
            temp = Label(tempFrame, text=rows[1], width=LABEL_RECORD_TITLE_WIDTH[2], anchor="center")
            temp.grid(row=0, column=2)
            temp = Label(tempFrame, text=str(rows[3]), width=LABEL_RECORD_TITLE_WIDTH[3], anchor="center")
            temp.grid(row=0, column=3)
            temp = Label(tempFrame, text=weeks, width=LABEL_RECORD_TITLE_WIDTH[4], anchor="center")
            temp.grid(row=0, column=4)
            temp = Label(tempFrame, text=str(rows[9]).zfill(2) + ":" + str(rows[10]).zfill(2), width=LABEL_RECORD_TITLE_WIDTH[5], anchor="center")
            temp.grid(row=0, column=5)
            temp = Button(tempFrame, text=LABEL_RECORD_TITLE[6], width=LABEL_RECORD_TITLE_WIDTH[6], command=lambda row=rows[0]: playSoundFunc(row))
            temp.grid(row=0, column=6)
            temp = Button(tempFrame, text=LABEL_RECORD_TITLE[7], width=LABEL_RECORD_TITLE_WIDTH[7], command=None)
            temp.grid(row=0, column=7)
            temp = Button(tempFrame, text=LABEL_RECORD_TITLE[8], width=LABEL_RECORD_TITLE_WIDTH[8], command=None)
            temp.grid(row=0, column=8)

        connect.close()

    여기서 노래 시작 정지 수정 삭제 기능 구현할 것
    def playSoundFunc(primaryKey):
        global play

        connect = sqlite3.connect("audiolist.db")
        cursor = connect.cursor()

        cursor.execute('SELECT * from audiolisttable where id=?', (primaryKey, ))
        get = cursor.fetchone()

        print(cursor.fetchall())

        connect.commit()
        connect.close()

        play = pygame.mixer.Sound(get[1])
        play.set_volume(float(get[3]) / 100)
        play.play()

## ============================================ 정의 ============================================ ##

    # 타입 정의


    # 프레임 정의
    frameButtons = Frame(window)
    frameRecordTitle = Frame(window)
    frameRecords = Frame(window)

    # frameButtons 프레임 위젯 정의
    buttonAdd = Button(frameButtons, text=BUTTON_ADD, command=toplevelAddFunc)
    buttonDelete = Button(frameButtons, text=BUTTON_DELETE, state="disable", command=None)
    buttonReload = Button(frameButtons, text=BUTTON_RELOAD, command=loadRecordsFunc)

    # frameRecordTitle 프레임 위젯 정의
    recordTitle = []
    separatorTitleCol = []
    separatorTitleRow = []
    for i in range(len(LABEL_RECORD_TITLE)):
        recordTitle.append(Label(frameRecordTitle, text=LABEL_RECORD_TITLE[i], width=LABEL_RECORD_TITLE_WIDTH[i], anchor="center"))
    for i in range(len(LABEL_RECORD_TITLE) - 1):
        separatorTitleCol.append(Separator(frameRecordTitle, orient="vertical"))
    for i in range(len(recordTitle) + len(separatorTitleCol)):
        separatorTitleRow.append(Separator(frameRecordTitle, orient="horizontal"))


    # frameRecords 프레임 위젯 정의

    


## ============================================ 배치 ============================================ ##

    # 프레임 배치
    frameButtons.pack(side=TOP)
    frameRecordTitle.pack(side=TOP)
    frameRecords.pack(side=TOP)

    # frameButtons 프레임 위젯 배치
    buttonAdd.pack(side=LEFT, padx=10, pady=5, ipadx=15, ipady=3)
    buttonDelete.pack(side=LEFT, padx=10, pady=5, ipadx=15, ipady=3)
    buttonReload.pack(side=LEFT, padx=10, pady=5, ipadx=15, ipady=3)

    # frameRecordTitle 프레임 위젯 배치
    for i in range(len(recordTitle)):
        recordTitle[i].grid(row=0, column=2 * i)
        if i >= len(separatorTitleCol):
            break
        separatorTitleCol[i].grid(row=0, column=2 * i + 1, sticky='ns')
        
    for i in range(len(separatorTitleRow)):
        separatorTitleRow[i].grid(row=1, column=i, sticky='ew')
    

    # frameButtons 프레임 위젯 배치
    
    window.mainloop()


## 전역 변수 ##
# pygame 오디오 재생 여부
toplevelPlay = None
play = None

# sql DB 및 테이블 생성, 존재 유무
connect = sqlite3.connect("audiolist.db")
cursor = connect.cursor()

cursor.execute('SELECT * from sqlite_master WHERE type="table" AND name="audiolisttable"')
row = cursor.fetchall()
if not row:
    connect.execute('CREATE TABLE audiolisttable(id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, name TEXT, vol INTEGER, mon INTEGER, tue INTEGER, wed INTEGER, thu INTEGER, fri INTEGER, hour INTEGER, minute INTEGER)') 

connect.commit()
connect.close()

if __name__=="__main__":
    main()