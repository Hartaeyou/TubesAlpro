import streamlit as st
import time
import playsound as ps
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tubes2 import data
from savetimer import timersave

def menu():
    menu = ["Pomodoro", "Timer", "Histori Belajar"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Pomodoro":
        st.title("Pomodoro Timer")
        st.write("Break Time = 5 Minutes")
        PomodoroForm()
    if choice == "Timer":
        st.title("Timer")
        timerForm()
    if choice == "Histori Belajar":
        st.title("Histori Belajar")
        analyze()

def timerForm():
    col5, col6 = st.columns(2)
    col1, col2, col3,col4 = st.columns(4)
    with col1:
        start = st.button("Start")
    with col2:
        st.button("Stop")
    with col3:
        reset = st.button("Reset")
    with col4:
        resume = st.button("Resume")
    with col5:
        dataTime = input()
    with col6:
        if start:
            status = st.empty()           
            timePrinted = st.empty()
            status.success("Timer Running")
            timerr(dataTime,timePrinted)
            status.warning("Timer Stoped")        
            status.warning("Time is up")              
        if reset:
            st.stop()  
        if resume:
            ganti = st.empty
            global timersave
            timerr(timersave, ganti)
            
def input():
    try:
        listTime = [0,0,0]
        listTime[0] = int(st.text_input("Hours", 00))
        listTime[1] = int(st.text_input("Minutes", 00))
        listTime[2] = int(st.text_input("Seconds", 00))
        if listTime[1] >= 60 or listTime[2] >= 60:
            st.warning("Angka Tidak Valid")
            if listTime[1] >= 60:
                listTime[1] = 59
                listTime[2] = 59   
            else:
                listTime[2] = 59        
        elif listTime[1] < 0 or listTime[2] < 0:
            st.warning("Angka Tidak Valid")
            if listTime[1] < 0:
                listTime[1] = 0  
                listTime[2] = 0
            else: 
                listTime[2] = 0     
    except ValueError:
            st.write("Invalid Value")
    return listTime  

def timerr(parameter,timePrinted):
    hours = parameter[0]
    minutes = parameter[1]
    seconds = parameter[2]  
    try:
        while True :
            if seconds == 0:
                if minutes == 0:
                    if hours == 0:                       
                        break
                    else:
                        hours -=1
                        minutes = 60
                else: 
                    minutes -= 1
                    seconds = 59
            else:
                seconds -= 1
            timePrinted.title(f"{hours}:{minutes}:{seconds}")
            time.sleep(1)
    except:        
        global timersave
        timersave =  [hours , minutes, seconds]
 
    # ps.playsound("soundtimer.mp3")

def PomodoroForm():
    col1, col2 = st.columns(2)
    col3,col4 = st.columns(2)
    with col3:
        start = st.button("Start")   
        with col1:
            try: 
                Time = st.select_slider('Focus Time',options=[10, 15, 20, 25, 30])
                breakTime = [0,5,0]
                focusTime = [0,Time,0]
                session = int(st.text_input("Session", 1))
            except ValueError:
                st.write("Invalid Value")
    with col2:
        if start:
            status = st.empty()
            timePrinted = st.empty()
            Pomodoro(session, breakTime, focusTime, timePrinted, status)
            savepomodoro(session, focusTime[1])      

def Pomodoro(session, breaktime, focustime, timePrinted, status):
    for i in range(session):
        status.warning("Focus Time")
        timerr(focustime, timePrinted)
        time.sleep(3)
        status.success("Break Time")
        timerr(breaktime,timePrinted)
        time.sleep(3)
    status.success("Selamat Anda Telah Menuntaskan Belajar")
    st.balloons()

def savepomodoro(session, time):
    global data
    nomor = len(data[1])+1    
    data[0].append(nomor)
    data[1].append(time)
    data[2].append(session)
    data[3].append(session * time)

def analyze():
    col1, col2 = st.columns(2)
    col3, col4, col5,col6 = st.columns(4)
    global data
    table = pd.DataFrame({
        "Belajar Ke-" : data[0],
        "Focus Time" : data[1] ,
        "Session" : data[2],
        "Waktu Belajar" : data[3] 
    })

    def tampilanGrapik( data2,  tanda, warna, vertical):
        fig = plt.figure(figsize=(10 , 5))
        plt.plot(data[0], data[data2], '.-',label=tanda, color = warna)
        plt.xlabel("Belajar Ke-")
        plt.ylabel(vertical)
        plt.title(tanda)
        plt.legend()
        return st.pyplot(fig)
       
    def tigaData():
        gambar = plt.figure(figsize=(10,5))
        w = 0.2
        belajar = data[0]
        focusTime = data[1]
        session = data[2]
        waktuBelajar = data[3]
        
        bar1 = np.arange(len(belajar),dtype = int)
        bar2 = [i+w for i in bar1]
        bar3 = [i+w for i in bar2]
        
        plt.bar(bar1 ,focusTime, w , color = "purple", label = "Focus Time")
        plt.bar(bar2 , session , w , color = "blue", label = "Session")
        plt.bar(bar3, waktuBelajar, w, color = "red", label = "Waktu belajar")

        plt.xticks(bar1+w, belajar)
        plt.xlabel("belajar ke-")
        plt.ylabel("Menit/Session")
        plt.title("Grapik Session, Focus Time, Waktu Belajar")
        plt.legend()

        return st.pyplot(gambar)
        
    with col3:
        tmblBelajar = st.button("Waktu Belajar")
    with col4:
        tmblSession = st.button("Session")
    with col5:
        tmblFocus = st.button("Focus")
    with col6:
        tiga = st.button("Tampilkan ke 3 Data")
    with col1:
        kosong = st.empty()
        if tmblBelajar:
            kosong.write("Grapik Waktu Belajar (session x belajar)")
            c = tampilanGrapik(3,"Waktu Belajar", "red","Menit")
        elif tmblSession:
            kosong.write("Grapik Session")
            d = tampilanGrapik(2,"Session", "blue","Session")
        elif tmblFocus:
            kosong.write("Grapik Focus Time")
            f = tampilanGrapik(1, "Focus Time" , "purple", "Menit" )
        elif tiga:
            kosong.write("Grapik Tiga Data")
            grapik = tigaData()
        st.write("Tabel Histori Belajar")
        st.write(table)

menu()
