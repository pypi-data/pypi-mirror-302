# python 3.10 -> eol at 2026-10
import time


def startTime():
    start_time = time.time()
    return start_time

def endTime():
    end_time = time.time()
    return end_time

def calculateWork(et, st):
    if (et or st != 0):
        work_time = et-st
        print(work_time)
        return work_time
    else: 
        print("program has not finished or started")