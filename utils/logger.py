import datetime

def log(source, message):
    time= datetime.datetime.now().strftime('%d-%m-%Y, %H:%M:%S')
    print(f"[{time}] [{source}] {message}")