
import streamlit as st
import os
import psutil
import time
import datetime

def get_cpu_memory_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    return cpu_percent, memory.percent

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent

def list_running_processes(limit=10):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:limit]

def show_watchdog_panel():
    st.title("📡 System Watchdog Panel")

    col1, col2, col3 = st.columns(3)
    with col1:
        cpu, mem = get_cpu_memory_usage()
        st.metric("🧠 CPU Usage (%)", f"{cpu}%")
    with col2:
        st.metric("💾 RAM Usage (%)", f"{mem}%")
    with col3:
        disk = get_disk_usage()
        st.metric("🗄️ Disk Usage (%)", f"{disk}%")

    st.divider()

    st.subheader("🔍 Top Running Processes")
    processes = list_running_processes()
    st.table(processes)

    st.divider()

    if st.button("🔄 Refresh Now"):
        st.rerun()
