import urllib2
import urllib
import re
import os
import datetime
import time
import warnings
#Function to check if the LastModificationTime of file > LastDownloadTime of file
def mDate(fname,dat):
	if not os.path.isfile(fname): return 1
	(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fname)
	LDT =datetime.datetime.strptime(datetime.datetime.fromtimestamp(mtime).strftime('%d/%m/%y %H:%M'),"%d/%m/%y %H:%M") 
	date,time1=dat.split(" ")
	day,month,year=date.split("-")
	hh,mm=time1.split(":")
	d = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
	LMT= datetime.datetime(int(year),d[month],int(day),int(hh),int(mm))
	if(LMT>LDT): return 1
	else: return 0
#Function to create a dir if not created
def mDir(Dir):
	if not os.path.exists(Dir):
		os.mkdir(Dir)
#Function to download each folder and its contents
def dwnld(n):	
	global q,fpattern,savDir,mainUrl,down,ndown,nd
	tsavDir = savDir + q[n]
        url = mainUrl + q[n]
	try:
        	lines = opener.open(urllib2.Request(url)).read().split('\n') #For extracting filenames from that page
        	q0 = [str((re.findall(fpattern,i))[0])+"~"+str((re.findall(dpattern,i))[0]) for i in [i for i in lines if 'alt="[TXT]"' in i or 'alt="[   ]"' in i and "Parent Directory" not in i and "key" not in i]]
        	q1 = dict([tuple(q0[p].split("~")) for p in range(len(q0))]) #Dict with keys as filename and values as modified date
		if q1 != {}:
			mDir(tsavDir)
			for i in q1: #i is filename
				fname = os.path.join(tsavDir,i)
				if(mDate(fname,q1[i])):
			 		try:
						data = opener.open(urllib2.Request(url+i))
						print "downloading file : ",i
                    				fname = os.path.join(tsavDir,i)
                    				with open(fname,"wb") as d:
                    					d.write(data.read())
						down += 1
                			except urllib2.URLError, e:
    						if hasattr(e, 'reason'):
							print '****',i,' - We failed to reach server.Reason: ', e.reason,'****'
    						elif hasattr(e, 'code'):
        						print '****',i,' - The server couldn\'t fulfill the request.Error code: ', e.code,'****'
        					else:
        						print '****',i,' cannot be downloaded due to some error','****'
						nd.append(i)
						ndown +=1
				else:
					print i," is not modified hence not downloaded"
	except urllib2.URLError, e:
    		if hasattr(e, 'reason'):
        		print 'We failed to reach server.'
        		print 'Reason: ', e.reason
    		elif hasattr(e, 'code'):
        		print 'The server couldn\'t fulfill the request.'
        		print 'Error code: ', e.code
        	else:
      			print 'Page Cannot be Displayed due to some error'
			
def main():
	global q,fpattern,savDir,mainUrl
	try:
		mDir(savDir)
		#Extracting all folders present in ISE Directory
		lines = opener.open(urllib2.Request(mainUrl)).read().split('\n')
		q = [(re.findall(fpattern,i))[0] for i in [i for i in lines if 'alt="[DIR]"' in i and "Parent Directory" not in i]]
		#Go into each folder and download all files
		for folders in range(0,len(q)):
			dwnld(folders)
	except urllib2.URLError, e:
    		if hasattr(e, 'reason'):
        		print 'We failed to reach server.'
        		print 'Reason: ', e.reason
    		elif hasattr(e, 'code'):
        		print 'The server couldn\'t fulfill the request.'
        		print 'Error code: ', e.code
        	else:
      			print 'Page Cannot be Displayed due to some error'

savDir = os.getcwd()+"/CompNwks/" #Main folder in which all files will be saved
mainUrl = 'http://ise.pesit.pes.edu/ISE/2013-CS301/' #URL from which files are downloaded
fpattern = r'(?<=href=").+?(?=")' #Regex to recognize each folder from main page
dpattern = r'\d{2}-\w{3}-\d{4} \d{2}:\d{2}' #Regex to extract last modified date
down = ndown = 0 #Counters to count the number of files downloaded and not downloaded
q = nd = [] #q contains all folder names and nd contains all filenames which can't be downloaded
if(__name__=="__main__"):
	start = time.time()
	#HTTP basic authentication
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, mainUrl, "ISE", "PESIT")
	handler = urllib2.HTTPBasicAuthHandler(password_mgr)
	# create "opener" (OpenerDirector instance)
	opener = urllib2.build_opener(handler)
	# use the opener to fetch a URL
	# Install the opener. Now all calls to opener.open use our opener.
	urllib2.install_opener(opener)
	warnings.filterwarnings("ignore", category=UserWarning, module='urllib2')
	main()
	end = time.time()
	print "\n----------------REPORT-----------------------"
	print "It took : ",end-start,"seconds"
	if(down!=0): print down," file(s) downloaded"
	if(ndown!=0): print "Error downloading files : "
	if(nd!=[]): print "\t",nd
	print "---------------------------------------------"
