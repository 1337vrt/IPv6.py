#!/usr/bin/python3
# -*- coding: utf-8 -*-
import getopt,sys,os,subprocess

def banner():
  print("""
 dP  888888ba           .d8888P 
 88  88    `8b          88'     
 88 a88aaaa8P' dP   .dP 88baaa. 
 88  88        88   d8' 88` `88 
 88  88  v1.1  88 .88'  8b. .d8 
 dP  dP        8888P'   `Y888P' 
oooooooooooooooooooooooooooooooo
                              
https://github.com/vrt36/ipv6.py
________________________________
  """)

def help():
  print("""
USAGE : ipv6 [-h] -d | -e | -p
To disable IPv6 permanently : sudo ipv6 -p
OPTIONS :
  -h       Show this help message and exit
  -d       Disable IPv6 temporarily
  -e       Enable IPv6 temporarily
  -p       Disable IPv6 permanently
  """)
  exit()

def check_root():
 if os.geteuid() != 0:
    print("You need to run this program as 'sudo'")
    exit()

def conf_dis():
   q = subprocess.getoutput("cat /proc/sys/net/ipv6/conf/all/disable_ipv6")
   if q == '1':
     print("[+] Already Disabled")
     exit()

def conf_en():
   q = subprocess.getoutput("cat /proc/sys/net/ipv6/conf/all/disable_ipv6")
   if q == '0':
     print("[+] Already Enabled")
     exit()

def disipv6():
     check_root()
     conf_dis()
     print("[+] Disabling IPv6")
     subprocess.run(["sysctl","-w","net.ipv6.conf.all.disable_ipv6=1"], stdout=subprocess.DEVNULL)
     subprocess.run(["sysctl","-w","net.ipv6.conf.default.disable_ipv6=1"], stdout=subprocess.DEVNULL)
     subprocess.run(["sysctl","-w","net.ipv6.conf.lo.disable_ipv6=1"], stdout=subprocess.DEVNULL)
     print("[+] IPv6 has been disabled")
     exit()

def perdisipv6():
     check_root()
     pe = open('/etc/sysctl.conf','r')
     qw = pe.read()
     pe.close()
     q = subprocess.getoutput("cat /proc/sys/net/ipv6/conf/all/disable_ipv6")
     if q == '0' and 'net.ipv6.conf.all.disable_ipv6 = 1' in qw:
             subprocess.run(["sysctl","-p"], stdout=subprocess.DEVNULL)
             print("[+] Already Disabled")
             exit()

     elif q == '1' and 'net.ipv6.conf.all.disable_ipv6 = 1' in qw:
             subprocess.run(["sysctl","-p"], stdout=subprocess.DEVNULL)
             print("[+] Already Disabled")
             exit()

     elif 'net.ipv6.conf.all.disable_ipv6 = 0' in qw:
             print("[+] Disabling IPv6")
             qw = qw.replace('net.ipv6.conf.all.disable_ipv6 = 0', 'net.ipv6.conf.all.disable_ipv6 = 1')
             qw = qw.replace('net.ipv6.conf.default.disable_ipv6 = 0', 'net.ipv6.conf.default.disable_ipv6 = 1')
             qw = qw.replace('net.ipv6.conf.lo.disable_ipv6 = 0', 'net.ipv6.conf.lo.disable_ipv6 = 1')
             pen = open('/etc/sysctl.conf','w').write(qw)
             subprocess.run(["sysctl","-p"], stdout=subprocess.DEVNULL)
             print("[+] IPv6 has been permanently disabled")
             exit()

     else:
             print("[+] Disabling IPv6")
             pe = open('/etc/sysctl.conf','w').write("net.ipv6.conf.all.disable_ipv6 = 1\nnet.ipv6.conf.default.disable_ipv6 = 1\nnet.ipv6.conf.lo.disable_ipv6 = 1")
             subprocess.run(["sysctl","-p"], stdout=subprocess.DEVNULL)
             print("[+] IPv6 has been permanently disabled")
             exit()

def enipv6():
     check_root()
     conf_en()
     print("[+] Enabling IPv6")
     subprocess.run(["sysctl","-w","net.ipv6.conf.all.disable_ipv6=0"], stdout=subprocess.DEVNULL)
     subprocess.run(["sysctl","-w","net.ipv6.conf.default.disable_ipv6=0"], stdout=subprocess.DEVNULL)
     subprocess.run(["sysctl","-w","net.ipv6.conf.lo.disable_ipv6=0"], stdout=subprocess.DEVNULL)
     print("[+] IPv6 has been enabled temporarily")
     print("[+] Ipv6 will be automatically disabled when you turn on your PC next time. To enable it next time, run 'ipv6 -e'.")
     exit()

argumentList = sys.argv[1:]
options = "hdpe"

try:
    arguments, values = getopt.getopt(argumentList, options)
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-h"):
            help()

        elif currentArgument in ("-d"):
            banner()
            disipv6()

        elif currentArgument in ("-e"):
            banner()
            enipv6()
           
        elif currentArgument in ("-p"):
            banner()
            perdisipv6()

except getopt.error as err:
    help()

help()
