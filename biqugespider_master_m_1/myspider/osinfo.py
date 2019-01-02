import psutil



def cpu_percent():
    cpu_percent = psutil.cpu_percent() 
    return cpu_percent

def cpu_percent_list():
    cpu_percent_list = psutil.cpu_percent(percpu=True) 
    return cpu_percent_list

def disk_percent():
    mem = psutil.virtual_memory()
    disk_percent = mem.percent
    return disk_percent