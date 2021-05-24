import schedule

import subprocess
import os

def stock_watch_job_start():
    print("启动stock_watch.exe")
    #win32api.ShellExecute(0, 'open', r'C:\Users\Administrator\Desktop\stockWatch.exe', '', '', 1)
    #os.system(r"C:\Users\Administrator\Desktop\stockWatch.exe")
    subprocess.run('cd C:\Users\Administrator\Desktop\stockWatch && stockWatch.exe ', shell=True)
def stock_watch_job_end():
    print("停止stock_watch.exe")
    os.system("taskkill /F /IM stockWatch.exe")


def glob_watch_job_start():
    print("启动glob_watch.exe")
    #win32api.ShellExecute(0, 'open', r'C:\Users\Administrator\Desktop\goldWatch.exe', '', '', 1)
    os.system(r"C:\Users\Administrator\Desktop\goldWatch\goldWatch.exe")
    subprocess.run('cd C:\Users\Administrator\Desktop\sgoldWatch && goldWatch.exe ', shell=True)
def glob_watch_job_end():
    print("停止glob_watch.exe")
    os.system("taskkill /F /IM goldWatch.exe")

if __name__ == "__main__":
    print("启动定时任务....")

    schedule.every().day.at("08:50").do(stock_watch_job_start)
    print("每天8点50启动stockWatch.exe....")
    schedule.every().day.at("15:40").do(stock_watch_job_end)
    print("每天下午3点40关闭stockWatch.exe....")
    schedule.every().day.at("08:50").do(glob_watch_job_start)
    print("每天8点50启动goldWatch.exe....")
    schedule.every().day.at("22:10").do(glob_watch_job_end)
    print("每天晚上10点10启动goldWatch.exe....")
    #schedule.every(2).seconds.do(stock_watch_job)
    while True:
        schedule.run_pending()
