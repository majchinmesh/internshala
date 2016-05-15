from bs4 import BeautifulSoup
import requests


Domain = 'http://internshala.com'
MURL = 'http://internshala.com/internships/computer science-internship/page-1'



def getTitle(I):
	return I.h4.get("title").encode('utf-8')


def getLocation(I):
	return I.find_all("span")[1].a.text.encode('utf-8')

def getTData(TD):
     TD = TD.text.encode('utf-8')
     temp = TD.split("  ")
     temp2 = ""
     for t in temp:
             temp2 += t
     return temp2.split("\r\n")[1]

def getTH(TH):
	return TH.text.encode('utf-8')

def getFOP(I):
	try :
		return getTData(I.find_all("div" ,{"class":"full-time-container"})[0])
	except :
		try :
			return getTData(I.find_all("div" ,{"class":"part-time-container"})[0])
		
		except:
			return "NA" 

def getLink(I):
	return Domain + I.find_all("a")[2].get("href").encode("utf-8")

def replaceAmpersand():
	XML = open("allInternships.xml",'r')
	code = XML.read()
	XML.close()
	
	code = code.split("&")
	code = 'and'.join(code)

	XML = open("allInternships.xml",'w')
	XML.write(code)
	XML.close()
	



File = open("allInternships.txt",'w')
XML = open("allInternships.xml",'w')

XML.write('<?xml version="1.0" encoding="ISO-8859-1" ?>\n')
XML.write("<AllInterships>")


i = 1 ;
counter = 0 
while 2>1 :
	Req = requests.get(MURL)
	Sop = BeautifulSoup(Req.content)
	INTS = Sop.find_all("div" ,{"class":"container-fluid individual_internship"}) 
	for I in INTS :
		XML.write("<Internship>\n\n")
		counter +=1 
		
		s =  getTitle(I)
		print "Title  :  " +s
		File.write("Title  :  " +s+"\n")
		XML.write("<Title>"+s+"</Title>\n")

		s =  getLocation(I)
		print"Location  :  " + s
		File.write("Location  :  " +s+"\n")
		XML.write("<Location>"+s+"</Location>\n")

		s = getFOP(I)
		print "Full/Part Time  :  " + s
		File.write("Full/Part Time  :  " + s+"\n")
		XML.write("<FullOrPart>"+s+"</FullOrPart>\n")

		th = I.find_all("th")
		td = I.find_all("td")
		
		for d in range(0,len(th)):
			t =  getTH(th[d]) 
			s = getTData(td[d])
			print t+"  :  "+s
			File.write(t+"  :  "+s +"\n")
			try :
				tag = t.split(" ")[0]+t.split(" ")[1]
			except:
				tag = t.split(" ")[0]

			XML.write("<"+tag+">" + s + "</"+tag+">\n")

			


		s = getLink(I)
		print "Link  :  " +  s
		File.write("Link  :  " + s+"\n")
		XML.write("<Link>"+s+"</Link>\n")

		
		print "\n\n"	
		File.write("\n\n\n")
		XML.write("</Internship>\n\n\n")

	print "\nDone with page " + str(i) + "\n" 
	next = Sop.find_all("a",{"id":"navigation-forward"},{"onclick":"return false"})[0]

	if next.get("href").encode('utf-8') == '#' :
		print "\n\n\nFound "+ str(counter) + " internships in all."
		XML.write("</AllInterships>")
		XML.close()
		replaceAmpersand() 
		File.close()
		break 
	else :
		i+=1
		MURL = Domain+ next.get("href").encode('utf-8')
		print "Next Page URL : "+MURL
 




while 2>1 :
	XML = open("allInternships.xml",'r')
	code = XML.read()
	print "\n\n"
	month = raw_input("Which month (i.e. Feb , May , Mar etc): ")
	fil = open(month+".txt",'w')
	
	sop = BeautifulSoup(code)
	ins = sop.find_all("internship")

	for i in ins:
		try:
			if i.startdate.text.encode('utf-8').split(' ')[1]==str(month+","):
				fil.write(i.title.text)
				fil.write("\n")
				fil.write(i.location.text)
				fil.write("\n")
				fil.write(i.startdate.text)
				fil.write("\n")
				fil.write(i.stipend.text)
				fil.write("\n")
				fil.write(i.link.text)
				fil.write("\n\n")
		except:
			pass

	fil.close()

