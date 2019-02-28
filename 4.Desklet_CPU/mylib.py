##!/usr/bin/python
from os import popen
from time import sleep
class cpu:
    def __init__(self):
        try:
            self.core_number=self.get_cpu_core_number()
            self.percent=self.calculate_cpu_percent()
        except Exception: 
            self.core_number=1
            self.percent=[0,0]
    def get_cpu_core_number(self):
        try:
            cmd=popen('grep "processor" /proc/cpuinfo')
        except Exception: print('error read cpuinfo')
        core_number=len(cmd.read().splitlines())
        cmd.close()
        return core_number
    def get_cpu_job_info(self):
        cpu=[]
        try:
            cmd=popen('grep "cpu" /proc/stat')
        except Exception: print('error read stat')            
        for i in range(self.core_number+1):
            cpu.append(cmd.readline().split())
        cmd.close()
        return cpu
    def calculate_cpu_percent(self):
        ok=False
        cpu=[]
        while not ok:
            jobs_begin=self.get_cpu_job_info()
            sleep(0.5)
            jobs_end=self.get_cpu_job_info()
            for i in range(len(jobs_begin)):
                active=(int(jobs_end[i][1])+int(jobs_end[i][3])+\
                    int(jobs_end[i][5]))-(int(jobs_begin[i][1])+\
                    int(jobs_begin[i][3])+int(jobs_begin[i][5]))
                total=active+int(jobs_end[i][4])-int(jobs_begin[i][4])
                if total==0:
                    print('total equal 0')                                        
                    cpu=[]
                    break
                else:    
                    cpu.append(100*active/total)
                    ok=True
        return cpu
#print cpu().core_number
#print cpu().percent
