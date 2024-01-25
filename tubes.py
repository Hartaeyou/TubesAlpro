import streamlit as st
import time
from timeit import default_timer as timer
import playsound as ps
import os
                
def menu():
    menu = ["Stopwatch", "Pomodoro", "Timer"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Stopwatch":
        st.title("Stopwatch")
        st.write("This is stopwatch")
    if choice == "Pomodoro":
        st.title("Pomodoro Timer")
        st.write("This Is Pomodoro Timer")
        pomodoro()
    if choice == "Timer":
        st.title("Timer")
        timerForm()

def input():
    try:
        listTime = [0,0,0]
        hours = int(st.text_input("Hours", 00))
        minutes = int(st.text_input("Minutes", 00))
        seconds = int(st.text_input("Seconds", 00))
        listTime[0] = hours
        listTime[1] = minutes
        listTime[2] = seconds
        if listTime[1] > 60 and listTime[2] > 60:
            st.write("Angka Tidak Valid")
            listTime[1] = 59
            listTime[2] = 59
        elif listTime[1] < 0 or listTime[2] < 0:
            listTime[1] = 0
            listTime[2] = 0
        
    except ValueError:
            st.write("Invalid Value")
    return listTime

def timerForm():
    col1, col2 = st.columns(2)
    col3, col4, col5 = st.columns(3)
    with col3:
        start = st.button("Start")
        state = "Start"
    with col4:
        global stop
        stop = st.button("Stop")
    with col5:
        ulangi = st.button("Ulangi Timer")
    with col1:
        dataTime = input()
        pauseTime = int(st.text_input("Pause time", 10))
    with col2:
        
        if start and state == "Start":
            data1 = timerr(dataTime)
        if stop and state == "Start":
            st.write(data1)
        if ulangi and state == "Start" and state == "Pause":
            state = "Start"

    
def timerr(parameter):
    hours = parameter[0]
    minutes = parameter[1]
    seconds = parameter[2]
    timePrinted = st.empty()
    while True :
        if seconds == 0:
            if minutes == 0:
                if hours == 0:
                    st.success("Time is Up!")
                    ps.playsound("soundtimer.mp3")
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
        data1 = []
        data1.append(hours)
        data1.append(minutes)
        data1.append(seconds)
        return data1

def pomodoro():
    start = st.button("Start")
    st.write("Break Time = 5 Minute")
    listkosong = [0,0,0]
    time = [1,15,25]
    choice = st.selectbox("Pilih Waktu Fokus (menit)", time)
    if choice == 1:
        listkosong[1] = time[0]
        if start:
            timerr(listkosong)
    if choice == 15:
        listkosong[1] = time[1]
        if start:
            timerr(listkosong)
    if choice == 25:
        listkosong[1] = time[2]
        if start:
            timerr(listkosong)
        

menu()
