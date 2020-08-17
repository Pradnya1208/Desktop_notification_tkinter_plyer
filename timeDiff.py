import datetime
import time


filename = 'covid.txt'
refresh_time = '23:00:00'
with open(filename, "r") as file:
    first_line = file.readline()
    

        
date_time_str = first_line  # previous data loading time
print ( "date_time_str"+date_time_str)
date_time_str = date_time_str.replace("\n",'')
format = "%b %d %Y at %I:%M%p"

start_time = datetime.datetime.now().strftime(format)
end_time = datetime.datetime.strptime(date_time_str,format)
print('start time:' + start_time )
print('end time:' + str(end_time))

total_time= datetime.datetime.strptime(start_time,format) - datetime.datetime.strptime(date_time_str,format)



print (total_time)
if total_time.days >= 1:
    print ("Time to refresh")
   
else:
    print ("comparing hours....")
    if ',' in str(total_time):
        t = (str(total_time).split(',')[1]).replace(' ','')
        t1 = datetime.datetime.strptime(t, '%H:%M:%S')
        print (t)
    else :
        t = str(total_time)
        t1 = datetime.datetime.strptime(t, '%H:%M:%S')
        
    t2 = datetime.datetime.strptime(refresh_time, '%H:%M:%S')
    
  
    if t1.time() > t2.time():
        print ("Its time to refresh")
    else:
        print ("Hang in there")
        
        



