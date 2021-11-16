import os

while True:
            try: 
                response = self.conn.getresponse().read()
                print(response)
            except:
                os.system("/usr/bin/python3 /home/pi/person_detection/oak1_counter.py -cam")