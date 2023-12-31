import datetime
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
import sqlite3
import pygame
import os
import os.path
import winshell

from define import *




def main():
    window = Tk()
    window.title(TITLE + " " + VERSION)
    window.geometry(GEOMETRY)
    window.resizable(width=FALSE, height=FALSE)
    path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    if os.path.isfile(path):
        window.iconbitmap(path)
    pygame.init()
    pygame.mixer.init()

    # X버튼 클릭 시
    def exitWindowX():
        exitProgram()

    window.protocol('WM_DELETE_WINDOW', exitWindowX)


## ============================================ toplevelAdd 함수 ============================================ ##

    ## toplevelAdd 윈도우 창 함수 ##
    def toplevelAddFunc():
        toplevelAdd = Toplevel(window)
        toplevelAdd.title(TOPLEVER_ADD_TITLE)
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

        toplevelAdd.protocol('WM_DELETE_WINDOW', exitWindowX)

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
            addSecond = 0
            
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
            addSecond = int(strVarAddComboboxSecond.get())

            path = os.path.join(os.path.dirname(__file__), 'audiolist.db')
            connect = sqlite3.connect(path)
            cursor = connect.cursor()

            cursor.execute("INSERT INTO audiolisttable (path, name, vol, mon, tue, wed, thu, fri, hour, minute, second) Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (addFilePath, addFileName, addVolume, addMon, addTue, addWed, addThu, addFri, addHour, addMinute, addSecond))

            connect.commit()
            cursor.close()
            connect.close()

            addButtonPlay.configure(state="disable")
            addButtonAdd.configure(state="disable")
            if toplevelPlay == None:
                toplevelAdd.destroy()
                reloadRecordFunc()
                return
            if toplevelPlay.get_num_channels() > 0:
                toplevelPlay.stop()
            toplevelAdd.destroy()
            reloadRecordFunc()


        def addPlayAudioFunc():
            global toplevelPlay
            addFilePath = strVarAddLabelFilePath.get()
            addVolumeSize = intVarAddScaleVolume.get() * 0.01

            if not os.path.isfile(addFilePath):
                messagebox.showwarning("경고!", "해당 경로에 파일이 없습니다.")
                toplevelAdd.lift()
                return

            toplevelPlay = pygame.mixer.Sound(addFilePath)
            toplevelPlay.set_volume(addVolumeSize)
            toplevelPlay.play()

            addButtonPlay.configure(text=BUTTON_STOP, command=addStopAudioFunc)


        def addStopAudioFunc():
            global toplevelPlay

            toplevelPlay.stop()
            addButtonPlay.configure(text=BUTTON_PLAY, command=addPlayAudioFunc)


        def setVolumeFunc(addVolumeSizeStr):
            addVolumeSize = float(addVolumeSizeStr) / 100
            
            if toplevelPlay == None:
                return
            if toplevelPlay.get_num_channels() > 0:
                toplevelPlay.set_volume(addVolumeSize)

        def addSetNowTimeFunc():
            addGetTime = str(datetime.datetime.now())
            addTimeList = addGetTime.split(" ")
            addTimeList = addTimeList[1].split(".")
            addTimeList = addTimeList[0].split(":")

            strVarAddComboboxHour.set(addTimeList[0])
            strVarAddComboboxMinute.set(addTimeList[1])
            strVarAddComboboxSecond.set(addTimeList[2])


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
        strVarAddComboboxHour.set(12)
        strVarAddComboboxMinute = StringVar()
        strVarAddComboboxMinute.set(00)
        strVarAddComboboxSecond = StringVar()
        strVarAddComboboxSecond.set(00)

        # 프레임
        addFrameFilePath = Frame(toplevelAdd)
        addFrameFileName = Frame(toplevelAdd)
        addFrameFileAdd = Frame(toplevelAdd)
        addFrameVolume = Frame(toplevelAdd)
        addFrameWeek = Frame(toplevelAdd)
        addFrameTime = Frame(toplevelAdd)
        addFrameSetNowTime = Frame(toplevelAdd)
        addFrameAdd = Frame(toplevelAdd)
        
        #위젯
        addLabelFilePath = Label(addFrameFilePath, text=LABEL_FILE_PATH, width=FILE_NAME_TITLE_WIDTH, anchor="e")
        addLabelFilePathString = Label(addFrameFilePath, textvariable=strVarAddLabelFilePath, wraplength=FILE_NAME_WRAPLENGTH)

        addLabelFileName = Label(addFrameFileName, text=LABEL_FILE_NAME, width=FILE_NAME_TITLE_WIDTH, anchor="e")
        addLabelFileNameString = Label(addFrameFileName, textvariable=strVarAddLabelFileName, wraplength=FILE_NAME_WRAPLENGTH)

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
        addComboboxSecond = Combobox(addFrameTime, width=COMBOBOX_WIDTH, textvariable=strVarAddComboboxSecond, values=COMBOBOX_SECOND)
        addLabelSecond = Label(addFrameTime, text=LABEL_SECOND)

        addSetNowTime = Button(addFrameSetNowTime, text=BUTTON_NOW_TIME, command=addSetNowTimeFunc)

        addButtonAdd = Button(addFrameAdd, text=BUTTON_ADD, state="disable", command=addFileAddFunc)


        ## ===== toplevelAdd 배치 ===== ##
        addFrameFilePath.pack(side=TOP, pady=(5, 0))
        addFrameFileName.pack(side=TOP, pady=3)
        addFrameFileAdd.pack(side=TOP, pady=(0, 10))
        addFrameVolume.pack(side=TOP, pady=10)
        addFrameWeek.pack(side=TOP, pady=10)
        addFrameTime.pack(side=TOP, pady=10)
        addFrameSetNowTime.pack(side=TOP)
        addFrameAdd.pack(side=BOTTOM, pady=(0, 20))

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
        addComboboxSecond.pack(side=LEFT)
        addLabelSecond.pack(side=LEFT)

        addSetNowTime.pack()

        addButtonAdd.pack()










## ============================================ toplevelModify 함수 ============================================ ##

    ## toplevelModify 윈도우 창 함수 ##
    def toplevelModifyFunc(primaryKey):
        toplevelModify = Toplevel(window)
        toplevelModify.title(TOPLEVER_MODIFY_TITLE)
        toplevelModify.geometry(MODIFY_GEOMETRY)
        toplevelModify.resizable(width=FALSE, height=FALSE)

        path = os.path.join(os.path.dirname(__file__), 'audiolist.db')
        connect = sqlite3.connect(path)
        cursor = connect.cursor()

        cursor.execute('SELECT * from audiolisttable where id=?', (primaryKey, ))
        get = cursor.fetchone()

        cursor.close()
        connect.close()

        # X버튼 클릭 시
        def exitWindowX():
            if toplevelPlay == None:
                toplevelModify.destroy()
                return

            if toplevelPlay.get_num_channels() > 0:
                toplevelPlay.stop()
            toplevelModify.destroy()

        toplevelModify.protocol('WM_DELETE_WINDOW', exitWindowX)


        ## ===== toplevelModify 프로그램 ===== ##

        def setVolumeFunc(modifyVolumeSizeStr):
            modifyVolumeSize = float(modifyVolumeSizeStr) / 100
            
            if toplevelPlay == None:
                return
            if toplevelPlay.get_num_channels() > 0:
                toplevelPlay.set_volume(modifyVolumeSize)


        def modifyPlayAudioFunc():
            global toplevelPlay
            modifyFilePath = get[1]
            modifyVolumeSize = float(intVarModifyScaleVolume.get()) * 0.01

            if not os.path.isfile(modifyFilePath):
                messagebox.showwarning("경고!", "해당 경로에 파일이 없습니다.")
                toplevelModify.lift()
                return

            toplevelPlay = pygame.mixer.Sound(modifyFilePath)
            toplevelPlay.set_volume(modifyVolumeSize)
            toplevelPlay.play()

            modifyButtonPlay.configure(text=BUTTON_STOP, command=modifyStopAudioFunc)


        def modifyStopAudioFunc():
            global toplevelPlay

            toplevelPlay.stop()
            modifyButtonPlay.configure(text=BUTTON_PLAY, command=modifyPlayAudioFunc)

        def modifyFileModifyFunc():
            modifyVolume = 0
            modifyMon = 1
            modifyTue = 1
            modifyWed = 1
            modifyThu = 1
            modifyFri = 1
            modifyHour = 0
            modifyMinute = 0
            modifySecond = 0

            modifyVolume = intVarModifyScaleVolume.get()

            if not boolVarModifyCheckboxMon.get():
                modifyMon = 0
            if not boolVarModifyCheckboxTue.get():
                modifyTue = 0
            if not boolVarModifyCheckboxWed.get():
                modifyWed = 0
            if not boolVarModifyCheckboxThu.get():
                modifyThu = 0
            if not boolVarModifyCheckboxFri.get():
                modifyFri = 0

            modifyHour = int(strVarModifyComboboxHour.get())
            modifyMinute = int(strVarModifyComboboxMinute.get())
            modifySecond = int(strVarModifyComboboxSecond.get())

            path = os.path.join(os.path.dirname(__file__), 'audiolist.db')
            connect = sqlite3.connect(path)
            cursor = connect.cursor()

            cursor.execute("UPDATE 'audiolisttable' SET vol = ? WHERE id = ?", (modifyVolume, primaryKey))
            cursor.execute("UPDATE 'audiolisttable' SET mon = ? WHERE id = ?", (modifyMon, primaryKey))
            cursor.execute("UPDATE 'audiolisttable' SET tue = ? WHERE id = ?", (modifyTue, primaryKey))
            cursor.execute("UPDATE 'audiolisttable' SET wed = ? WHERE id = ?", (modifyWed, primaryKey))
            cursor.execute("UPDATE 'audiolisttable' SET thu = ? WHERE id = ?", (modifyThu, primaryKey))
            cursor.execute("UPDATE 'audiolisttable' SET fri = ? WHERE id = ?", (modifyFri, primaryKey))
            cursor.execute("UPDATE 'audiolisttable' SET hour = ? WHERE id = ?", (modifyHour, primaryKey))
            cursor.execute("UPDATE 'audiolisttable' SET minute = ? WHERE id = ?", (modifyMinute, primaryKey))
            cursor.execute("UPDATE 'audiolisttable' SET second = ? WHERE id = ?", (modifySecond, primaryKey))

            connect.commit()
            cursor.close()
            connect.close()

            if toplevelPlay == None:
                toplevelModify.destroy()
                reloadRecordFunc()
                return
            if toplevelPlay.get_num_channels() > 0:
                toplevelPlay.stop()
            toplevelModify.destroy()
            reloadRecordFunc()

        def modifySetNowTimeFunc():
            modifyGetTime = str(datetime.datetime.now())
            modifyTimeList = modifyGetTime.split(" ")
            modifyTimeList = modifyTimeList[1].split(".")
            modifyTimeList = modifyTimeList[0].split(":")

            strVarModifyComboboxHour.set(modifyTimeList[0])
            strVarModifyComboboxMinute.set(modifyTimeList[1])
            strVarModifyComboboxSecond.set(modifyTimeList[2])


        ## ===== toplevelModify 정의 ===== ##
        
        # 타입
        intVarModifyScaleVolume = IntVar()
        intVarModifyScaleVolume.set(get[3])

        boolVarModifyCheckboxMon = BooleanVar()
        boolVarModifyCheckboxMon.set(True if get[4] == 1 else False)
        boolVarModifyCheckboxTue = BooleanVar()
        boolVarModifyCheckboxTue.set(True if get[5] == 1 else False)
        boolVarModifyCheckboxWed = BooleanVar()
        boolVarModifyCheckboxWed.set(True if get[6] == 1 else False)
        boolVarModifyCheckboxThu = BooleanVar()
        boolVarModifyCheckboxThu.set(True if get[7] == 1 else False)
        boolVarModifyCheckboxFri = BooleanVar()
        boolVarModifyCheckboxFri.set(True if get[8] == 1 else False)

        strVarModifyComboboxHour = StringVar()
        strVarModifyComboboxHour.set(str(get[9]))
        strVarModifyComboboxMinute = StringVar()
        strVarModifyComboboxMinute.set(str(get[10]))
        strVarModifyComboboxSecond = StringVar()
        strVarModifyComboboxSecond.set(str(get[11]))

        # 프레임
        modifyFrameFileName = Frame(toplevelModify)
        modifyFrameVolume = Frame(toplevelModify)
        modifyFrameWeek = Frame(toplevelModify)
        modifyFrameTime = Frame(toplevelModify)
        modifyFrameModify = Frame(toplevelModify)
        modifyFrameSetNowTime = Frame(toplevelModify)

        # modifyFrameFileName
        modifyLabelFileNameText = Label(modifyFrameFileName, text=LABEL_FILE_NAME, width=FILE_NAME_TITLE_WIDTH, anchor="e")
        modifyLabelFileName = Label(modifyFrameFileName, text=get[2], wraplength=FILE_NAME_WRAPLENGTH)

        # modifyFrameVolume
        modifyLabelVolume = Label(modifyFrameVolume, text=LABEL_VOLUME)
        modifyScaleVolume = Scale(modifyFrameVolume, from_=0, to=100, variable=intVarModifyScaleVolume, command=setVolumeFunc)
        modifyButtonPlay = Button(modifyFrameVolume, text=BUTTON_PLAY, command=modifyPlayAudioFunc)

        # modifyFrameWeek
        modifyLabelWeek = Label(modifyFrameWeek, text=LABEL_WEEK)
        modifyCheckbuttonMon = Checkbutton(modifyFrameWeek, text=CHECKBUTTON_MON, variable=boolVarModifyCheckboxMon)
        modifyCheckbuttonTue = Checkbutton(modifyFrameWeek, text=CHECKBUTTON_TUE, variable=boolVarModifyCheckboxTue)
        modifyCheckbuttonWed = Checkbutton(modifyFrameWeek, text=CHECKBUTTON_WED, variable=boolVarModifyCheckboxWed)
        modifyCheckbuttonThu = Checkbutton(modifyFrameWeek, text=CHECKBUTTON_THU, variable=boolVarModifyCheckboxThu)
        modifyCheckbuttonFri = Checkbutton(modifyFrameWeek, text=CHECKBUTTON_FRI, variable=boolVarModifyCheckboxFri)

        # modifyFrameTime
        modifyLabelTime = Label(modifyFrameTime, text=LABEL_TIME)
        modifyComboboxHour = Combobox(modifyFrameTime, width=COMBOBOX_WIDTH, textvariable=strVarModifyComboboxHour, values=COMBOBOX_HOUR)
        modifyLabelHour = Label(modifyFrameTime, text=LABEL_HOUR)
        modifyComboboxMinute = Combobox(modifyFrameTime, width=COMBOBOX_WIDTH, textvariable=strVarModifyComboboxMinute, values=COMBOBOX_MINUTE)
        modifyLabelMinute = Label(modifyFrameTime, text=LABEL_MINUTE)
        modifyComboboxSecond = Combobox(modifyFrameTime, width=COMBOBOX_WIDTH, textvariable=strVarModifyComboboxSecond, values=COMBOBOX_SECOND)
        modifyLabelSecond = Label(modifyFrameTime, text=LABEL_SECOND)

        modifySetNowTime = Button(modifyFrameSetNowTime, text=BUTTON_NOW_TIME, command=modifySetNowTimeFunc)

        modifyButtonModify = Button(modifyFrameModify, text=BUTTON_MODIFY, command=modifyFileModifyFunc)


        ## ===== toplevelModify 배치 ===== ##

        # 프레임
        modifyFrameFileName.pack(side=TOP, pady=5)
        modifyFrameVolume.pack(side=TOP, pady=5)
        modifyFrameWeek.pack(side=TOP, pady=5)
        modifyFrameTime.pack(side=TOP, pady=5)
        modifyFrameSetNowTime.pack(side=TOP)
        modifyFrameModify.pack(side=BOTTOM, pady=(0, 20))

        # modifyFrameFileName
        modifyLabelFileNameText.pack(side=LEFT)
        modifyLabelFileName.pack(side=LEFT)

        # modifyFrameVolume
        modifyLabelVolume.pack(side=LEFT)
        modifyScaleVolume.pack(side=LEFT)
        modifyButtonPlay.pack(side=LEFT)

        # modifyFrameWeek
        modifyLabelWeek.pack(side=LEFT)
        modifyCheckbuttonMon.pack(side=LEFT)
        modifyCheckbuttonTue.pack(side=LEFT)
        modifyCheckbuttonWed.pack(side=LEFT)
        modifyCheckbuttonThu.pack(side=LEFT)
        modifyCheckbuttonFri.pack(side=LEFT)

        # modifyFrameTime
        modifyLabelTime.pack(side=LEFT)
        modifyComboboxHour.pack(side=LEFT)
        modifyLabelHour.pack(side=LEFT)
        modifyComboboxMinute.pack(side=LEFT)
        modifyLabelMinute.pack(side=LEFT)
        modifyComboboxSecond.pack(side=LEFT)
        modifyLabelSecond.pack(side=LEFT)

        modifySetNowTime.pack()

        modifyButtonModify.pack()








## ============================================ 프로그램 ============================================ ##

    def exitProgram():
        exitProgramAnswer = messagebox.askokcancel("안내", "종료 하시겠습니까?")
        if exitProgramAnswer:
            window.quit()
            window.destroy()

    def menuHelpInfoFunc():
        messagebox.showinfo("정보", f"""
버전: {VERSION}
OS: Windows
Dev Tools: Python, SQLite
제작: 조대영
                                    """)

    def loadRecordsFunc():
        global recordList
        number = 0
        weeks = ""

        path = os.path.join(os.path.dirname(__file__), 'audiolist.db')
        connect = sqlite3.connect(path)
        cursor = connect.cursor()
        
        if sortMode == 0:
            cursor.execute('SELECT * from audiolisttable')
        elif sortMode == 1:
            cursor.execute('SELECT * from audiolisttable ORDER BY hour, minute, second')
        elif sortMode == 2:
            cursor.execute('SELECT * from audiolisttable ORDER BY name, id')


        for rows in cursor:
            number += 1
            weeks = ""
            rowClone = []

            rowClone = list(rows)

            rowClone.append(number - 1)

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
            tempFrame.pack(side=TOP, pady=3)
            temp = Label(tempFrame, text=str(number), width=LABEL_RECORD_TITLE_WIDTH[0], anchor="center")
            temp.grid(row=0, column=0)
            temp = Label(tempFrame, text=rows[2], width=LABEL_RECORD_TITLE_WIDTH[1], anchor="center", wraplength=LABEL_RECORD_FILE_NAME_WRAPLENGTH)
            temp.grid(row=0, column=1)
            temp = Label(tempFrame, text=rows[1], width=LABEL_RECORD_TITLE_WIDTH[2], anchor="center", wraplength=LABEL_RECORD_FILE_PATH_WRAPLENGTH)
            temp.grid(row=0, column=2)
            temp = Label(tempFrame, text=str(rows[3]), width=LABEL_RECORD_TITLE_WIDTH[3], anchor="center")
            temp.grid(row=0, column=3)
            temp = Label(tempFrame, text=weeks, width=LABEL_RECORD_TITLE_WIDTH[4], anchor="center")
            temp.grid(row=0, column=4)
            temp = Label(tempFrame, text=str(rows[9]).zfill(2) + ":" + str(rows[10]).zfill(2) + ":" + str(rows[11]).zfill(2), width=LABEL_RECORD_TITLE_WIDTH[5], anchor="center")
            temp.grid(row=0, column=5)
            temp = Button(tempFrame, text=LABEL_RECORD_TITLE[6], width=LABEL_RECORD_TITLE_WIDTH[6] - 1, command=lambda row=rows[0], number=number - 1: playSoundFunc(row, number))
            rowClone.append(temp)
            temp.grid(row=0, column=6)
            temp = Button(tempFrame, text=LABEL_RECORD_TITLE[7], width=LABEL_RECORD_TITLE_WIDTH[7] - 1, command=lambda row=rows[0]: toplevelModifyFunc(row))
            rowClone.append(temp)
            temp.grid(row=0, column=7, padx=1)
            temp = Button(tempFrame, text=LABEL_RECORD_TITLE[8], width=LABEL_RECORD_TITLE_WIDTH[8] - 1, command=lambda row=rows[0]: deleteRecordFunc(row))
            rowClone.append(temp)
            temp.grid(row=0, column=8)

            recordList.append(rowClone)

        cursor.close()
        connect.close()

    
    def playSoundFunc(primaryKey, number):
        global play
        global nowPlaying
        global recordList

        if nowPlaying != []:
            for i in nowPlaying:
                stopSoundFunc(i[0], i[1])

        path = os.path.join(os.path.dirname(__file__), 'audiolist.db')
        connect = sqlite3.connect(path)
        cursor = connect.cursor()

        cursor.execute('SELECT * from audiolisttable where id=?', (primaryKey, ))
        get = cursor.fetchone()

        cursor.close()
        connect.close()

        if not os.path.isfile(get[1]):
            messagebox.showwarning("경고!", "해당 경로에 파일이 없습니다.")
            return

        play = pygame.mixer.Sound(get[1])
        play.set_volume(float(get[3]) / 100)
        play.play()
        nowPlaying.append([primaryKey, number])

        recordList[number][13].configure(text=BUTTON_STOP)
        recordList[number][13].configure(command=lambda: stopSoundFunc(primaryKey, number))


    def stopSoundFunc(primaryKey, number):
        global play
        global nowPlaying
        global recordList

        play.stop()

        recordList[number][13].configure(text=BUTTON_PLAY)
        recordList[number][13].configure(command=lambda: playSoundFunc(primaryKey, number))
        
        nowPlaying.remove([primaryKey, number])

    def initialization():
        global play
        global nowPlaying
        global recordList

        play = None
        nowPlaying = []
        recordList = []
        
        
        if play == None:
            pass
        elif play.get_num_channels() > 0:
            play.stop()
        
        frameRecordsList = frameRecords.pack_slaves()
        for i in frameRecordsList:
            recordWidgetList = i.grid_slaves()
            for y in recordWidgetList:
                y.destroy()
            i.destroy()

    def stopAllSound():
        if toplevelPlay == None:
            pass
        elif toplevelPlay.get_num_channels() > 0:
            toplevelPlay.stop()

        if play == None:
            pass
        elif play.get_num_channels() > 0:
            play.stop()

    def reloadRecordFunc():
        stopAllSound()
        initialization()
        loadRecordsFunc()

    def deleteRecordFunc(primaryKey):
        deleteAnswer = messagebox.showwarning("경고!", "정말 삭제하시겠습니까?")

        if deleteAnswer:
            path = os.path.join(os.path.dirname(__file__), 'audiolist.db')
            connect = sqlite3.connect(path)
            cursor = connect.cursor()

            cursor.execute('DELETE FROM "audiolisttable" WHERE id=?', (primaryKey, ))

            connect.commit()
            cursor.close()
            connect.close()

            reloadRecordFunc()


    def initializationDatabase():
        initializationAnswer = messagebox.askokcancel("경고!", "정말 '초기화'하시겠습니까?")
        if initializationAnswer:
            initializationReanswer = messagebox.askokcancel("경고!", "되돌릴 수 없습니다. 정말 '초기화'하시겠습니까?")
            if initializationReanswer:
                path = os.path.join(os.path.dirname(__file__), 'audiolist.db')
                connect = sqlite3.connect(path)
                cursor = connect.cursor()

                cursor.execute('DROP TABLE "audiolisttable"')

                connect.commit()
                cursor.close()
                connect.close()

                messagebox.showinfo("안내", "초기화 되었습니다. 프로그램을 재시작 해주세요.")

                window.quit()
                window.destroy()

    def timeCheckAutoStartFunc():
        global saveHour
        global saveMinute
        global saveSecond
        global saveWeek

        nowHour = 0
        nowMinute = 0
        nowSecond = 0

        timeList = ""

        getTime = str(datetime.datetime.now())
        timeList = getTime.split(" ")
        timeList = timeList[1].split(".")
        timeList = timeList[0].split(":")

        getWeek = datetime.datetime.today().weekday()

        nowHour = timeList[0]
        nowMinute = timeList[1]
        nowSecond = timeList[2]

        if not (saveHour == nowHour and saveMinute == nowMinute and saveSecond == nowSecond and saveWeek == getWeek):
            saveHour = nowHour
            saveMinute = nowMinute
            saveSecond = nowSecond
            saveWeek = getWeek

            path = os.path.join(os.path.dirname(__file__), 'audiolist.db')
            connect = sqlite3.connect(path)
            cursor = connect.cursor()

            cursor.execute('SELECT * FROM "audiolisttable" where hour=? AND minute=? AND second=?', (timeList[0], timeList[1], timeList[2]))
            get = cursor.fetchone()

            cursor.close()
            connect.close()
            
            if get != None:
                for i in recordList:
                    if (i[0] == get[0]) and (get[getWeek + 4] == 1):
                        playSoundFunc(get[0], i[12])

        window.after(400, timeCheckAutoStartFunc)

    def buttonSortFunc():
        global sortMode

        if sortMode == 0:
            sortTime()

        elif sortMode == 1:
            sortName()

        elif sortMode == 2:
            sortID()

    def sortID():
        global sortMode

        sortMode = 0
        bindFile = open("bind.txt", "r")
        binds = bindFile.readlines()
        bindFile.close()
        for i in range(len(binds)):
            oneBindSplit = binds[i].split(" ")
            if oneBindSplit[0] == "sort_mode":
                binds[i] = "sort_mode 0\n"
        bindFile = open("bind.txt", "w")
        for oneBind in binds:
            bindFile.write(oneBind)
        bindFile.close()
        buttonSort.configure(text=SORT_MODE[0])

        intVarMenuSort.set(0)

        reloadRecordFunc()

    def sortTime():
        global sortMode

        sortMode = 1
        bindFile = open("bind.txt", "r")
        binds = bindFile.readlines()
        bindFile.close()
        for i in range(len(binds)):
            oneBindSplit = binds[i].split(" ")
            if oneBindSplit[0] == "sort_mode":
                binds[i] = "sort_mode 1\n"
        bindFile = open("bind.txt", "w")
        for oneBind in binds:
            bindFile.write(oneBind)
        bindFile.close()
        buttonSort.configure(text=SORT_MODE[1])

        intVarMenuSort.set(1)

        reloadRecordFunc()

    def sortName():
        global sortMode

        sortMode = 2
        bindFile = open("bind.txt", "r")
        binds = bindFile.readlines()
        bindFile.close()
        for i in range(len(binds)):
            oneBindSplit = binds[i].split(" ")
            if oneBindSplit[0] == "sort_mode":
                binds[i] = "sort_mode 2\n"
        bindFile = open("bind.txt", "w")
        for oneBind in binds:
            bindFile.write(oneBind)
        bindFile.close()
        buttonSort.configure(text=SORT_MODE[2])

        intVarMenuSort.set(2)

        reloadRecordFunc()

    def startProgramAddFunc():
        startupFolder = winshell.startup()
        thisEXEPath = os.path.join(os.path.dirname(__file__), 'AUtoDio.exe')
        shortcutPath = os.path.join(startupFolder, "AUtoDio.lnk")
        if boolVarMenuSettingStartProg.get():
            if os.path.exists(thisEXEPath) and (not os.path.exists(shortcutPath)):
                winshell.CreateShortcut(
                    Path=shortcutPath,
                    Target=thisEXEPath,
                    Icon=(thisEXEPath, 0),
                    Description="AUtoDio shortcut"
                )
        else:
            if os.path.exists(shortcutPath):
                os.remove(shortcutPath)

        bindFile = open("bind.txt", "r")
        binds = bindFile.readlines()
        bindFile.close()
        for i in range(len(binds)):
            oneBindSplit = binds[i].split(" ")
            if oneBindSplit[0] == "set_start":
                binds[i] = "set_start " + str(int(boolVarMenuSettingStartProg.get()))
        bindFile = open("bind.txt", "w")
        for oneBind in binds:
            bindFile.write(oneBind)
        bindFile.close()





## ============================================ 정의 ============================================ ##

    # 타입 정의
    intVarMenuSort = IntVar()
    intVarMenuSort.set(sortMode)
    boolVarMenuSettingStartProg = BooleanVar()
    boolVarMenuSettingStartProg.set(startProgram)

    # 메뉴 바 정의
    menubar = Menu(window)
    menuFile = Menu(menubar, tearoff=0)
    menuSort = Menu(menubar, tearoff=0)
    menuSetting = Menu(menubar, tearoff=0)
    menuProblem = Menu(menubar, tearoff=0)
    menuHelp = Menu(menubar, tearoff=0)

    # 프레임 정의
    frameRecordTitle = Frame(window)
    frameRecords = Frame(window)
    frameButtons = Frame(window)

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
        # loadRecordsFunc()가 관여


    # frameButtons 프레임 위젯 정의
    buttonAdd = Button(frameButtons, text=BUTTON_ADD, command=toplevelAddFunc)
    buttonReload = Button(frameButtons, text=BUTTON_RELOAD, command=reloadRecordFunc)
    buttonSort = Button(frameButtons, text=SORT_MODE[sortMode], command=buttonSortFunc)
    buttonExit = Button(frameButtons, text=BUTTON_EXIT, command=exitProgram)




## ============================================ 배치 ============================================ ##

    # 메뉴바 배치
    menuFile.add_command(label=MENU_FILE_ADD, command=toplevelAddFunc)
    menuFile.add_separator()
    menuFile.add_command(label=MENU_FILE_EXIT, command=exitProgram)
    menubar.add_cascade(label=MENU_FILE, menu=menuFile)

    menuSort.add_radiobutton(label=SORT_MODE[0], variable=intVarMenuSort, value=0, command=sortID)
    menuSort.add_radiobutton(label=SORT_MODE[1], variable=intVarMenuSort, value=1, command=sortTime)
    menuSort.add_radiobutton(label=SORT_MODE[2], variable=intVarMenuSort, value=2, command=sortName)
    menubar.add_cascade(label=MENU_SORT, menu=menuSort)

    menuSetting.add_checkbutton(label=MENU_SETTING_STARTPROG, variable=boolVarMenuSettingStartProg, command=startProgramAddFunc)
    menubar.add_cascade(label=MENU_SETTING, menu=menuSetting)

    menuProblem.add_command(label=MENU_PROBLEM_REROAD, command=reloadRecordFunc)
    menuProblem.add_command(label=MENU_PROBLEM_INITIALIZATION, command=initializationDatabase)
    menubar.add_cascade(label=MENU_PROBLEM, menu=menuProblem)

    menuHelp.add_command(label=MENU_HELP_INFO, command=menuHelpInfoFunc)
    menubar.add_cascade(label=MENU_HELP, menu=menuHelp)

    # 프레임 배치
    frameRecordTitle.pack(side=TOP, pady=(20, 0))
    frameRecords.pack(side=TOP)
    frameButtons.pack(side=BOTTOM, pady=(0, 20))

    # frameRecordTitle 프레임 위젯 배치
    for i in range(len(recordTitle)):
        recordTitle[i].grid(row=0, column=2 * i)
        if i >= len(separatorTitleCol):
            break
        separatorTitleCol[i].grid(row=0, column=2 * i + 1, sticky='ns')
        
    for i in range(len(separatorTitleRow)):
        separatorTitleRow[i].grid(row=1, column=i, sticky='ew')

    # frameButtons 프레임 위젯 배치
    buttonAdd.pack(side=LEFT, padx=10, pady=5, ipadx=15, ipady=3)
    buttonReload.pack(side=LEFT, padx=10, pady=5, ipadx=15, ipady=3)
    buttonSort.pack(side=LEFT, padx=10, pady=5, ipadx=15, ipady=3)
    buttonExit.pack(side=LEFT, padx=10, pady=5, ipadx=15, ipady=3)
    
    # 초기 실행 함수
    timeCheckAutoStartFunc()
    loadRecordsFunc()
    window.config(menu=menubar)
    window.mainloop()
    


## 전역 변수 ##
# pygame 오디오 재생 여부
toplevelPlay = None
play = None
recordList = []
nowPlaying = [] # [[primaryKey, number], [primaryKey, number], [primaryKey, number]]
saveHour = 0
saveMinute = 0
saveSecond = 0
saveWeek = 0

bindFile = None
bind = []
sortMode = 0 # 0: 등록 순  1: 시간 순
startProgram = False

path = os.path.join(os.path.dirname(__file__), 'bind.txt')
if not os.path.isfile(path):
    path = os.path.join(os.path.dirname(__file__), 'bind_initialization.txt')
    bindInitFile = open(path, "r")
    bindInit = bindInitFile.read()
    bindInitFile.close()

    path = os.path.join(os.path.dirname(__file__), 'bind.txt')
    bindFile = open(path, "w")
    bindFile.write(bindInit)
    bindFile.close()

path = os.path.join(os.path.dirname(__file__), 'bind.txt')
if os.path.isfile(path):
    bindFile = open(path, "r")
    bind = bindFile.readlines()
    bindFile.close()

for bindOneLine in bind:
    bindNameAndSet = bindOneLine.split(" ")
    if bindNameAndSet[0] == "sort_mode":
        sortMode = int(bindNameAndSet[1])
    if bindNameAndSet[0] == "set_start":
        startProgram = bool(int(bindNameAndSet[1]))


# sql DB 및 테이블 생성, 존재 유무
path = os.path.join(os.path.dirname(__file__), 'audiolist.db')
connect = sqlite3.connect(path)
cursor = connect.cursor()

cursor.execute('SELECT * from sqlite_master WHERE type="table" AND name="audiolisttable"')
row = cursor.fetchall()
if not row:
    connect.execute('CREATE TABLE audiolisttable(id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, name TEXT, vol INTEGER, mon INTEGER, tue INTEGER, wed INTEGER, thu INTEGER, fri INTEGER, hour INTEGER, minute INTEGER, second INTEGER)') 
    connect.commit()
    
cursor.close()
connect.close()

if __name__=="__main__":
    main()