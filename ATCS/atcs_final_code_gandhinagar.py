# @author DKP
import subprocess
import serial
import time
import datetime
import threading
# import sqlite3
import serial.tools.list_ports
import gc
# from flask import Flask, redirect, request, render_template
import json
import os
import requests
# import math
import psycopg2
import sys, os
import datetime
from datetime import date, timedelta
from waiting import wait, TimeoutExpired
from datetime import datetime
import sys
import copy
#---------------------------- following some line has to be changed as per new hardware and network settings------------------#
# url_events = "http://10.195.96.197/atcs-gmc-webapi/api/Event/Online/"
#url_events = "http://10.195.98.205:89/api/Event/Online"
#url_events = "https://atcssecurewebapi.amnex.com/api/Event/Online"
url_events = "https://SuratWebAPI.amnex.com/api/Event/Online"
#url_events = "https://gscdlwebapi.amnex.com/api/Event/Online"
#url_events = "https://syncnexindorewebapi.amnex.com:4431/api/Event/Online"

# url_current_operating = "http://10.195.96.197:90/atcs-gmc-webapi/api/ControllerLiveAction/Insert"
#url_current_operating = "https://atcssecurewebapi.amnex.com/api/ControllerLiveAction/Insert"
url_current_operating = "https://SuratWebAPI.amnex.com/api/ControllerLiveAction/Insert"
#url_current_operating = "https://gscdlwebapi.amnex.com/api/ControllerLiveAction/Insert"
#url_current_operating = "https://syncnexindorewebapi.amnex.com:4431/api/ControllerLiveAction/Insert"
#url_login  = "https://atcssecurewebapi.amnex.com/api/login"
url_login  = "https://SuratWebAPI.amnex.com/api/login"
#url_login  = "https://gscdlwebapi.amnex.com/api/login"
#url_login  = "https://syncnexindorewebapi.amnex.com:4431/api/login"

url_auto_diag="https://suratwebapi.amnex.com/api/Event/Autodiagnosisevent"

# default_string = "1,17,20,18,23,61,58,60,55,22,42,78,2,3,2,2,2,2\n"

#controller_id = "111 sudo openfortivpn 182.237.15.241:10443 --username=amnexatcs --realm=bar --trusted-cert 934e5c00bb6ce815a186100f78551a65347fd35241eb85933e93336941e0e061111114"
# #----------------Controller_Id---------------------#
# controller_id = ""
# f = open("/home/atreyo-atcs14/Documents/ATCS/controller_id",'r')
# controller_id = f.read()
# f.close()
# controller_id = controller_id[:-1]
# print("controller_id-------",controller_id)
# #---------------------------------------------------#

database_ip = "localhost"
prev_known_fixed_seq = ""
urname = "ATCS"
passwrd = "ATCS@12345"

serial_data = ""
ser = None
error_count = 0
update_flag = 0
#------------------- For Detector Health -----------------------#
detector_ip = ["172.16.7.210","172.16.7.211","172.16.7.212","172.16.7.213"]
detector_health_flag = []
detector_min_time = 8
# ---------------Common to all events---------------------------#

generation_time = "" #datetime.datetime.today().strftime('%d%m%Y%H%M%S') or time.strftime('%d%m%Y%H%M%S')
generation_time_2 = ""
event_type = ""
no_of_parameter = ""
reserved_1 = "000000000000"
reserved_2 = "000000000000"
#--------------------ATCS Variable-------------------------------#
tmp_atcs_stage = 0
tmp_split_stage = 0 
tmp_total_cycle = 0
split_cylce = 0
send_au = 0
#---------Hurry Call , Junction On/Off, Flashing Amber ----------#
arm_no = ""
status = ""
JOFF_flag = 0
prevous_sequence = "" # Temporary sequence which have to send during hurry call events.
temp_key_from_software = "" # Because there will be temporary primary key from server which have to send after hurry call event triggered by switch.
#-------------------RTC Sync-------------------------------------#
rtc_time_diff_sign = ""
rtc_out_of_sync = ""
#--------------------RTC Time Sync Update-------------------------#
rtc_set_time = ""
rtc_time_from = ""
system_time = ""
stored_time = ""
rtc_fail = ""
system_date = ""
#-------------------Stage Skip-----------------------------------#
next_stage = ""
#-------------------Controller reboot----------------------------#
controller_reboot = "00"
#--------------------Power ON------------------------------------#
power_on = '00'
last_off_time = ""
#-------------------Stage Change---------------------------------#
current_seq_no = ""
previous_stage_no = ""
current_stage_no = ""
prev_known_fixed_seq = ""
#-------------------Lamp Health----------------------------------#
lamp_health = '1'
lamp_intensity_1 = ''
prv_lamp_intensity_1 = ''
lamp_health_event_type = "" # Because It takes more time in porcess therefore common variable will not work
lamp_health_no_of_parameter = ""
lamp_id = ""
lamp_ids = ['A','B','C','D','E','F','G','H']
default_no_of_lamps = 7 # it will be change in case of number of lights increase or decrease
lamp_intensity = ''
intensity_event = ''
#-----------------Green Conflict----------------------------------#
lamptype_1 = ""
lampcode_1 = ""
arm_1 = ""
lamptype_2 = ""
lampcode_2 = ""
arm_2 = ""
#------------------Counter Health--------------------------------#
counter_health = '1'
counter_id = ""
#--------------current operating parameter all are assumed by default (all are dummy initializations)-----------------------#
current_zone = "A1"
current_mode = "5"
prv_mode = ""
corridor = "U"
total_stage = "9"
all_stage_time = ['120','3','90','3','60','3','70','3','10']
current_cycle_time = ""
msg_stage_timing = "$08008003008003008003008003#"
#-------------cycle change report-----------------------------#
previous_cycle_time = "0"
cycle_start_date_time = time.strftime('%Y-%m-%d %H:%M:%S') 
#----------------------------------------------------------------#
atcs_exe_flag = 0
exe_status_flag = 0
final_msg = ""
#---------------------------------------AX--------------------------added by krusha on 17/01/2022---#
arm_id_1 = 1		#added by krusha
arm_id_2 = 2
arm_id_3 = 3
arm_id_4 = 4
lamp_fb_1 = ""
re_seq_1 = ""
stage_no_1 = ""
mode_1 = ""
timer_count_1 = ""
time_bet_con_1 = ""
lamp_fb_2 = ""
re_seq_2 = ""
stage_no_2 = ""
mode_2 = ""
timer_count_2 = ""
time_bet_con_2 = ""
lamp_fb_3 = ""
re_seq_3 = ""
stage_no_3 = ""
mode_3 = ""
timer_count_3 = ""
time_bet_con_3 = ""
lamp_fb_4 = ""
re_seq_4 = ""
stage_no_4 = ""
mode_4 = ""
timer_count_4 = ""
time_bet_con_4 = ""
HC_Flag = 0
hcid1 = 0
count_num = 0
attempt = 0
mod_flag = 0
reboot_flag = 0
ar_flag = 0
raw_flag = 0
condition_flag = 0
condition_count = 0
ap_count = 0
stage_count = 7
previous_stage = 0
#global hcid1
list_total_cycle_from_db = []
list_split_time_from_db = []
list_atcs_time_from_db = [] 
#----------------------for events mode change-----------------------#
event_start_time = time.strptime(time.strftime('%H:%M:%S'),'%H:%M:%S')
event_end_time = time.strptime(time.strftime('%H:%M:%S'),'%H:%M:%S')


final_token = ""
time.sleep(1)


#--------------------------get_flag--------------------------#HARSHAD
get_flag = 0        #HARSHAD

global TA  # totalarm                        #HARSHAD
TA = 4  # total arm        # DO NOT CHANGE   #HARSHAD
#--------------------------------------------------------------#HARSHAD

#--------------------------OTA flag--------------------------------#	krusha
OTA_flag = '4'
#------------------read data from file-----------------------------#
def read_file(file):
	try:
		f = open(file,'r')
		data = f.read()
		f.close()
		return data.strip()
	except:
		print("No file to open !")

#----------------write data to file----------------------------------#
def write_to_file(file,data):
	global serial_data
	try:
		f = open(file,'w')
		f.write(data)
		f.close()
	except:
		print("No file to write")
#--------------------device_name-----------------------------------#
# device_name = read_file("/home/atcs-02/Documents/ATCS/device_name")
time.sleep(2)
device_name = subprocess.check_output("logname").decode('utf-8').strip() # This will fetch the username of the processor.
print("device_name:::::::",device_name)
#--------------------------------------------------------------------#

#--------------------controller_id-----------------------------------#
controller_id = read_file("/home/{}/Documents/ATCS/controller_id".format(device_name))
print("controller_id-------",controller_id)

# OTA_string_1 = "$" + controller_id + ","  
# OTA_string_2 = ",AQ,013,000000000000,000000000000,2,U,9999999,1,2,"
# OTA_string_3 = "@002#"
#"$1111111113,31082021020416,AQ,013,000000000000,000000000000,2,U,9999999,1,2,31082021020416@002#"
#--------------------------------------------------------------------#

#-------------------------For Initialization of detector_health_flag------------------------------------#
def initialize_detector_health_flag():
	global detector_health_flag
	for i in range(len(detector_ip)):
		detector_health_flag.append(0)

def insert_raw_data(new_final_msg):

	try:
		if(new_final_msg[-1] != '#'):
			new_final_msg = new_final_msg + time.strftime('%d%m%Y%H%M%S') + "#"	
		print("new_final_msg::::::",new_final_msg)
		inser_querry = "INSERT INTO atcs.eventrawstringLogs(eventrawstring,createdon) VALUES (%s,now())"
		WriteToDatabase(inser_querry, new_final_msg)
	except Exception as e:
		print(e)

#----------------------------Following are to auto detect serial----------------------------------------#
def detect_port():
	global ser
	while True:
		try:
			list_of_ports = [p.device for p in serial.tools.list_ports.comports() if (('Prolific' in p.description) or ('Controller' in p.description) or ('USB' in p.description) or ('Serial' in p.description) or ('USB to UART Bridge'in p.description))]
			#list_of_ports = [ p.device for p in serial.tools.list_ports.comports() if (('Prolific' in p.description ) or ('Controller' in p.description ))]
			print(list_of_ports)
			collected = gc.collect()
			print ("Garbage collector: collected %d objects." % (collected))
			port1 = list_of_ports[0]    #port1 = list_of_ports[0]
			print("port1::::::::::",port1)
			ser = serial.Serial(port1,115200,timeout=2)   #Default 115200
			print("ser::::::::::", ser)
			#ser.flush()
			#ser.flushInput()
			#ser.flushOutput()
			print(ser)
			break
		except:
			time.sleep(1)
			continue
#######################################################################
######################################HARSHAD##########################
def new_read_serial():
	global ser

	while True:
		try:
			print("In Read Serial:::::::::::::::::::::::::::::::::::::")
			new_serial_data = ser.readline().decode()
			# ser.read(size=30)
			# ser.flush()

			#ser.flushInput()
			# ser.flushOutput()
			d_q_sqser = "DELETE from atcs.serial_datalog WHERE createdon < (now() - interval '2 days')"
			WriteToDatabase(d_q_sqser)
			sqserial = "INSERT INTO atcs.serial_datalog (serialdata , createdon ) VALUES(%s,%s)"
			WriteToDatabase(sqserial, str(new_serial_data), time.strftime('%Y-%m-%d %H:%M:%S'))
			threading.Thread(target=handle_serial_data, args=(new_serial_data,)).start()
		except Exception as e:
			print("ERROR IN NEW READ SERIAL",e)
			detect_port()

def handle_serial_data(serial_dat):
	global respond_flag
	global mode_flag
	global start_exe_flag
	global prevous_priority
	global error_count
	global ser
	global update_flag
	global current_seq_no
	global reboot_flag
	global OTA_flag  # krusha
	global priority_flag
	global current_mode
	global cf_counter

	start_exe_flag = 1  # this flag will reset when controller will send
	# start exe string after completing current cycle during mode change in VA
	respond_flag = 1  # For dual side communications

	try:
		if (len(serial_dat) >= 2):

			print(serial_dat)
			serial_data = serial_dat.split(",")
			print(serial_data)

			if ((serial_data[0] == "$" or serial_data[0] == " \x00$" or serial_data[0] == "\x00$" or serial_data[
				0] == "OKOK$") and serial_data[-1] == "#\n"):

				generation_time = time.strftime('%d%m%Y%H%M%S')  # datetime.datetime.today().strftime('%d%m%Y%H%M%S')
				generation_time_2 = time.strftime('%Y-%m-%d %H:%M:%S')  # For write in Database
				time.sleep(0.2)
				threading.Thread(target=process_serial_data,args=(serial_data, generation_time, generation_time_2)).start()
				error_count = 0
				time.sleep(0.2)
				threading.Thread(target=watchdog, args=(serial_data,)).start()  # commented by Harshad

			elif (str(serial_data[0]) == "OK"):
				print("Acknowledged from controller..........")
				respond_flag = 0
				error_count = 0

			elif (str(serial_data[0]) == "GET" or str(serial_data[0]) == "GET\n"):
				print("controller Expecting sequence again ???????..........")
				mode_flag = 0
				prevous_priority -= 1
				error_count = 0
				#cf_counter =0

				# if (get_flag == 0):    #HARSHAD
				#threading.Thread(target=send_hurrycall_keypad).start()  ###################HARSHAD
				send_hurrycall_keypad()
				threading.Thread(target=check_n_send_global_variables).start()
				start_exe_flag = 0
			# get_flag=1    #HARSHAD
			# threading.Thread(target=get_flag_reset).start()   #HARSHAD   from  if condition

			elif ((str(serial_data[0]) == "Start Exe") or (str(serial_data[0]) == "Start Exe\n")):
				print("starting exe....................")
				start_exe_flag = 0
				error_count = 0

			elif ((str(serial_data[0]) == "update") or (str(serial_data[0]) == "update\n")):
				update_flag = 1
				reboot_flag += 1
				print("starting new thread..............")
				if reboot_flag == 2:
					write_to_serial("reboot#")
					reboot_flag = 0
				threading.Thread(target=CheckDatabase).start()

			elif ((str(serial_data[0]) == "ATCS Tumkuru Master: Version 1.0.0") or (str((serial_data[0])) == 'ATCS Tumkuru Master: Version 1.0.0\r\n')):
				print("Reset ATCS Variable....")
				list_total_cycle_from_db = []
				list_atcs_time_from_db = []
				list_split_time_from_db = []
				print(list_total_cycle_from_db, list_atcs_time_from_db, list_split_time_from_db)

			elif ((str(serial_data[0]).strip().lower() == "cycle over")):
				print("Got cycle over ....................")
				if current_mode == '2' or current_mode == '3' or current_mode == '4' or current_mode == '6' or current_mode == '7':
					time.sleep(3)
				print("calling from cycle over")
				threading.Thread(target=send_cycle_over_event).start()
				start_exe_flag = 0
				error_count = 0
			elif (str(serial_data[0]) == "kill atcs" or str(serial_data[0]) == "kill atcs\n"):
				print("Sending mode change event.....")
				current_seq_no = "8888888"
				threading.Thread(target=check_mode_chnage).start()
		else:
			error_count += 1
		if (error_count > 1000):  # If error continue or controller doesn't send any data then send it to reboot
			write_to_serial("reboot")
			error_count = 0
	except Exception as e:
		error_count += 1
		print("-------Eorrr in read serial :: ", e)
		if (error_count > 1000):
			try:
				write_to_serial("reboot")
			except Exception as e:
				print("communications failed with microcontroller xxxxxxxx", e)
				detect_port()
				error_count = 0


########################################################################HARSHAD################
################################################################################################
#-------------------------------Continous reading serial----------------------#
def read_serial():	
	
	global respond_flag
	global mode_flag
	global start_exe_flag
	global prevous_priority
	global error_count
	global ser
	global update_flag
	global current_seq_no
	global reboot_flag
	global OTA_flag 							#krusha
	global priority_flag
	global current_mode

	global get_flag                       #HARSHAD



	start_exe_flag = 1 # this flag will reset when controller will send
					# start exe string after completing current cycle during mode change in VA 
	respond_flag = 1 # For dual side communications	

	

	while True:

		try:

			if(OTA_flag != 1):				#krusha
				print("In Read Serial:::::::::::::::::::::::::::::::::::::")
				serial_dat = ser.readline().decode()
				#ser.read(size=30)
				#ser.flush()

				ser.flushInput()
				#ser.flushOutput()
				d_q_sqser="DELETE from atcs.serial_datalog WHERE createdon < (now() - interval '2 days')"
				WriteToDatabase(d_q_sqser)
				sqserial= "INSERT INTO atcs.serial_datalog (serialdata , createdon ) VALUES(%s,%s)"
				WriteToDatabase(sqserial, str(serial_dat), time.strftime('%Y-%m-%d %H:%M:%S'))


				if(len(serial_dat) >= 2):
					
					print(serial_dat)
					serial_data = serial_dat.split(",")
					print(serial_data)
						
					if ((serial_data[0] == "$" or serial_data[0] == " \x00$" or serial_data[0] == "\x00$" or serial_data[0] == "OKOK$") and serial_data[-1] == "#\n" ):

						generation_time = time.strftime('%d%m%Y%H%M%S') 				  #datetime.datetime.today().strftime('%d%m%Y%H%M%S')
						generation_time_2 = time.strftime('%Y-%m-%d %H:%M:%S') # For write in Database
						time.sleep(0.2)
						threading.Thread(target=process_serial_data, args = (serial_data,generation_time,generation_time_2)).start()
						error_count = 0
						time.sleep(0.2)
						threading.Thread(target=watchdog, args = (serial_data,)).start()		#commented by Harshad
	
					elif(str(serial_data[0]) == "OK"):
						print("Acknowledged from controller..........")
						respond_flag = 0
						error_count = 0
	
					elif(str(serial_data[0]) == "GET" or str(serial_data[0]) == "GET\n"):
						print("controller Expecting sequence again ???????..........")
						mode_flag = 0
						prevous_priority -= 1
						error_count = 0

						#if (get_flag == 0):    #HARSHAD
						threading.Thread(target=send_hurrycall_keypad).start() ###################HARSHAD
						threading.Thread(target=check_n_send_global_variables).start()
						start_exe_flag = 0
							#get_flag=1    #HARSHAD
							#threading.Thread(target=get_flag_reset).start()   #HARSHAD   from  if condition


					elif((str(serial_data[0]) == "Start Exe") or (str(serial_data[0]) == "Start Exe\n")):
						print("starting exe....................")
						start_exe_flag = 0					
						error_count = 0
	
					elif((str(serial_data[0]) == "update") or (str(serial_data[0]) == "update\n")):
						update_flag = 1
						reboot_flag += 1
						print("starting new thread..............")
						if reboot_flag == 2:
							write_to_serial("reboot#")
							reboot_flag = 0
						threading.Thread(target = CheckDatabase).start()
	
					elif((str(serial_data[0]) == "ATCS Tumkuru Master: Version 1.0.0") or (str((serial_data[0])) 	== 'ATCS Tumkuru Master: Version 1.0.0\r\n')):
						print("Reset ATCS Variable....")
						list_total_cycle_from_db = []  
						list_atcs_time_from_db = []    
						list_split_time_from_db = []   
						print(list_total_cycle_from_db,list_atcs_time_from_db,list_split_time_from_db)
	
					elif((str(serial_data[0]).strip().lower() == "cycle over")):
						print("Got cycle over ....................")
						if current_mode == '2' or  current_mode == '3' or  current_mode == '4' or current_mode == '6' or current_mode == '7':
							time.sleep(3)
						print("calling from cycle over")
						threading.Thread(target=send_cycle_over_event).start()
						start_exe_flag = 0					
						error_count = 0
					elif(str(serial_data[0]) == "kill atcs" or str(serial_data[0]) == "kill atcs\n"):
						print("Sending mode change event.....")
						current_seq_no = "8888888"
						threading.Thread(target=check_mode_chnage).start()
	
				else:
					error_count += 1
			else:
				time.sleep(3)
				generation_time = time.strftime('%d%m%Y%H%M%S') 				  #datetime.datetime.today().strftime('%d%m%Y%H%M%S')
				generation_time_2 = time.strftime('%Y-%m-%d %H:%M:%S') # For write in Database
				time.sleep(0.2)
				threading.Thread(target=process_serial_data, args = (serial_data,generation_time,generation_time_2)).start()
	
			if(error_count > 1000): # If error continue or controller doesn't send any data then send it to reboot
				write_to_serial("reboot")
				error_count = 0
	
		except Exception as e:
			error_count += 1
			print("-------Eorrr in read serial :: ",e)
			if(error_count > 1000):
				try:
					write_to_serial("reboot")
				except Exception as e:
					print("communications failed with microcontroller xxxxxxxx",e)
					detect_port()
					error_count = 0
	print("Entering OTA mode......................................................................")

##############################################################HARSHAD
def send_hurrycall_keypad():
	global TA  # totalarm                        #HARSHAD
	TA = 4  # total arm        # DO NOT CHANGE   #HARSHAD
	km=[]
	my_keys = {}
	for i in range(1, TA + 1):
		key_name = "key%d" % i
		my_keys[key_name] = 0
	#print(my_keys)
	a = "select armid,switchid from atcs.hurrycallconfigmaster"
	ka=ReadDatabase(a)
	#for i in ka:
		#print(i[3])
		#km.append(i[3])
	if (len(ka)>0):
		for i in ka:
			key_name = "key%d" %i[0]
			my_keys[key_name] = i[1]
			#print(i[0],i[1])
		print(my_keys)

		my_keypad = "KM" + str(TA)
		for i in ka:
			key_name = "key%d" % i[0]
			my_keypad += str(i[0])
			my_keypad += str(my_keys[key_name])
		my_keypad += "#"
		print("Final KEYPAD Config. result:", my_keypad)   # KM=keypad mapping TA=total arm ...11,22,33,44=(switchid,mapping id)        #HARSHAD
		#print(type(my_string))

		time.sleep(0.2)
		write_to_serial(my_keypad)  # KM=keypad mapping TA=total arm ...11,22,33,44=(switchid,mapping id)        #HARSHAD
		time.sleep(0.2)

		

def get_flag_reset():
	global get_flag
	t_end = time.time() + 10

	get = 0
	while (time.time() < t_end):
		get = get + 1
	get_flag = 0
	print("get flag done", get_flag)
	"""
	while (time.time() < t_end):
		try:
			#print("end time", t_end)
			# print("helloo")
			print("real time", time.time())
			if (time.time() == t_end):
				get_flag = 0
				#print("get flag done", get_flag)
				break
			#print("at END")
		except Exception as ex:
			print("get flag reset", ex)
			    """
#################################################################################################################  HARSHAD

def watchdog(serial_data):
	global previous_stage
	global stage_count
	global JOFF_flag
	#global serial_data
	print("previous_stage::::",previous_stage)
	if (serial_data[1] == "AQ" and HC_Flag==0 and JOFF_flag == 0):
		current_stage_1 = (int(serial_data[2])+1)
		print("current_stage_1:::",current_stage_1)
		current_mode_1 = int(serial_data[4])
		if(previous_stage == current_stage_1 and current_mode_1 != 5 and current_mode_1 != 10):    #mode 10 for manual mode run by police panel
			stage_count -= 1
			print("stage_count:",stage_count)
			if(stage_count == 0):														#07-02-2022
				print("xxxxxxx::: Sending reboot command to microcontroller :::xxxxxx")
				write_to_serial("reboot#")
				#stage_count = 17
				stage_count = 200    #HARSHAD
				
		else:
			#stage_count = 17
			stage_count = 200  # HARSHAD
		previous_stage = current_stage_1
	if (serial_data[1] == "AB"):
		stage_count = 7
		previous_stage = 0

def process_serial_data(serial_data,generation_time,generation_time_2):
	global OTA_flag 						#krusha
	# global OTA_msg							#krusha	
	# global OTA_string1
	# global OTA_string2
	# global OTA_string3

	# global serial_data
	global final_msg
	# global generation_time
	global event_type
	global no_of_parameter	
#---------Hurry Call , Junction On/Off, Flashing Amber ----------#
	global arm_no
	global status
	global JOFF_flag
	global prevous_sequence
	global temp_key_from_software
#-------------------RTC Sync and RTC Time Sync Update-------------#
	global rtc_time_diff_sign
	global rtc_set_time
	global rtc_time_from
	global system_time
	global stored_time
	global rtc_fail
	global attempt
	global system_date
#-------------------Stage Skip-----------------------------------#
	global next_stage
#-------------------Controller reboot----------------------------#
	global controller_reboot
#--------------------Power ON------------------------------------#
	global power_on
	global last_off_time	
#-------------------Stage Change---------------------------------#
	global current_seq_no
	global previous_stage_no
	global current_stage_no # Because stage comes from controllers starts from 0 thats why we've to add 1
	global mode_rcv
	global prv_mode
	global mod_flag
	global created_by
#-------------------Lamp Health----------------------------------#
	global lamp_health
	global lamp_intensity_1
	global prv_lamp_intensity_1
	global lamp_id
	global lamp_health_event_type
	global lamp_health_no_of_parameter
	global lamp_intensity
	global intensity_event
#-------------------Green Conflict--------------------------------#
	global lamptype_1
	global lampcode_1 
	global arm_1
	global lamptype_2
	global lampcode_2 	
	global arm_2
#-------------------Counter Health----------------------------------#
	global counter_health
	global counter_id
	global send_au
#--------------current operating parameter-----------------------#
	global current_zone
	global current_mode
	global corridor
	global total_stage
	global all_stage_time
	global current_cycle_time	
	
	global exe_status_flag
	print(serial_data)
	global HC_Flag
	global hcid
	global hcid1
	global killexe
	global count_num
	global raw_flag
	#------------------Debug Variables----------------------------# added by krusha
	global arm_id_1
	global arm_id_2
	global arm_id_3
	global arm_id_4
	global lamp_fb_1
	global re_seq_1
	global stage_no_1
	global mode_1
	global timer_count_1
	global time_bet_con_1
	global lamp_fb_2 
	global re_seq_2
	global stage_no_2 
	global mode_2 
	global timer_count_2
	global time_bet_con_2
	global lamp_fb_3
	global re_seq_3 
	global stage_no_3
	global mode_3
	global timer_count_3 
	global time_bet_con_3
	global lamp_fb_4
	global re_seq_4
	global stage_no_4 
	global mode_4 
	global timer_count_4
	global time_bet_con_4
	global priority_flag
	global cf_counter
#----------------------------------------Hurry Call-------------------------------------------------#
	if (serial_data[1] == "AA" and OTA_flag!= 1):																#krusha
		
		event_type = serial_data[1]
		arm_no = serial_data[2]
		status = serial_data[3]
		operated_from1 = (serial_data[4]) # From Hardware or software	0 form software 1 from hardware
		sql5 = "SELECT userid from atcs.eventwise_userid WHERE eventcode = 'AH' order by id desc limit 1 ;"  #changed for atcs user as required software team
		if(operated_from1=='1'):
			userid = '1'
		else:	
			userid=ReadDatabase(sql5)[0]
			print(str(userid[0]))

		if(int(status) == 1):

			HC_Flag = 1
			print("hurry call--->",HC_Flag)
			no_of_parameter = "009"
			if(operated_from1 == '1'):
				hcid = '0'
			else:
				# f = open("/home/atcs-02/Documents/ATCS/hcid",'r')
				hcid=read_file("/home/{}/Documents/ATCS/hcid1".format(device_name))
				print("hcid",hcid)
				#open("/home/{}/Documents/ATCS/hcid".format(device_name), 'w').close()
			
			final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + operated_from1  + "," +str(hcid)  + "," \
			+ arm_no + "," + status + ","
			
			sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
							requestreserverd1,requestreserverd2,requestarmno,requesteventstatus,isuploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

			if(int(current_mode) == 2 or int(current_mode) == 3):# Kill exe of valogic in VA mode so it could start from stage one after reset event.
				os.system("sudo killall -9 ATCS_GMC_NewVALogic")
				os.system("sudo killall -9 ATCS_GMC_NewVAWithBRTLogic") # Kill VA Exe if running.(mileen)
				exe_status_flag = 0
			print("exe_status:------------> ",exe_status_flag)

			if(current_seq_no != "1000000"):
				prevous_sequence = current_seq_no
				current_seq_no = "1000000"
			print("mode id--------",current_mode)
			print(final_msg)
			
			insert_raw_data(final_msg)

			# AA_string = final_msg
			try:
				print("calling from AA event")
				send_cycle_over_event()
				hcid1=hcid
				if(operated_from1=='1'):
					send_sequence_change_event(prevous_sequence,current_seq_no,current_mode,'-1')
				else:	
					send_sequence_change_event(prevous_sequence,current_seq_no,current_mode,userid[0])  ### Added by Amit 1_9_20
				post_online(url_events,final_msg,"eventstring")
				
			except Exception as e:
				print(e)
				WriteToDatabase(sql1,1, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,arm_no,bool(status),False)
		#---------- This is because software team will send unique key in against of each hurry call events which have to respond us during hurry call events--------------#
				sql2 = "SELECT eventlogid from atcs.eventlogs WHERE requesteventgeneratetimestamp = {}"
				temp_key_from_software = ReadDatabase(sql2.format(generation_time_2))#It will be unique for each hurrycall event in case of we're offine
																			#and we could not get temp key from API
		else:
			
			if(HC_Flag ==1) :
				print("hurry call--->",HC_Flag)
				print("hcid",hcid)
			HC_Flag=0
			atcs_exe_flag = 0
			print("atcs_exe_flag when hurry call is over", atcs_exe_flag)

			if(prevous_sequence != "1000000"):
				current_seq_no = prevous_sequence 
				
			if (len(temp_key_from_software) <= 0):
				no_of_parameter = "009"
				temp_key_from_software = "0"
				final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + str(userid[0]) + "," + str(hcid1) + "," + arm_no + "," + status + ","
			else :
				#no_of_parameter = "010"
				no_of_parameter = "009"
				final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + str(userid[0]) + "," + str(temp_key_from_software) + "," + arm_no + "," + status + ","
			print("number of para...",no_of_parameter)
			print("temp key...",temp_key_from_software)
			print("userid hc call",userid[0])
			print("final msg for hurry call", final_msg)

			
			sql1 = "UPDATE atcs.eventlogs SET requesteventendtimestamp_hurrycall = %s WHERE eventlogid = %s"			

			#print(final_msg)
			# AA_string = final_msg
			insert_raw_data(final_msg)

			try:
				post_online(url_events,final_msg,"eventstring")

				temp_key_from_software = ""
			except Exception as e:
				print(e)
				WriteToDatabase(sql1,time.strftime('%Y-%m-%d %H:%M:%S'),temp_key_from_software)
				
			print("exe_status:------------> ",exe_status_flag)			
			if(exe_status_flag == 0):
				time.sleep(9)
				threading.Thread(target=start_va_sva_logic,args=(int(current_mode),)).start()
				# threading.Thread(target=start_camera_raw_data).start()
				exe_status_flag = 1
				print("exe_status:",exe_status_flag)

#----------------------------------------Junction On/Off-------------------------------------------------#
	elif (serial_data[1] == "AB" and OTA_flag!= 1):						#krusha

		no_of_parameter = "009"
		event_type = serial_data[1]					
		status = serial_data[2]
		operated_from = serial_data[3] # From Hardware or software
		sql5 = "SELECT userid from atcs.eventwise_userid WHERE eventcode = 'AJ' order by id desc limit 1 ;"
		userid=ReadDatabase(sql5)[0]
		print(str(userid[0]))
		print(bool(status))
		global res_2 
		if(int(status) == 0):
			JOFF_flag = 0
		if(serial_data[4]=='2'):
			res_2 ='-1'
		else:
			res_2 ="000000000000"
		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + \
					str(userid[0]) + "," +res_2  + "," + status + "," + operated_from + ","
		
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
								requestreserverd1,requestreserverd2,requesteventstatus,requestjunctiononofffrom,isuploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                

		print(final_msg)
		insert_raw_data(final_msg)
		try:    
			post_online(url_events,final_msg,"eventstring")
                        
		except Exception as e:
			print("Exception got here",e)
			WriteToDatabase(sql1,2, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,\
							reserved_1,reserved_2,status,int(operated_from),False)

		if(int(status) == 1):
			JOFF_flag = 1
			if(int(current_mode) == 2 or int(current_mode) == 3):
				#os.system("sudo killall -9 ATCS_GMC_NewVALogic")
				#os.system("sudo killall -9 ATCS_GMC_NewVAWithBRTLogic") # Kill VA Exe if running.(mileen)
				exe_status_flag = 0

		# elif (int(status) == 0):
		# 	print("exe_status in AB:------------> ", final_msg)
		#
		# 	exe_status_flag = 1
		# 	time.sleep(2)
		# 	threading.Thread(target=start_va_sva_logic, args=(int(current_mode),)).start()
		# 	time.sleep(2)

		elif(exe_status_flag == 0):
			print("exe_status in AB:------------> ",final_msg)
			exe_status_flag = 1
			time.sleep(2)
			threading.Thread(target=start_va_sva_logic,args=(int(current_mode),)).start()
			time.sleep(2)

			print(final_msg)
			# AB_string = final_msg
		# f = open("/home/atcs-02/Documents/ATCS/mode",'w')
		# f.write('5')
		# f.close()
		write_to_file("/home/{}/Documents/ATCS/mode".format(device_name),'5')




#----------------------------------------Flashing Amber-------------------------------------------------#
	elif (serial_data[1] == "AC" and OTA_flag!= 1):								#krusha

		no_of_parameter = "008"
		event_type = serial_data[1]					
		status = serial_data[2]

		if(serial_data[2] == '1'):
			send_au = 1
		elif(serial_data[2] == '0'):
			send_au = 0 

		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2  + "," + status + ","
		
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
								requestreserverd1,requestreserverd2,requesteventstatus,isuploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		print(final_msg)
		insert_raw_data(final_msg)
		# AC_string = final_msg
		## To send sequence change event when operated from police panel.
		try:
			print("Sending AC Event:::")
			prevous_sequence = current_seq_no
			print("Sending AC Event",final_msg)
			# time.sleep(2)
			post_online(url_events,final_msg,"eventstring")
			time.sleep(1)
			send_sequence_change_event(prevous_sequence,"8888888",5,"-1")  
			
			threading.Thread(target=send_au_during_blinker).start()
		except Exception as e:
			print(e)
			WriteToDatabase(sql1,3, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,bool(status),False)

		if(int(status) == 1):
			if(int(current_mode) == 2 or int(current_mode) == 3):
				os.system("sudo killall -9 ATCS_GMC_NewVALogic")
				os.system("sudo killall -9 ATCS_GMC_NewVAWithBRTLogic") # Kill VA Exe if running.(mileen)
				exe_status_flag = 0
		elif(exe_status_flag == 0):
			exe_status_flag = 1
			time.sleep(2)
			threading.Thread(target=start_va_sva_logic,args=(int(current_mode),)).start()


#----------------------------------------RTC Sync-------------------------------------------------#
	elif (serial_data[1] == "AD" and OTA_flag!= 1):									#krusha

		no_of_parameter = "010"
		event_type = serial_data[1]					
		status = serial_data[2]

		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2  + "," + status + "," + rtc_time_diff_sign + "," + rtc_set_time + ","
		
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
								requestreserverd1,requestreserverd2,requesteventstatus,requestrtctimedifference,requestrtcoutofsyncimestamp,isuploaded) \
								VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		print(final_msg)
		insert_raw_data(final_msg)
		# AD_string = final_msg
		try:
			post_online(url_events,final_msg,"eventstring")
		except Exception as e:
			print(e)
			WriteToDatabase(sql1,4, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,status,rtc_time_diff_sign,rtc_set_time,False)

#----------------------------------------RTC Time Sync Update-------------------------------------------------#
	elif (serial_data[1] == "AF" and OTA_flag!= 1):									#krusha

		no_of_parameter = "010"
		formatt = "%Y-%m-%d %H:%M:%S"
		event_type = serial_data[1]					
		hour_from_controller = format_byte(serial_data[2],2)+":"+format_byte(serial_data[3],2)+":"+format_byte(serial_data[4],2)
		d1 = time.strftime("%Y-%m-%d ")+hour_from_controller
		d2 = time.strftime(formatt)
		# rtc_set_date_time = str(int(time.strftime("%Y%m%d%H%M%S"))-int(time.strftime("%Y-%m-%d ")+hour_from_controller))
		rtc_set_date_time = str(datetime.datetime.strptime(d1,formatt)-datetime.datetime.strptime(d2,formatt))
		if(rtc_set_date_time[0:1] == '-'):# For extracting +/- from above difference
			rtc_time_diff_sign = '-' 
			rtc_set_time = rtc_set_date_time[-8:] # Just extracting HH:MM:SS
		else:
			rtc_time_diff_sign = '+'
			rtc_set_time = rtc_set_date_time[-8:]
		rtc_time_from = serial_data[5]
		# time.strftime("%d%m%Y")+"152451" [u'$', u'AF', u'19', u'1', u'39', u'1', u'#\n']
		if (rtc_set_time == ''):
			rtc_set_time = d2  # added by udgish

		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2  + "," + rtc_time_diff_sign + "," + rtc_set_time + "," + rtc_time_from + ","
		
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
								requestreserverd1,requestreserverd2,requestrtctimedifference,requestrtcsettimestamp,requstrtcsettimefrom,isuploaded) \
								VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		
		junction_time = time.strftime('%d %b %Y %H:%M:%S',time.strptime(d2,formatt))
		print(junction_time)
		# os.system("date -s '{}'".format(junction_time))
		print(final_msg)
		insert_raw_data(final_msg)
		# AF_string = final_msg
		try:
			post_online(url_events,final_msg,"eventstring")
		except Exception as e:
			print(e)
			WriteToDatabase(sql1,6, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,rtc_time_diff_sign,rtc_set_time,rtc_time_from,False)

#--------------------------------- RTC failure Event -----------------------------------------------------#

		# f = open("/home/atcs-02/Documents/ATCS/RTC_Time",'w')
		# f.write(hour_from_controller)
		# f.close()
		write_to_file("/home/{}/Documents/ATCS/RTC_Time".format(device_name),hour_from_controller)
		print("Controller time----", hour_from_controller)
		system_time = time.strftime("%H:%M:%S")
		system_date = time.strftime('%Y%m%d')
		print("system time------", system_time)
		# f1 = open("/home/atreyo-atcs14/Documents/ATCS/RTC_Time",'r')
		stored_time = read_file("/home/{}/Documents/ATCS/RTC_Time".format(device_name))
		# f1.close()
		if(system_time == stored_time):
			# f = open("/home/atreyo-atcs14/Documents/ATCS/RTC",'w')
			# f.write(0)
			# f.close()
			write_to_file("/home/{}/Documents/ATCS/RTC".format(device_name),0)
		elif(system_time != stored_time):
			if(stored_time[:2] > system_time[:2] or stored_time[:2] < system_time[:2]): # or (stored_time[3:5] > system_time[3:5] or stored_time[3:5] < system_time[3:5])):
				# f = open("/home/atreyo-atcs14/Documents/ATCS/RTC",'w')
				# f.write("BA")
				# f.close()
				write_to_file("/home/{}/Documents/ATCS/RTC".format(device_name),"BA")
				attempt += 1
				print("mismatch detected----", attempt)
		# f = open("/home/atreyo-atcs14/Documents/ATCS/RTC",'r')
		rtc_fail = read_file("/home/{}/Documents/ATCS/hcid".format(device_name))
		# f.close()

		if(rtc_fail == "BA" and attempt == 2):
			no_of_parameter = "008"
			event_type = "BA"
			attempt = 0
			stored_time = stored_time.replace(":","")
			final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + system_date + stored_time + "," + reserved_1 + "," +reserved_2  + ","
			print(final_msg)
			insert_raw_data(final_msg)
			# BA_string = final_msg
			sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
								requestreserverd1,requestreserverd2,requestrtcfailtime,isuploaded) \
								VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			try:
				post_online(url_events,final_msg,"eventstring")
			except Exception as e:
				print(e)
				WriteToDatabase(sql1,20,controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,stored_time,False)
		


#----------------------------------------Stage Skip-------------------------------------------------#
	elif (serial_data[1] == "AG" and OTA_flag!= 1):

		no_of_parameter = "010"
		event_type = serial_data[1]
		# current_seq_no = str(serial_data[2])
		current_stage_no = str(int(serial_data[3])+1)# Because stage comes from controllers starts from 0 thats why we've to add 1
		next_stage = str(serial_data[4])
		
		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2  + "," \
		+ current_seq_no + "," + current_stage_no + "," + next_stage + ","
		
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
											requestreserverd1,requestreserverd2,requestcurrentsequenceno,requestcurrentstageno,requestnextstageno,isuploaded)\
											VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		print(final_msg)
		insert_raw_data(final_msg)
		# AG_string = final_msg
		try:
			post_online(url_events,final_msg,"eventstring")
		except Exception as e:
			print(e)
			WriteToDatabase(sql1,7, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,current_seq_no,current_stage_no,next_stage,False)


#----------------------------------------Controller Reboot-------------------------------------------------#
	elif (serial_data[1] == "AI" and OTA_flag!= 1):

		no_of_parameter = "008"
		event_type = serial_data[1]					
		controller_reboot = serial_data[2]

		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2  + "," + controller_reboot + ","
		insert_raw_data(final_msg)
		
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
								requestreserverd1,requestreserverd2,requestisreboot,isuploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		try:
			post_online(url_events,final_msg,"eventstring")
			# AI_string = final_msg
		except Exception as e:
			print(e)
			WriteToDatabase(sql1,9, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,controller_reboot,False)

#----------------------------------------Power ON-------------------------------------------------#
	elif (serial_data[1] == "AJ" and OTA_flag!= 1):

		no_of_parameter = "009"
		event_type = serial_data[1]					
		power_on = str(int(serial_data[2]))
		last_off_time = time.strftime('%d%m%Y%H%M%S')

		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2  + "," + power_on + "," + last_off_time + ","
		
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
								requestreserverd1,requestreserverd2,requestispoweron,requestlastcontrollerofftime,isuploaded) \
								VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		print(final_msg)
		insert_raw_data(final_msg)
		# AJ_string = final_msg
		try:
			post_online(url_events,final_msg,"eventstring")
		except Exception as e:
			print(e)
			WriteToDatabase(sql1,10, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,power_on,last_off_time,False)

#------------------------------Exceptional Mode Change ------------------------------------------------#
	elif (serial_data[1] == "AK" and OTA_flag!= 1):
		
		prevous_mode = serial_data[2]
		current_mode = serial_data[3]
		if(serial_data[4]=='1'):
			send_mode_change_event(prevous_mode,current_mode,'-1')
		else:
		    send_mode_change_event(prevous_mode,current_mode,created_by)
				
		
#----------------------------------------Stage Change-------------------------------------------------#
	elif (serial_data[1] == "AN" and OTA_flag!= 1):
		
		no_of_parameter = "011"
		event_type = serial_data[1]
		# current_seq_no = str(serial_data[2])

		if(int(serial_data[3])):
			#print("serial data----",int(serial_data[3]))
			previous_stage_no = str(int(serial_data[3]))
		else:
			previous_stage_no = str(total_stage)
		
		current_stage_no = str(int(serial_data[3])+1)# Because stage comes from controllers starts from 0 thats why we've to add 1
		mode_rcv = str(int(serial_data[4]))
		#final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2  + "," \
		#+ str(current_seq_no) + "," + previous_stage_no + "," + current_stage_no + ","
		
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
											requestreserverd1,requestreserverd2,requestcurrentsequenceno,requestpreviousstageno,requestcurrentstageno,isuploaded,effectivegreenjson)\
											VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		sql2 = "INSERT INTO atcs.cycleydata (sequenceid,stageid,stagedatetime) VALUES (%s,%s,%s)"
		WriteToDatabase(sql2,str(current_seq_no),current_stage_no,generation_time_2)
		
		sql3 = "select * from atcs.sp_get_effective_green('ref');fetch all in \"ref\";"
		b = ReadDatabase(sql3)

		sql8="SELECT stageid,(select stagedatetime from atcs.cycleydata order by id desc offset 1 limit 1) as fromtime,stagedatetime as totime from atcs.cycleydata order by id desc limit 1;"
		d = ReadDatabase(sql8)
		print(d)
		rcv_stgid = d[0][0]
		fromtime1 = d[0][1]
		totime1   = d[0][2]

		if(rcv_stgid==current_stage_no):
			sql6 = "SELECT * from atcs.sp_get_saturationindex_report('ref1','{}','{}');fetch all in \"ref1\";" #query for saturation index added 20/5/2020 udgish
			saturationind = ReadDatabase(sql6.format(fromtime1,totime1))[0][0] #added sa
		else:
			saturationind = '0'

		#global resdte
		if(len(b) > 0):
			
			for row in b:
				res_temp = {}
				res_temp["armid"] = row[0] # {"result": [{"armid": 1, "pcuinred": 123.0, "pcuinlasthorizon": 204.0, "redphaseseconds": 171}]}
				res_temp["effectivegreen"] = row[1]
				res_temp["actualgreen"] = row[2]
				res_temp["pcu"] = row[3]
				res_temp["stageno"]= row[4]
				res_temp["stagetime"]= row[5]
				res_temp["corid"]= row[6]
				res_temp["corstream"]= row[7] 
				res_temp["dos"]= row[8]
			
			print("---------------Effective Green Data-------------- \n" +json.dumps(res_temp) + " \n --------------------")
			c = json.dumps(res_temp)
		else:
			c = "{}"
				
		if(count_num == 1):
			count_num = 2
		
		final_msg = "$" + controller_id + "," + generation_time + "," + "AN" + "," + no_of_parameter + "," + mode_rcv + "," +saturationind + "," \
		+ str(current_seq_no) + "," + previous_stage_no + "," + current_stage_no + "," + c.replace(",", ";") + ","
		print(final_msg)
		insert_raw_data(final_msg)
		# AN_string = final_msg
		try:
			post_online(url_events,final_msg,"eventstring")
		except Exception as e:
			print(e)
			WriteToDatabase(sql1,14, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,current_seq_no,previous_stage_no,current_stage_no,False,c)

#----------------------------------------Lamp Health-------------------------------------------------#
	elif (serial_data[1] == "AO" and OTA_flag!= 1):					#krusha

		lamp_ids = read_lamp_ids_from_db()
		lamp_health_no_of_parameter = "012"
		lamp_health_event_type = serial_data[1]		
		# lamp_health = serial_data[2]
		j = 2 # for offset in serial data i.e. the lamp health will start from index 2
		lamp_intensity = serial_data[-3]
		arm_no = serial_data[-2]
		#lamp_health = serial_data[2]
		for i in range(len(lamp_ids)):
			lamp_id = str((lamp_ids[i]))
			print("lamp id--------",lamp_id)
			#sql11= "SELECT lamptype from atcs.lamp_master where lampcode = lamp_id;"
			sql11=("SELECT lamptype from atcs.lamp_master where lampcode= '{}' ".format(lamp_id))
			#sql11 = "SELECT lampcode from atcs.lamp_master where lamptype='9' AND slavecode = (select slavecode from atcs.slave_master where armno='4');"
			lamp_sign = ReadDatabase(sql11)[0][0]
			print("Lamp sign ------------",lamp_sign)
			lamp_health = serial_data[j]
			print("lamp_health------",lamp_health)
			if(int(serial_data[4]) == int(lamp_sign)):					#krusha
				final_msg = "$" + controller_id + "," + generation_time + "," + lamp_health_event_type + "," + lamp_health_no_of_parameter + "," + current_stage_no + "," + str(current_seq_no)  + "," \
				+ lamp_health + "," + lamp_intensity + "," + arm_no + "," + str(lamp_sign)+ ","+lamp_id +"," 
				
				sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
													requestreserverd1,requestreserverd2,requestlamhealth,requestlampintensity,requestarmno,requestlamptrafficsign,isuploaded)\
													VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

				print(final_msg)
				AO_string = final_msg
				try:
					post_online(url_events,final_msg,"eventstring")
				except Exception as e:
					print(e)
					WriteToDatabase(sql1,15, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),lamp_health_no_of_parameter,reserved_1,reserved_2,lamp_health,lamp_intensity,arm_no,lamp_id,False)


#----------------------------------------Counter Health-------------------------------------------------#
	elif (serial_data[1] == "AP" and OTA_flag!= 1 and int(current_mode) != 5):

		no_of_parameter = "009"
		event_type = serial_data[1]
		counter_health = serial_data[2]
		counter_id = serial_data[3]
		
		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2  + "," \
		+ counter_health + "," + counter_id + ","
		
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
											requestreserverd1,requestreserverd2,requestcounterhealth,requestcounterid,isuploaded)\
											VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		print(final_msg)
		insert_raw_data(final_msg)
		# AP_string = final_msg
		try:
			post_online(url_events,final_msg,"eventstring")
		except Exception as e:
			print(e)
			WriteToDatabase(sql1,16, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,counter_health,counter_id,False)

#----------------------------------------Arm Health-------------------------------------------------#
	elif (serial_data[1] == "AR" and OTA_flag!= 1 and int(current_mode) != 5):
		global ar_flag 
		ar_flag = 1
		print("ar_flag is.........",ar_flag)
		no_of_parameter = "010"
		event_type = serial_data[1]
		status = serial_data[2]
		arm_no = serial_data[3]
		slave_code = ReadDatabase("SELECT slavecode FROM atcs.slave_master WHERE armno = {}".format(int(arm_no)))[0][0]
		
		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2 + "," \
		+ status + "," + arm_no + "," + slave_code + ","
		
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
						requestreserverd1,requestreserverd2,requesteventstatus,requestarmno,requestslavecode,isuploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		print(final_msg)
		insert_raw_data(final_msg)
		# AR_string = final_msg
		# f = open("/home/atreyo-atcs14/Documents/ATCS/mode",'w')
		# f.write('5')
		# f.close()
		write_to_file("/home/{}/Documents/ATCS/mode".format(device_name),'5')
		try:
			post_online(url_events,final_msg,"eventstring")   ####Commented by udgish 5 jan for testing
			if(count_num == 0):
				count_num = 1
				if(count_num == 1):
					print("Conter inside------",count_num)
					time.sleep(.5)
					send_mode_change_event(modeid,5,"-1")
					time.sleep(.5)
					prevous_sequence = current_seq_no
					print("------Previous sequence is:----",prevous_sequence)
					send_sequence_change_event(prevous_sequence,"8888888",5,"-1")
					time.sleep(.5)
				
		except Exception as e:
			print(e)
			WriteToDatabase(sql1,18, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,bool(status),arm_no,slave_code,False)
		print("Conter outside------",count_num)
		
##----------------------------Intensity Change Event -----------------------##

	elif (serial_data[1] == "AV" and OTA_flag!= 1):
		raw_flag += 1
		no_of_parameter = "008"
		event_type = serial_data[1]
		lamp_intensity = serial_data[2]
		if serial_data[2] == "1":
			lamp_intensity_1 = '75'
			prv_lamp_intensity_1 = '100'
			raw_data = "3300"
		elif serial_data[2] == "2":
			lamp_intensity_1 = '100'
			prv_lamp_intensity_1 = '75'
			raw_data = "3850"
		#counter_id = serial_data[3]
		# f = open("/home/atreyo-atcs14/Documents/ATCS/Intensity_Event",'r')
		intensity_event = read_file("/home/{}/Documents/ATCS/Intensity_Event".format(device_name))
		# f.close()
		
		# f = open("/home/atreyo-atcs14/Documents/ATCS/Intensity_Event",'w')
		# f.write(serial_data[2])
		# f.close()
		write_to_file("/home/{}/Documents/ATCS/Intensity_Event".format(device_name),lamp_intensity)
		
		if raw_flag == 2:
			final_msg = "$" + controller_id + "," + generation_time + "," + "BB" + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2  + "," \
			+ raw_data + ","
			print(final_msg)
			insert_raw_data(final_msg)
			# AB_string = final_msg
			try:
				post_online(url_events,final_msg,"eventstring")
				raw_flag = 0
			except Exception as e:
				print(e)
		
		if (intensity_event != serial_data[2]):
			final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + prv_lamp_intensity_1 + "," +reserved_2  + "," \
			+ lamp_intensity_1 + "," 
			
			sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
												requestreserverd1,requestreserverd2,requestlamp_intensity,isuploaded)\
												VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

			print(final_msg)
			insert_raw_data(final_msg)
			# AV_string = final_msg
			try:
				post_online(url_events,final_msg,"eventstring")
			except Exception as e:
				print(e)
				WriteToDatabase(sql1,19,controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,lamp_intensity_1,False)

#-------------------------------Conflict hardware-New development 2/6/2020 by udgish---------------------------------------------------------#

	elif (serial_data[1] == "AY" and OTA_flag!= 1):

		no_of_parameter = "009"
		event_type = serial_data[1]
		
		lamptype_1 =  serial_data[2]
		arm_1 = serial_data[3]
		
		lamptype_2 =  serial_data[4]
		arm_2 = serial_data[5]
		
		#slave_code = ReadDatabase("SELECT slavecode FROM atcs.slave_master WHERE armno = {}".format(int(arm_no)))[0][0]
		lampcode_1 = ReadDatabase("SELECT lampcode from atcs.lamp_master where lamptype='{}' AND slavecode = (select slavecode from atcs.slave_master where armno='{}')".format(int(lamptype_1),int(arm_1)))[0][0]
		print("lampcode_1----------",lampcode_1)
		lampcode_2 = ReadDatabase("SELECT lampcode from atcs.lamp_master where lamptype='{}' AND slavecode = (select slavecode from atcs.slave_master where armno='{}')".format(int(lamptype_2),int(arm_2)))[0][0]
		print("lampcode_2----------",lampcode_2)
		
		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2 + "," \
		+ lampcode_1 + "," + lampcode_2 + ","
		
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
												requestreserverd1,requestreserverd2,requestlampcode_1,requestlampcode_2,isuploaded)\
												VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		print(final_msg)
		insert_raw_data(final_msg)
		# AY_string = final_msg
		# f = open("/home/atreyo-atcs14/Documents/ATCS/mode",'w')
		# f.write('5')
		# f.close()
		write_to_file("/home/{}/Documents/ATCS/mode".format(device_name),'5')
		try:
			post_online(url_events,final_msg,"eventstring")
			if(count_num == 0):
				count_num = 1
				if(count_num == 1):
					print("Conter inside------",count_num)
					time.sleep(.5)
					send_mode_change_event(modeid,5,"-1")
					time.sleep(.5)
					prevous_sequence = current_seq_no
					print("------Previous sequence is:----",prevous_sequence)
					send_sequence_change_event(prevous_sequence,"8888888",5,"-1")
					time.sleep(.5)
		except Exception as e:
			print(e)
			WriteToDatabase(sql1,20,controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,lampcode_1,lampcode_2,False)
			
#---------------------------Output short circuit -------------------------------------#
			
	elif (serial_data[1] == "AZ" and OTA_flag!= 1):

		no_of_parameter = "009"
		event_type = serial_data[1]
		shortcircuit =  serial_data[2]
		arm_id = serial_data[3]
		mode_rcv = str(int(serial_data[4]))
		print("Mode Received-------",)
		#slave_code = ReadDatabase("SELECT slavecode FROM atcs.slave_master WHERE armno = {}".format(int(arm_no)))[0][0]
		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + mode_rcv + "," +reserved_2 + "," \
		+ shortcircuit + "," + arm_id + ","
		
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
						requestreserverd1,requestreserverd2,requestshortcircuit,requestarm_id,requestmode_rcv,isuploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		print(final_msg)
		insert_raw_data(final_msg)
		# AZ_string = final_msg
		try:
			post_online(url_events,final_msg,"eventstring")
		except Exception as e:
			print(e)
			WriteToDatabase(sql1,21,controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,shortcircuit,arm_id,mode_rcv,False)

#----------------------------------------Current Operating-------------------------------------------------#
	elif (serial_data[1] == "AQ" and OTA_flag!= 1):
		no_of_parameter = "013"
		event_type = serial_data[1]
		current_stage_no = str(int(serial_data[2])+1) # Because stage comes from controllers starts from 0 thats why we've to add 1
		# current_cycle_time = str(serial_data[4])
		current_mode = str(serial_data[4])
	#--- to format string "$08008003008003008003008003#" into ["$08","008","003","008","003","008","003","008","003","#"]
		all_stage_time = [msg_stage_timing[i:i+3] for i in range(0,len(msg_stage_timing),3)]
		current_cycle_time = int(all_stage_time[1])
		all_stage_time_str = str(all_stage_time[1])
		for i in range(2,len(all_stage_time)): # iterate from 2nd element because we've already first element above.
			if(all_stage_time[i] != '#'):
				current_cycle_time += int(all_stage_time[i])
				all_stage_time_str += ("," + str(all_stage_time[i]))
		print("Enter in current_mode :1......",prev_known_fixed_seq)
		if(HC_Flag==1):
			current_seq_no = "1000000"
			current_stage_no = "3"
		else:
			if(current_mode == '1'):                    #changed by ud 5/08
				if(prev_known_fixed_seq == '8888888' or prev_known_fixed_seq == '9999999'):
					current_seq_no = read_seq()
					print("current_seq_no......... after reading database",current_seq_no)
				else:
					print("enter in else condition of mode:1.............")
					current_seq_no  = prev_known_fixed_seq  #changed by ud 5/08
				print("Enter in current_mode :1......",prev_known_fixed_seq)
			if(current_mode == '2' or current_mode =='3' or current_mode =='4' or current_mode == '6' or current_mode == '7'):
				current_seq_no = read_seq() #added for va 16stage (mileen)
				print("Enter in current_mode :2......")
			if((current_mode == '5')):
				current_seq_no = "8888888"
				print("Enter in current_mode :5......")	
		
		# final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2  + "," \
		# + current_mode + "," + corridor + "," + str(current_seq_no) + "," + str(current_stage_no) + "," + str(current_cycle_time) + "," + time.strftime('%d%m%Y%H%M%S') + '@' + all_stage_time[1] + "," + all_stage_time[3] \
		# + "," + all_stage_time[5] + "," + all_stage_time[7] + '#'

		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2  + "," \
		+ current_mode + "," + corridor + "," + str(current_seq_no) + "," + str(current_stage_no) + "," + str(current_cycle_time) + "," + time.strftime('%d%m%Y%H%M%S') + '@' + all_stage_time_str + '#'
		
		sql1 = "INSERT INTO atcs.currentoperatinglogs ( eventid , requestcontrollerid , requesteventgeneratetimestamp , requesteventsendtimestamp,requestpacketparameterno,\
											requestreserverd1,requestreserverd2,requestcurrentzone,requestcurrentmodeid,requestadaptivecoridor,requestcurrentsequence, \
											requestcurrentcycletime,status,isuploaded) \
											VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"#(17, controller_id,generation_time,time.strftime('%d%m%Y%H%M%S'),\
											#no_of_parameter,reserved_1,reserved_2,current_zone,current_mode,corridor,current_seq_no,current_cycle_time,1)
		log ="SELECT max(logid) from atcs.currentoperatinglogs "
		logid1 = ReadDatabase(log.format(0,date.today())) 
		print(logid1)
		logid = logid1[0]

		sql2 = "INSERT INTO atcs.currentoperatingstagelogs ( requeststagewisetime, status, createdon, isuploaded,logid) VALUES (%s,%s,%s,%s,%s)"

		print(final_msg)
		# AQ_string = final_msg

		insert_raw_data(final_msg)

		try:
			post_online(url_current_operating,final_msg,"eventstring")
		except Exception as e:
			print(e)
			
			WriteToDatabase(sql1, 17, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,current_zone,current_mode,corridor,current_seq_no,current_cycle_time,True,False)
			
			for i in range(1,len(all_stage_time)-1): # write individual stage time in database.
				WriteToDatabase(sql2, all_stage_time[i], True, generation_time_2,False,logid)
				# WriteToDatabase(sql2, ",".join(all_stage_time)[4:-2], True, generation_time_2,False)
#-----------------------------------Light status received from slave---------------------------#added by krusha 4/1/22
	elif(serial_data[1] == "AW"):
		if(int(serial_data[3]) == 0):
			AWFB_string = time.strftime('%d-%m-%Y %H:%M:%S') + "\t Feedback Data\t:\t" + str(serial_data[2])
			print(AWFB_string)
		elif(int(serial_data[3]) == 1):
			AWS_string = time.strftime('%d-%m-%Y %H:%M:%S') + "\tSignal Data\t:\t" + str(serial_data[2])
			print(AWS_string)

#---------------------------------Debug Variable received from Slave--------------------------#added by krusha on 4/1/22
	elif(serial_data[1] == "AX"):
		#   for conflict detection             sequence_for_conflict
		arm_ID = int(serial_data[2])
		mode_ID = int(serial_data[5])
		stage_NO = int(serial_data[6])
		received_conf=str(serial_data)

		#print(binary)
		#print(binary1[0])
		if(mode_ID == 1):
			#green strait comparision
			conflict_num = int(serial_data[3])
			binary = bin(conflict_num)
			binary1 = binary[2:]
			total_STAGE = (len(sequence_for_conflict)) / int(TA)
			if(stage_NO!=0):
				seq_no=((((stage_NO)*int(TA))+arm_ID)-1)-int(TA)
			else:
				seq_no=(((total_STAGE-1)*int(TA))+arm_ID)-1

			a1 = sequence_for_conflict[seq_no]
			amber_con = 0
			red_con = 0
			through_con = 0
			right_con = 0
			brts_st = 0
			brts_g0 = 0
			if (int(a1[3]) != int(binary1[-5])):
				#print("conflict ember")
				amber_con = 1
			if (int(a1[2]) != int(binary1[-4])):
				#print("conflict red")
				red_con = 1
			if (int(a1[6]) != int(binary1[-1])):
				#print("conflict through")
				through_con = 1
			if(amber_con==1 or red_con==1 or through_con==1):
				d_con_qur = "DELETE from atcs.conflict_detact WHERE created_on < (now() - interval '5 minutes')"
				#WriteToDatabase(d_con_qur)
				conflic_qurry = "INSERT INTO atcs.conflict_detact(arm_id, stage_no, red, amber, green_straight, green_rigjht, brts_stop, brts_go, created_on,received_string,sequence_1)VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				#WriteToDatabase(conflic_qurry, str(arm_ID), str(stage_NO), str(red_con), str(amber_con), str(through_con),str(right_con), str(brts_st), str(brts_g0), str(time.strftime('%Y-%m-%d %H:%M:%S')),received_conf,str(a1))
				amber_con = 0
				red_con = 0
				through_con = 0
				right_con = 0
				brts_st = 0
				brts_g0 = 0


		if(int(serial_data[9]) == 1):
			arm_id_1 = 1
			lamp_fb_1 = serial_data[2]
			re_seq_1 = serial_data[3]
			stage_no_1 = serial_data[4]
			mode_1 = serial_data[5]
			timer_count_1 = serial_data[6]
			time_bet_con_1 = serial_data[7]	
		elif(int(serial_data[9]) == 2):
			arm_id_2 = 2
			lamp_fb_2 = serial_data[2]
			re_seq_2 = serial_data[3]
			stage_no_2 = serial_data[4]
			mode_2 = serial_data[5]
			timer_count_2 = serial_data[6]
			time_bet_con_2 = serial_data[7]
		elif(int(serial_data[9]) == 3):
			arm_id_3 = 3
			lamp_fb_3 = serial_data[2]
			re_seq_3 = serial_data[3]
			stage_no_3 = serial_data[4]
			mode_3 = serial_data[5]
			timer_count_3 = serial_data[6]
			time_bet_con_3 = serial_data[7]
		elif(int(serial_data[9]) == 4):
			arm_id_4 = 4
			lamp_fb_4 = serial_data[2]
			re_seq_4 = serial_data[3]
			stage_no_4 = serial_data[4]
			mode_4 = serial_data[5]
			timer_count_4 = serial_data[6]
			time_bet_con_4 = serial_data[7]
		
		print("Time Stamp for Debug output:\t\t",time.strftime('%Y-%m-%d %H:%M:%S'))
		print("Arm Number:\t\t\t\t\t"+	str(arm_id_1) + "\t" + str(arm_id_2) + "\t" + str(arm_id_3) + "\t" + str(arm_id_4))
		print("Lamp Feedback:\t\t\t\t\t" + lamp_fb_1 + "\t" + lamp_fb_2 + "\t" + lamp_fb_3 + "\t" + lamp_fb_4 )
		print("Received Sequence:\t\t\t\t" + re_seq_1 + "\t" + re_seq_2 + "\t" + re_seq_3 + "\t" + re_seq_4)
		print("Stage number:\t\t\t\t\t" + stage_no_1 + "\t" + stage_no_2 + "\t" + stage_no_3 + "\t" + stage_no_4)
		print("Mode:\t\t\t\t\t\t" + mode_1 + "\t"  + mode_2 + "\t"  + mode_3 + "\t"  + mode_4)
		print("Timer Count:\t\t\t\t\t" + timer_count_1 + "\t" + timer_count_2 + "\t" + timer_count_3 + "\t" + timer_count_4)
		print("Time between 2 consecutive:\t\t\t" + time_bet_con_1 + "\t" + time_bet_con_2 + "\t" + time_bet_con_3 + "\t" + time_bet_con_4)


	# else:
		# continue
		# try:
		# 	#while (OTA_flag == 1):
		# 	#time.sleep(3)
		# 	OTA_msg = OTA_string_1 + generation_time + OTA_string_2 + time.strftime('%d%m%Y%H%M%S') + OTA_string_3	
		# 	post_online(url_events,OTA_msg,"eventstring")
		# 	print(OTA_msg)
		# 	print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
		# except Exception as e:
		# 	print(e)
	elif (serial_data[1] == "BX"):
		event_type = serial_data[1]
		reset_cause = serial_data[2]
		master_pcb_voltage = serial_data[3]
		packet_send_arm1 = int(serial_data[4])
		packet_rece_arm1 = int(serial_data[5])
		packet_send_arm2 = int(serial_data[6])
		packet_rece_arm2 = int(serial_data[7])
		packet_send_arm3 = int(serial_data[8])
		packet_rece_arm3 = int(serial_data[9])
		packet_send_arm4 = int(serial_data[10])
		packet_rece_arm4 = int(serial_data[11])
		packet_send_arm5 = int(serial_data[12])
		packet_rece_arm5 = int(serial_data[13])
		packet_send_arm6 = int(serial_data[14])
		packet_rece_arm6 = int(serial_data[15])
		core_temp = serial_data[16]
		light_feedback_1 = serial_data[17]
		light_feedback_2 = serial_data[18]
		light_feedback_3 = serial_data[19]
		light_feedback_4 = serial_data[20]
		light_feedback_5 = serial_data[21]
		light_feedback_6 = serial_data[22]
		light_sc_1 = serial_data[23]
		light_sc_2 = serial_data[24]
		light_sc_3 = serial_data[25]
		light_sc_4 = serial_data[26]
		light_sc_5 = serial_data[27]
		light_sc_6 = serial_data[28]
		# print(reset_cause)
		#print(master_pcb_voltage)
		#print(packet_send_arm1)
		#print(packet_rece_arm1)
		#print(packet_send_arm2)
		#print(packet_rece_arm2)
		#print(packet_send_arm3)
		#print(packet_rece_arm3)
		#print(packet_send_arm4)
		#print(packet_rece_arm4)
		#print(packet_send_arm5)
		#print(packet_rece_arm5)
		#print(packet_send_arm6)
		#print(packet_rece_arm6)
		#print(core_temp)
		#print(light_feedback_1)
		#print(light_feedback_2)
		#print(light_feedback_3)
		#print(light_feedback_4)
		#print(light_feedback_5)
		#print(light_feedback_6)

		a = "arm_packet_perc"
		b = 1
		for i in range(4, 15, 2):
			if (int(serial_data[i]) != 0):
				globals()[a + str(b)] = (int(serial_data[i + 1]) * 100) / int(serial_data[i])
			else:
				globals()[a + str(b)] = None
			b = b + 1

		#  arm_packet_perc1     variable format
		#print("arm_packet_perc1 =", arm_packet_perc1)
		#print("arm_packet_perc2 =", arm_packet_perc2)
		#print("arm_packet_perc3 =", arm_packet_perc3)
		#print("arm_packet_perc4 =", arm_packet_perc4)
		#print("arm_packet_perc5 =", arm_packet_perc5)
		#print("arm_packet_perc6 =", arm_packet_perc6)

		cause_list = ["LOW POWER RESET", "WINDOW WATCHDOG RESET", "INDEPENDENT WATCHDOG RESET", "SOFTWARE RESET",
					  "POWER ON/DOWN RESET (POR/PDR)", "EXTERNAL RESET PIN RESET", "BROWNOUT RESET", "UNKNOWN"]
		#reset_cause = cause_list[int(serial_data[2])]
		#print(reset_cause)

		auto_qurrey = "INSERT INTO atcs.auto_diagnosis(reset_cause, pcb_voltage, arm1_send_packet, arm1_received_packet, arm2_send_packet,arm2_received_packet, arm3_send_packet, arm3_received_packet, arm4_send_packet,arm4_received_packet, arm5_send_packet, arm5_received_packet, arm6_send_packet,arm6_received_packet, core_temprature, arm1_light_oc, arm2_light_oc, arm3_light_oc, arm4_light_oc, arm5_light_oc, arm6_light_oc, arm1_light_sc, arm2_light_sc, arm3_light_sc, arm4_light_sc, arm5_light_sc, arm6_light_sc, created_on)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		WriteToDatabase(auto_qurrey, str(reset_cause), str(master_pcb_voltage), str(packet_send_arm1),
						str(packet_rece_arm1), str(packet_send_arm2), str(packet_rece_arm2), str(packet_send_arm3),
						str(packet_rece_arm3), str(packet_send_arm4), str(packet_rece_arm4), str(packet_send_arm5),
						str(packet_rece_arm5), str(packet_send_arm6), str(packet_rece_arm6), str(core_temp),
						str(light_feedback_1), str(light_feedback_2), str(light_feedback_3), str(light_feedback_4),
						str(light_feedback_5), str(light_feedback_6),str(light_sc_1),str(light_sc_2),str(light_sc_3),str(light_sc_4),str(light_sc_5),str(light_sc_6), str(time.strftime('%Y-%m-%d %H:%M:%S')))

		final_msg = "$" +","+ str(event_type) + ","+ int(controller_id) + "," + generation_time+ ","  + int(reset_cause) + "," + int(master_pcb_voltage) + "," + int(packet_send_arm1) + "," + int(packet_rece_arm1) + "," + int(packet_send_arm2) + "," + int(packet_rece_arm2) + "," + int(packet_send_arm3) + "," + int(packet_rece_arm3) +  "," + int(packet_send_arm4) + "," + int(packet_rece_arm4) + ","  + int(packet_send_arm5) + "," + int(packet_rece_arm5) + ","  + int(packet_send_arm6) + "," + int(packet_rece_arm6) + ","+ int(core_temp) + "," + int(light_feedback_1) + "," + int(light_feedback_2) +"," + int(light_feedback_3) +"," + int(light_feedback_4) +"," + int(light_feedback_5) +"," + int(light_feedback_6) +"," + int(light_sc_1) + "," + int(light_sc_2) + "," + int(light_sc_3) + "," + int(light_sc_4) + "," + int(light_sc_5) + "," + int(light_sc_6) + ","+'#'
		print(final_msg)
		try:
			post_online(url_auto_diag,final_msg,"eventstring")
		except Exception as e:
			print(e)

	elif (serial_data[1] == "CF" and OTA_flag != 1):
		print(serial_data[1])
		#cf_counter += 1
		conf_sql = "DELETE from atcs.cf_conflict WHERE created_time < (now() - interval '2 days')"
		WriteToDatabase(conf_sql)
		cf_quarry="INSERT INTO atcs.cf_conflict(arm_id, light_name, mode_no, stage, what_need, what_is,created_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
		WriteToDatabase(cf_quarry,str(serial_data[2]),str(serial_data[3]),str(serial_data[4]),str(serial_data[5]),str(serial_data[6]),str(serial_data[7]),str(time.strftime('%Y-%m-%d %H:%M:%S')))

		# if cf_counter == 3:
		# 	write_to_serial("?AI1#")

		############added by HARSHAD For short circuit
		no_of_parameter = "009"
		event_type = "AZ"
		if(int(serial_data[6])==1 and int(serial_data[7])==0):
			shortcircuit = 0
			print("open ckt created")
		elif(int(serial_data[6]) == 0 and int(serial_data[7]) == 1):
			shortcircuit = 1   #  1 for short circuit
			print("short ckt created")
			detact_conflict_event(serial_data)
			print ("calling conflict function")
		# else:
		# 	shortcircuit = 1
		# 	#detact_conflict_event(serial_data)
		# 	print("calling conflict function2")
		arm_id = serial_data[2]
		mode_rcv = str(int(serial_data[4]))
		print("Mode Received-------", )
		# slave_code = ReadDatabase("SELECT slavecode FROM atcs.slave_master WHERE armno = {}".format(int(arm_no)))[0][0]
		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + mode_rcv + "," + reserved_2 + "," \
					+ str(shortcircuit) + "," + arm_id + ","

		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
								requestreserverd1,requestreserverd2,requestshortcircuit,requestarm_id,requestmode_rcv,isuploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		print(final_msg)
		insert_raw_data(final_msg)
		# AZ_string = final_msg
		try:
			post_online(url_events, final_msg, "eventstring")
		except Exception as e:
			print(e)
			WriteToDatabase(sql1, 21, controller_id, generation_time_2, time.strftime('%Y-%m-%d %H:%M:%S'),
							no_of_parameter, reserved_1, reserved_2, shortcircuit, arm_id, mode_rcv, False)


		lamp_ids = read_lamp_ids_from_db()
		lamp_health_no_of_parameter = "012"
		lamp_health_event_type = "AO"
		lamp_intensity = 1
		arm_no = serial_data[2]
		lamp_name = serial_data[3]
		if(lamp_name=="RED"):
			lamp_type=3
		elif(lamp_name=="GRN"):
			lamp_type=6
		elif (lamp_name == "GRNR"):
			lamp_type = 5
		lamp_ids_quarry = "select lampcode from atcs.lamp_master where lamptype='{}' and lampcode LIKE '%\{}'".format(lamp_type,arm_no)
		lamp_id = str(ReadDatabase(lamp_ids_quarry)[0][0])
		print("lamp id--------", lamp_id)
		sql11 = ("SELECT lamptype from atcs.lamp_master where lampcode= '{}' ".format(lamp_id))
		lamp_sign = ReadDatabase(sql11)[0][0]
		lamp_sign = str(lamp_sign)
		print("Lamp sign ------------", lamp_sign)
		lamp_health = 0
		print("lamp_health------", lamp_health)
		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + str(lamp_health_no_of_parameter) + "," + str(current_stage_no) + "," + \
					str(current_seq_no) + "," \
					+ str(lamp_health) + "," + str(lamp_intensity) + "," + str(arm_no) + "," + str(lamp_sign) + "," + str(lamp_id) + ","

		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
													requestreserverd1,requestreserverd2,requestlamhealth,requestlampintensity,requestarmno,requestlamptrafficsign,isuploaded)\
													VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		print(final_msg)
		try:
			post_online(url_events, final_msg, "eventstring")
		except Exception as e:
			print(e)
			WriteToDatabase(sql1, 15, controller_id, generation_time_2, time.strftime('%Y-%m-%d %H:%M:%S'),
							lamp_health_no_of_parameter, reserved_1, reserved_2, lamp_health, lamp_intensity,
							arm_no, lamp_id, False)


def detact_conflict_event(cf_string):
	generation_time = time.strftime('%d%m%Y%H%M%S')
	#print("conflict string",cf_string)  $,CF,2,RED,2,1,0,1,#(cf, arm id, lightname, mode, stage, need , is )
	arm_id = cf_string[2]
	cf_light = cf_string[3]
	stage_id = cf_string[5]
	#print("arm id from function",arm_id)
	sql_cf = "SELECT * FROM atcs.cf_conflict WHERE created_time > (now() - interval '10 minute') and what_is = '1' and light_name = '{}' and arm_id = '{}' ".format(cf_light,arm_id)
	#print("seq for conflict from fun",sequence_for_conflict)
	detected_conflict = ReadDatabase(sql_cf)
	print("detected conflict",detected_conflict)
	#print("cf string",cf_string)
	print ("len of detected conflict",len(detected_conflict))
	if len(detected_conflict) > 3 and (cf_light == "GRN" or cf_light == "GRNR"):
		print("blinker mode on")
		write_to_serial("?AI1#")

	if (cf_light == "GRN" or cf_light == "GRNR"):
		green_stage = [x for x in sequence_for_conflict if x[6] != int(0)]
		print(("green_stage", green_stage))
		for i in green_stage:
			print("green stage in for loop",i)
			print("stage id from string",stage_id)
			if str(stage_id) == str(i[1]):
				print("conflict stag id",i[1])
				conflict_arm_id = i[0]
				print("conflict arm id", i[0])

		event_type = "AY"
		no_of_parameter = "10"
		shortcircuit_event = "1"
		if (cf_light == "GRNR"):
			lamp_type = 5
		elif (cf_light == "GRN"):
			lamp_type = 6


		sql_lampcode1 = "select lampcode from atcs.lamp_master lm inner join atcs.slave_master as ms on ms.slavecode = lm.slavecode where ms.armno = '{}' and lm.lamptype = '{}'".format(arm_id, lamp_type)
		sql_lampcode2 = "select lampcode from atcs.lamp_master lm inner join atcs.slave_master as ms on ms.slavecode = lm.slavecode where ms.armno = '{}' and lm.lamptype = '{}'".format(conflict_arm_id, lamp_type)
		shortcircuit_lamp_code = ReadDatabase(sql_lampcode1)[0][0]
		print("short ckt lamp code",shortcircuit_lamp_code)
		conflict_lamp_code =  ReadDatabase(sql_lampcode2)[0][0]
		print("conflict lamp code", conflict_lamp_code)

		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," + reserved_2 + "," \
				+ str(shortcircuit_lamp_code) + "," + str(conflict_lamp_code) + "," + str(shortcircuit_event) + ","

		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
														requestreserverd1,requestreserverd2,requestlampcode_1,requestlampcode_2,isuploaded)\
														VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		print(final_msg)
		try:
			post_online(url_events, final_msg, "eventstring")
		except Exception as e:
			print(e)
			WriteToDatabase(sql1, 15, controller_id, generation_time_2, time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter, reserved_1, reserved_2, shortcircuit_lamp_code, conflict_lamp_code, False)
		if cf_light == "GRN":
			id = 0
		elif cf_light == "GRNR":
			id = 1
		cf_to_master = "CF"+chr(int(id))+chr(int(arm_id))+chr(int(id))+chr(int(conflict_arm_id))+"#"
		write_to_serial(cf_to_master)


def check_mode_chnage():
	global created_by
	global mod_flag
	# f = open("/home/atreyo-atcs14/Documents/ATCS/mode",'r')
	prv_mode = read_file("/home/{}/Documents/ATCS/mode".format(device_name))
	# f.close()
	print("prv_mode---------",prv_mode)
	print("mod_flag---------",mod_flag)
	if(current_mode != prv_mode and mod_flag == 0):
		send_mode_change_event(prv_mode,current_mode,'-1')
		mod_flag = 1

def send_au_during_blinker():
	global send_au
	while(send_au == 1):
		print("calling from send_au function" )
		_ = send_cycle_over_event()
		time.sleep(2)

def send_detector_events(arm_no,detector_ip,health):
	
	generation_time = time.strftime('%d%m%Y%H%M%S') #datetime.datetime.today().strftime('%d%m%Y%H%M%S')
	generation_time_2 = time.strftime('%Y-%m-%d %H:%M:%S')
	
	event_type = 'AE'
	no_of_parameter = '010'

	final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + current_stage_no + "," +str(current_seq_no) + "," \
		+ str(arm_no) + "," + str(detector_ip) + "," + str(health) + ","
		
	sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
					requestreserverd1,requestreserverd2,requestarmno,requestdetectoripaddress,requesteventstatus,isuploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

	print(final_msg)
	insert_raw_data(final_msg)
	# AE_string = final_msg
	try:
		post_online(url_events,final_msg,"eventstring")
	except:
		WriteToDatabase(sql1,5, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,arm_no,detector_ip,health,False)



def send_mode_change_event(prevous_mode,current_mode,created_by):
	global count_num
	if(str(prevous_mode) != str(current_mode) ):

		generation_time = time.strftime('%d%m%Y%H%M%S') #datetime.datetime.today().strftime('%d%m%Y%H%M%S')
		generation_time_2 = time.strftime('%Y-%m-%d %H:%M:%S')
		
		event_type = 'AK'
		no_of_parameter = '011'

		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2 + "," \
			+ str(prevous_mode) + "," + str(current_mode) + "," + str(current_seq_no) + "," + str(created_by) + ","
			
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
						requestreserverd1,requestreserverd2,requestpreviousmodetype,requestcurrentmodetype,requestcurrentsequenceno,requesteventchangedby,isuploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		if count_num == 1:
			count_num = 0
		print(final_msg)
		insert_raw_data(final_msg)
		# AK_string = final_msg
		try:
			post_online(url_events,final_msg,"eventstring")
		except:
			WriteToDatabase(sql1,11, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,prevous_mode,current_mode,current_seq_no,created_by,False)


def send_sequence_change_event(prevous_sequence,current_sequence,mode_id,created_by):

	if(str(prevous_sequence) != str(current_sequence)):
		print("prevous_sequence-----",prevous_sequence)

		generation_time = time.strftime('%d%m%Y%H%M%S') #datetime.datetime.today().strftime('%d%m%Y%H%M%S')
		generation_time_2 = time.strftime('%Y-%m-%d %H:%M:%S')
		
		event_type = 'AL'
		no_of_parameter = '011'

		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2 + "," \
			+ str(prevous_sequence) + "," + str(current_sequence) + "," + str(mode_id) + "," + str(created_by) + ","
			
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
						requestreserverd1,requestreserverd2,requestprevioussequenceno,requestcurrentsequenceno,requestcurrentmodetype,requesteventchangedby,isuploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		print(final_msg)
		insert_raw_data(final_msg)
		# AL_string = final_msg
		try:
			post_online(url_events,final_msg,"eventstring")
		except:
			WriteToDatabase(sql1,12, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,prevous_sequence,current_sequence,mode_id,created_by,False)

def send_cycle_time_change_event(temp_previous_cycle_time,current_cycle_time):

	if(str(temp_previous_cycle_time) != str(current_cycle_time)):

		generation_time = time.strftime('%d%m%Y%H%M%S') #datetime.datetime.today().strftime('%d%m%Y%H%M%S')
		generation_time_2 = time.strftime('%Y-%m-%d %H:%M:%S')
		
		event_type = 'AM'
		no_of_parameter = '009'

		final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + reserved_1 + "," +reserved_2 + "," \
			+ str(temp_previous_cycle_time) + "," + str(current_cycle_time) + ","
			
		sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
						requestreserverd1,requestreserverd2,requestpreviouscycletime,requestcurrentcycletime,isuploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

		print(final_msg)
		insert_raw_data(final_msg)
		# AM_string = final_msg
		try:
			post_online(url_events,final_msg,"eventstring")
		except:
			WriteToDatabase(sql1,13, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,temp_previous_cycle_time,current_cycle_time,False)


def send_cycle_over_event():

	global previous_cycle_time
	global cycle_start_date_time
	sql1 = "SELECT coalesce(sum(pcu),0.0000) as pcu from atcs.cameraprocesseddata where utctime between '{}' and '{}'"	

	generation_time = time.strftime('%d%m%Y%H%M%S') #datetime.datetime.today().strftime('%d%m%Y%H%M%S')
	generation_time_2 = time.strftime('%Y-%m-%d %H:%M:%S')

	print(generation_time_2)
	print(cycle_start_date_time)

	sql6 = "SELECT * from atcs.sp_get_saturationindex_report('ref1','{}','{}');fetch all in \"ref1\";" #query for saturation index added 20/5/2020 udgish
	saturationind1 = ReadDatabase(sql6.format(cycle_start_date_time,generation_time_2))[0][0] #added sa
	print(saturationind1)
	if(modeid==4):

		sql3="SELECT (sum(atcstime))::text as corridorcycletime from atcs.adaptiveoutputdata; "	
		coritime=ReadDatabase(sql3)[0][0]
		print(coritime)
	else:
		coritime = '0'

	print("coritime",coritime)
	
	event_type = 'AU'
	no_of_parameter = '014'
	pcu_count = ReadDatabase(sql1.format(cycle_start_date_time,generation_time_2))[0][0]

	s1 = cycle_start_date_time[11:]
	print("cycle_start_date_time...",s1)
	s2 = generation_time_2[11:]
	print("generation_time_2...", s2)
	FMT = '%H:%M:%S'
	t = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
	
	if(current_mode == '1'):
		current_cycle_1  = t.seconds
		print("current_cycle_1...",current_cycle_1) 
	else:
		if(current_mode == '5'):
			current_cycle_1 = '2'
		else:
			current_cycle_1 = current_cycle_time

	cycle_start_date_time = generation_time_2 # store cycle start time for next cycle over evenct and pcu count.

	diff = int(previous_cycle_time)-int(current_cycle_time)
	if(diff >= 0):
		sign = "+"
		diff = str(diff)
	else:
		sign = "-"
		diff = str(diff)[1:]

	previous_cycle_time = current_cycle_time

	final_msg = "$" + controller_id + "," + generation_time + "," + event_type + "," + no_of_parameter + "," + str(current_seq_no) + "," +str(saturationind1) + "," \
		+ corridor +","+ current_mode +","+str(current_cycle_1) + "," + sign + "," + diff + "," + str(pcu_count) + ","+ str(coritime)+","
		
	sql1 = "INSERT INTO atcs.eventlogs (eventid,requestcontrollerid,requesteventgeneratetimestamp,requesteventsendtimestamp,requestpacketparameterno,\
			requestreserverd1,requestreserverd2,requestadaptivecoridor,requestcurrentmodetype,requestcurrentcycletime,requestrtctimedifference,requestcycledifference,pcu,isuploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

	print(final_msg)
	insert_raw_data(final_msg)
	# AU_string = final_msg
	try:
		post_online(url_events,final_msg,"eventstring")
	except:
		WriteToDatabase(sql1,34, controller_id,generation_time_2,time.strftime('%Y-%m-%d %H:%M:%S'),no_of_parameter,reserved_1,reserved_2,corridor,current_mode,current_cycle_time,sign,diff,pcu_count,False)

def ReadDatabase(querry):
	
	counter = 0 # for trying atleast five times in case of failure.
	while True:
		try:
			conn = psycopg2.connect(database="atcs_gmc", user="postgres", password="postgres", host=database_ip, port="5432")
			#print(querry)
			cur = conn.cursor()
			cur.execute(querry)
			result = cur.fetchall()#[(1,hg,64),()]
			# result = conn.execute(querry).fetchall()
			conn.close()
			break
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			try:
				conn.close()
				counter += 1
				if(counter > 5):
					result = []
					break
			except:
				result = []
				break
	counter = 0
	return result
	
def WriteToDatabase(sql1,*args):
	# print(args)
	counter = 0 # for trying atleast five times in case of failure.
	while True:
		try:
			conn = psycopg2.connect(database="atcs_gmc", user="postgres", password="postgres", host=database_ip, port="5432")
			cur = conn.cursor()
			cur.execute(sql1,args)
			conn.commit()
			conn.close()
			print("Inserted in Database....")
			break
		except Exception as e:
			print("Error in Database writing-------::::",e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			try:
				conn.close()
				counter += 1
				if(counter > 5):
					break
			except Exception as e:
				print("WriteToDatabase error",e)
				break
	counter = 0


def send_stage_time(table_name,total_stage,slot,sequence,today_date):

	global msg_stage_timing
	global current_cycle_time

	temp_previous_cycle_time = current_cycle_time

	length = (((int(total_stage))*3)+4) # this is total byte for microcontroller ## length = (((5)*3)+4)

	write_to_serial("st"+ format_byte(str(length),2)+"#") #chr(length) If required.
	
	msg_stage_timing = "$" + format_byte(str(total_stage),2) # Used in AQ Event

	send_stage_timing = "$" + chr(total_stage) # To send stage time to microcontroller

	for i in range(1,int(total_stage)+1): # Read stage time from database.
		querry = "SELECT totaltime FROM atcs.daywise_planoperations WHERE (stageid = '{}'and slotno = '{}' and sequenceid = '{}' and plandate = '{}')".\
					format(i,slot,sequence,today_date)
		res1 = ReadDatabase(querry)[0][0]
		msg_stage_timing += format_byte(str(res1),3)
		send_stage_timing += chr(res1)  

	send_stage_timing += "#" # To send stage time to microcontroller
	msg_stage_timing += "#" # Used in AQ Event
	print("Stage_timing---",msg_stage_timing)

	write_to_serial(send_stage_timing)
	time.sleep(2)

	all_stage_time = [msg_stage_timing[i:i+3] for i in range(0,len(msg_stage_timing),3)]
	current_cycle_time = int(all_stage_time[1])
	
	for i in range(3,len(all_stage_time),2):
		if(all_stage_time[i] != '#'):
			current_cycle_time += int(all_stage_time[i])

	send_cycle_time_change_event(temp_previous_cycle_time,current_cycle_time)

	
def send_sequence(querry): # Read sequences from database and send to microcontroller.

	global sequence_string
	global sequence_for_conflict         #HARSHAD 14-03-2023

	write_to_serial("sequ#")
	time.sleep(0.1)
	result = ReadDatabase(querry)
	sequence_for_conflict = copy.deepcopy(result)      #HARSHAD 14-03-2023

	print("result--------------",result)
	print("len of result------------------",len(result))

	if(len(result)>0):

		for row in result:
			print("row----------",row)
			# a = "@" + arm_no_id + format_byte(stage_id,2) + (stop) + (caution) + (leftsign) + rightsign + throughsign + walkman + stopman + u_turn + no_uturn + no_left_turn + "#"

			if(int(row[2]) == 1 and int(row[3]) == 1):
				print("Found unappropriate sequence in database ..............")
				break
			else:
				# sequence_string = "@" + chr(int(row[0])) + chr(row[1]) + chr(invert(row[2])) + chr(
				# 	invert(row[3])) + chr(invert(row[4])) + chr(invert(row[5])) \
				# 				  + chr(invert(row[6])) + chr(invert(row[7])) + chr(invert(row[8])) + chr(
				# 	invert(row[9])) + chr(invert(row[10])) + chr(invert(row[11])) + "#"
				sequence_string = "@" + chr(int(row[0])) + chr(row[1]) + chr(invert(row[2])) + chr(
					invert(row[3])) + chr(invert(row[4])) + chr(invert(row[5])) \
								  + chr(invert(row[6])) + chr(invert(row[7])) + chr(invert(row[8])) + chr(
					invert(row[9])) + chr(invert(row[10])) + chr(invert(row[11]))  + chr((row[12])) +  chr(invert(row[13])) + chr(invert(row[14]))+ "#"

			# sequence_string = "@" + str(row[0]) + format_byte(str(row[1]),2) + invert(row[2]) + invert(row[3]) + invert(row[4]) + invert(row[5])\
				 # + invert(row[6]) + invert(row[7]) + invert(row[8]) + invert(row[9]) + invert(row[10]) + invert(row[11]) + "#"
				#sequence_string = "@" + chr(int(row[0])) + chr(row[1]) + chr(invert(row[2])) + chr(invert(row[3])) + chr(invert(row[4])) + chr(invert(row[5]))+ chr(invert(row[6])) + chr(invert(row[7])) + chr(invert(row[8])) + chr(invert(row[9])) + chr(invert(row[10])) + chr(invert(row[11]) + chr(brt_invert(row[12])) +  chr(brt_invert(row[13])) + chr(brt_invert(row[14])) + "#"
				print("final string to serial------------ewdwfw",sequence_string)
			write_to_serial(sequence_string)
			print("final string to serial------------",sequence_string)
			# write_to_serial(sequence_string)
			print(sequence_string.encode())
			time.sleep(.3)
			count_num = 0 
			
def check_conditions(timing_tools):# This function check plan time with current time continously.
	counter = 0
	if(len(timing_tools)>0):
		for key,value in timing_tools.items():	# timing tools will be like {"2":["00:05:34","12:22:32"]} where "2" is slot.	
			counter += 1
			current_time = time.strptime(time.strftime('%H:%M:%S'),'%H:%M:%S')
			start_time = time.strptime(value[0],'%H:%M:%S')
			end_time = time.strptime(value[1],'%H:%M:%S')
			if((current_time >= start_time) and (current_time <= end_time)):
				return True,key
				break
			elif(counter == len(timing_tools)):
				return False,key
	else:
		return False,0

def check_event_conditions(timing_tools): # This function check event time (set from dashboard) with current time continously.
	
	condition = False
	priority = 1
	mode = 0
	
	if(len(timing_tools)>0):
		for key in sorted(timing_tools):# for key,value in timing_tools.items(): #event timing will be like {"2":["1",00:05:34","12:22:32"]} where "2" is priority and "1" is modeid.
			value = timing_tools[key]		

			current_time = time.strptime(time.strftime('%H:%M:%S'),'%H:%M:%S')
			start_time = time.strptime(value[1],'%H:%M:%S')
			end_time = time.strptime(value[2],'%H:%M:%S')

			if((current_time >= start_time) and (current_time <= end_time)):
				condition = True
				if (priority<=int(key)):
					priority = int(key)
					mode = int(value[0])
		return condition,priority,mode	
	else:
		return condition,priority,mode

def read_seq():
	global sequenceid
	global current_seq_no
	global today_date
	global priority_flag
	print(priority_flag,today_date,"@@@flag,date@@@")
	sql4 = "SELECT slotno from atcs.daywise_planoperations WHERE priorityflag = '{}' and plandate = '{}'"
	slot = ReadDatabase(sql4.format(priority_flag,today_date))[0][0]
	print(slot,"@@@slot@@@")
	
	sql2 = "SELECT sequenceid FROM atcs.daywise_planoperations WHERE slotno = '{}' and plandate = '{}'"
	#prevous_sequence = current_seq_no
	sequenceid = ReadDatabase(sql2.format(slot,today_date))[0][0]
	current_seq_no = str(sequenceid)
	print(current_seq_no,"@@@current_seq_no@@@")
	return current_seq_no
	#if(mode_id == 1):
		#prev_known_fixed_seq = current_seq_no   #changed by ud 5/08
	
def send_configuration_data_to_microcontroller(slot,mode_id,created_by,today_date): # Send stage time and sequence to microcontroller.

	global total_stage
	global sequenceid
	global current_seq_no

	sql1 = "SELECT MAX(stageid) from atcs.daywise_planoperations WHERE slotno = '{}' and plandate = '{}'"
	sql2 = "SELECT sequenceid FROM atcs.daywise_planoperations WHERE slotno = '{}' and plandate = '{}'"
	# sql3 = "SELECT  armid, stageid, stop, caution, leftsign, rightsign, throughsign,walkman, stopman, u_turn,\
	# 			 no_u_turn, noo_left_turn from atcs.daywise_planoperations WHERE (slotno = '{}' and sequenceid = '{}' and plandate = '{}') order by fromtime, totime, stageid, armid"	------without brts logic(mileen)
	sql3 = "SELECT  armid, stageid, stop, caution, leftsign, rightsign, throughsign,walkman, stopman, u_turn, no_u_turn, noo_left_turn,\
        		COALESCE(isbrt,false) AS isbrt, COALESCE(brtred,0) AS brtred, COALESCE(brtgreen,0) AS brtgreen \
				from atcs.daywise_planoperations \
				inner join atcs.global_configurations on armno = armid \
				WHERE (slotno = '{}' and sequenceid = '{}' and plandate = '{}') order by fromtime, totime, stageid, armid"  #----with brts logic(mileen)

	try:
		total_stage = ReadDatabase(sql1.format(slot,today_date))[0][0] # Read no.f Stage from database.
		prevous_sequence = current_seq_no
		print("prevous_sequence----",prevous_sequence)
		sequenceid = ReadDatabase(sql2.format(slot,today_date))[0][0]
		#print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@sqid@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",sequenceid)
		current_seq_no = str(sequenceid)
		print("current_sequence----",current_seq_no)

		send_sequence_change_event(prevous_sequence,current_seq_no,mode_id,created_by)
		if(mode_id == 1):
			global prev_known_fixed_seq
			prev_known_fixed_seq = current_seq_no   # Used in AQ Event.
			print("prev_known_fixed_seq-----",prev_known_fixed_seq)

		send_stage_time("atcs.daywise_planoperations",total_stage,slot,sequenceid,today_date) # This Function send stage time to microcontroller.
		print("slot in send configuration data to microcontroller",slot)

		send_sequence(sql3.format(slot,sequenceid,today_date)) # This Function send sequence time to microcontroller.

	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		print("Handle_mode_change function error......",e)

def handle_mode_change(slot,today_date,mode_id): # This function will execute as per plan timing or mode change events from software.
	
	global created_by  # Added By Amit 1-9-20
	global modeid
	global start_exe_flag
	global mod_flag
	global HC_Flag
	global cycle_start_date_time
	
	querry = "SELECT coalesce(createdby,0) FROM atcs.daywise_planoperations WHERE plandate = '{}' and slotno = '{}'"
	created_by = ReadDatabase(querry.format(today_date,slot))[0][0]

	time.sleep(3) # Chnged form 10 to 3.

	if(mode_id == 1): 

		# f = open("/home/atreyo-atcs14/Documents/ATCS/mode",'w') #Store the mode_id in a file
		# f.write('1')
		# f.close()
		write_to_file("/home/{}/Documents/ATCS/mode".format(device_name),'1')
		if(modeid == 5):  # Tell Controller to Stop Blinker mode
			write_to_serial("stop#")
			print("Stop Blinker Mode...............")
			time.sleep(2)

		print("Entered in Fix mode ...........................................")
		# check and send remaining stage timing for va/sva/atcs mode manually
		_ = check_ramaining_stage_in_previous_mode(2)
		_ = check_ramaining_stage_in_previous_mode(3)
		_ = check_ramaining_stage_in_previous_mode(4)	
		_ = check_ramaining_stage_in_previous_mode(6)	
		_ = check_ramaining_stage_in_previous_mode(7)
		_ = check_ramaining_stage_in_previous_mode(8)         #new mode 23-03-2023
		_ = check_ramaining_stage_in_previous_mode(9)         #new mode 23-03-2023

		try:
			write_to_serial("?AA1#") #  Send Mode change to controller
			time.sleep(0.3)
			write_to_serial("?AA1#") #  Send Mode change to controller
			send_configuration_data_to_microcontroller(slot,1,created_by,today_date) # send stage time and sequences to controller
			time.sleep(0.01)
			write_to_serial("?AA1#") #  Send Mode change to controller
			cycle_start_date_time = time.strftime('%Y-%m-%d %H:%M:%S')
			print("cycle start time is:", cycle_start_date_time)
			# send_configuration_data_to_microcontroller(slot,1,created_by,today_date) # send stage time and sequences to controller
			time.sleep(0.3)
			write_to_serial("?AA1#")
			mod_flag = 0

		except Exception as e:
			#ReadDatabase(sql1.format(slot,today_date))[0][0]
			print("Got error......",e)
			
		threading.Thread(target = fix_mode).start() # Start fix mode through this thread.
		modeid = 1
		
	if(mode_id == 2):

		# f = open("/home/atreyo-atcs14/Documents/ATCS/mode",'w') # Store the mode_id in a file
		# f.write('2')
		# f.close()
		write_to_file("/home/{}/Documents/ATCS/mode".format(device_name),'2')
		if(modeid == 5): # Tell Controller to Stop Blinker mode
			write_to_serial("stop#")
			print("Stop Blinker Mode...............")
			time.sleep(2)

		try:
			print("Entered in VA mode ...........................................")
			os.system("sudo killall -9 ATCS_GMC_NewVALogic") # Kill VA Exe if running.
			os.system("sudo killall -9 ATCS_GMC_NewVAWithBRTLogic") # Kill VA Exe if running.(mileen)
			# check and send remaining stage timing for va/sva/atcs/ mode manually
			# _ = check_ramaining_stage_in_previous_mode(2)
			_ = check_ramaining_stage_in_previous_mode(3)
			_ = check_ramaining_stage_in_previous_mode(4) 
			_ = check_ramaining_stage_in_previous_mode(6)
			_ = check_ramaining_stage_in_previous_mode(7)
			_ = check_ramaining_stage_in_previous_mode(8)  # new mode 23-03-2023
			_ = check_ramaining_stage_in_previous_mode(9)  # new mode 23-03-2023

			time.sleep(0.05)
			write_to_serial("?AA2#")
			time.sleep(0.3)
			write_to_serial("?AA2#")
			send_configuration_data_to_microcontroller(slot,2,created_by,today_date) # send stage time and sequences to controller
			time.sleep(0.01)			
			write_to_serial("?AA2#")
			time.sleep(0.3)
			write_to_serial("?AA2#")
			mod_flag = 0
			# It will wait until cycle over doesn't happen and controller willn't send start exe string.
			count_out=1
			while (start_exe_flag):
				time.sleep(1)			
				write_to_serial("?AA2#")
				if (count_out>=10):
					break
				count_out+=1
				continue
			start_exe_flag = 1

		except Exception as e:
			print("Got error......",e)
		
		threading.Thread(target = va_sva_mode,args=(2,slot,today_date,)).start() # Start VA Mode through this thread.
		modeid = 2
		
	if(mode_id == 3):

		# f = open("/home/atreyo-atcs14/Documents/ATCS/mode",'w') #Store the mode_id in a file
		# f.write('3')
		# f.close()	
		write_to_file("/home/{}/Documents/ATCS/mode".format(device_name),'3')

		if(modeid == 5): #Tell Controller to Stop Blinker mode
			write_to_serial("stop#")
			print("Stop Blinker Mode...............")
			time.sleep(2)

		try:
			print("Entered in SVA mode ...........................................")
			os.system("sudo killall -9 ATCS_GMC_NewVALogic")  # Kill SVA Exe if running.
			os.system("sudo killall -9 ATCS_GMC_NewVAWithBRTLogic") # Kill VA Exe if running.(mileen)
			_ = check_ramaining_stage_in_previous_mode(2)
			# _ = check_ramaining_stage_in_previous_mode(3)
			_ = check_ramaining_stage_in_previous_mode(4)## Added by Amit 1_9_20
			_ = check_ramaining_stage_in_previous_mode(6)	## Added by Amit 1_9_20	
			_ = check_ramaining_stage_in_previous_mode(7)	## Added by Amit 1_9_20
			_ = check_ramaining_stage_in_previous_mode(8)  # new mode 23-03-2023
			_ = check_ramaining_stage_in_previous_mode(9)  # new mode 23-03-2023
			time.sleep(0.05)
			write_to_serial("?AA3#")
			time.sleep(0.3)
			write_to_serial("?AA3#")
			send_configuration_data_to_microcontroller(slot,3,created_by,today_date) # send stage time and sequences to controller
			time.sleep(0.05)
			write_to_serial("?AA3#")
			time.sleep(0.3)
			write_to_serial("?AA3#")
			mod_flag = 0
			# It will wait until cycle over doesn't happen and controller willn't send start exe string.
			count_out=1
			while (start_exe_flag):
				time.sleep(1)			
				write_to_serial("?AA3#")
				if(count_out>=10):
					break
				count_out+=1 
				continue
			start_exe_flag = 1
			
		except Exception as e:
			print("Got error......",e)

		threading.Thread(target = va_sva_mode,args = (3,slot,today_date,)).start() # Start SVA Mode through this thread.
		modeid = 3
		
	if(mode_id == 4):

		# f = open("/home/atreyo-atcs14/Documents/ATCS/mode",'w') #Store the mode_id in a file
		# f.write('4')
		# f.close()
		write_to_file("/home/{}/Documents/ATCS/mode".format(device_name),'4')
		print("Entered in ATCS mode----------------")

		if(modeid == 5): #Tell Controller to Stop Blinker mode
			write_to_serial("stop#")
			print("Stop Blinker Mode...............")
			time.sleep(2)

		try:
			time.sleep(0.05)
			write_to_serial("?AA4#") # Send Mode change to controller
			time.sleep(0.3)
			write_to_serial("?AA4#") # Send Mode change to controller
			send_configuration_data_to_microcontroller(slot,4,created_by,today_date) # send stage time and sequences to controller
			time.sleep(0.05)
			write_to_serial("?AA4#") #  Send Mode change to controller
			time.sleep(0.3)
			write_to_serial("?AA4#")
			mod_flag = 0

		except Exception as e:
			print("Got error......",e)

		threading.Thread(target = atcs_mode).start() # Start ATCS Mode through this thread.
		modeid = 4
    
	if(mode_id == 5 ):

		# f = open("/home/atreyo-atcs14/Documents/ATCS/mode",'w') #Store the mode_id in a file
		# f.write('5')
		# f.close()	
		write_to_file("/home/{}/Documents/ATCS/mode".format(device_name),'5')
		try:
			print("Entered in Blinking Mode----------------")
			os.system("sudo killall -9 ATCS_GMC_NewVALogic") # Kill SVA Exe if running.
			os.system("sudo killall -9 ATCS_GMC_NewVAWithBRTLogic") # Kill VA Exe if running.(mileen)
			_ = check_ramaining_stage_in_previous_mode(2)
			_ = check_ramaining_stage_in_previous_mode(3)
			_ = check_ramaining_stage_in_previous_mode(4) 
			_ = check_ramaining_stage_in_previous_mode(6)
			_ = check_ramaining_stage_in_previous_mode(7)
			_ = check_ramaining_stage_in_previous_mode(8)  # new mode 23-03-2023
			_ = check_ramaining_stage_in_previous_mode(9)  # new mode 23-03-2023
			time.sleep(0.05)
			write_to_serial("?AA5#")
			time.sleep(0.3)
			write_to_serial("?AA5#")
			send_configuration_data_to_microcontroller(slot,5,created_by,today_date) # send stage time and sequences to controller.
			time.sleep(0.05)
			write_to_serial("?AA5#")
			time.sleep(0.3)
			write_to_serial("?AA5#")
			mod_flag = 0

		except Exception as e:
			print("Got error......",e)
		
		threading.Thread(target = blinkmode_mode).start() # Start Blinker Mode through this thread.
		modeid = 5
		
	if(mode_id == 6):

		# f = open("/home/atreyo-atcs14/Documents/ATCS/mode",'w') #Store the mode_id in a file
		# f.write('6')
		# f.close()
		write_to_file("/home/{}/Documents/ATCS/mode".format(device_name),'6')
		print("Entered in VA_Offset_mode-----------------")

		if(modeid == 5): #Tell Controller to Stop Blinker mode
			write_to_serial("stop#")
			print("Stop Blinker Mode...............")
			time.sleep(2)

		try:
			time.sleep(0.05)
			write_to_serial("?AA6#") # Send Mode change to controller
			time.sleep(0.3)
			write_to_serial("?AA6#") # Send Mode change to controller
			send_configuration_data_to_microcontroller(slot,6,created_by,today_date) # send stage time and sequences to controller.
			time.sleep(0.05)
			write_to_serial("?AA6#") #  Send Mode change for controller
			time.sleep(0.3)
			write_to_serial("?AA6#") # Send Mode change to controller
			mod_flag = 0

		except Exception as e:
			print("Got error......",e)

		threading.Thread(target = atcs_mode).start() # Start VA_Offset Mode through this thread.
		modeid = 6	
	
	if(mode_id == 7):

		# f = open("/home/atreyo-atcs14/Documents/ATCS/mode",'w') #Store the mode_id in a file.
		# f.write('7')
		# f.close()
		write_to_file("/home/{}/Documents/ATCS/mode".format(device_name),'7')
		print("Entered in Fix_offset_mode---------------")

		if(modeid == 5): #Tell Controller to Stop Blinker mode
			write_to_serial("stop#")
			print("Stop Blinker Mode...............")
			time.sleep(2)
		
		try:
			time.sleep(0.05)
			write_to_serial("?AA7#") #  Send Mode change for controller
			time.sleep(0.3)
			write_to_serial("?AA7#")
			send_configuration_data_to_microcontroller(slot,7,created_by,today_date) # send stage time and sequences to controller.
			time.sleep(0.05)
			write_to_serial("?AA7#") #  Send Mode change for controller
			time.sleep(0.3)
			write_to_serial("?AA7#")
			mod_flag = 0

		except Exception as e:
			print("Got error......",e)
		threading.Thread(target = atcs_mode).start() # Start Fix_Offset Mode through this thread.
		modeid = 7

	if (mode_id == 8):           # ADDED BY HARSHAD 17-03-2023

		# f = open("/home/atreyo-atcs14/Documents/ATCS/mode",'w') # Store the mode_id in a file
		# f.write('2')
		# f.close()
		write_to_file("/home/{}/Documents/ATCS/mode".format(device_name), '8')
		if (modeid == 5):  # Tell Controller to Stop Blinker mode
			write_to_serial("stop#")
			print("Stop Blinker Mode...............")
			time.sleep(2)

		try:
			print("Entered in VA with STAGE SKIP mode ...........................................")
			os.system("sudo killall -9 ATCS_GMC_NewVALogic")  # Kill VA Exe if running.
			os.system("sudo killall -9 ATCS_GMC_NewVAWithBRTLogic") # Kill VA Exe if running.(mileen)
			# check and send remaining stage timing for va/sva/atcs/ mode manually
			_ = check_ramaining_stage_in_previous_mode(2)
			_ = check_ramaining_stage_in_previous_mode(3)
			_ = check_ramaining_stage_in_previous_mode(4)
			_ = check_ramaining_stage_in_previous_mode(6)
			_ = check_ramaining_stage_in_previous_mode(7)
			#_ = check_ramaining_stage_in_previous_mode(8)
			_ = check_ramaining_stage_in_previous_mode(9)

			time.sleep(0.05)
			write_to_serial("?AA8#")
			time.sleep(0.3)
			write_to_serial("?AA8#")
			send_configuration_data_to_microcontroller(slot, 8, created_by,today_date)  # send stage time and sequences to controller
			time.sleep(0.01)
			write_to_serial("?AA8#")
			time.sleep(0.3)
			write_to_serial("?AA8#")
			mod_flag = 0
			# It will wait until cycle over doesn't happen and controller willn't send start exe string.
			count_out = 1
			while (start_exe_flag):
				time.sleep(1)
				write_to_serial("?AA8#")
				if (count_out >= 10):
					break
				count_out += 1
				continue
			start_exe_flag = 1

		except Exception as e:
			print("Got error......", e)

		threading.Thread(target=va_sva_mode, args=(8,)).start()  # Start VA Mode through this thread.
		modeid = 8

	if (mode_id == 9):           # ADDED BY HARSHAD 17-03-2023

		# f = open("/home/atreyo-atcs14/Documents/ATCS/mode",'w') # Store the mode_id in a file
		# f.write('2')
		# f.close()
		write_to_file("/home/{}/Documents/ATCS/mode".format(device_name), '9')
		if (modeid == 5):  # Tell Controller to Stop Blinker mode
			write_to_serial("stop#")
			print("Stop Blinker Mode...............")
			time.sleep(2)

		try:
			print("Entered in VA with STAGE SKIP mode ...........................................")
			os.system("sudo killall -9 ATCS_GMC_NewVALogic")  # Kill VA Exe if running.
			os.system("sudo killall -9 ATCS_GMC_NewVAWithBRTLogic") # Kill VA Exe if running.(mileen)
			# check and send remaining stage timing for va/sva/atcs/ mode manually
			_ = check_ramaining_stage_in_previous_mode(2)
			_ = check_ramaining_stage_in_previous_mode(3)
			_ = check_ramaining_stage_in_previous_mode(4)
			_ = check_ramaining_stage_in_previous_mode(6)
			_ = check_ramaining_stage_in_previous_mode(7)
			_ = check_ramaining_stage_in_previous_mode(8)
			#_ = check_ramaining_stage_in_previous_mode(9)

			time.sleep(0.05)
			write_to_serial("?AA9#")
			time.sleep(0.3)
			write_to_serial("?AA9#")
			send_configuration_data_to_microcontroller(slot, 9, created_by,today_date)  # send stage time and sequences to controller
			time.sleep(0.01)
			write_to_serial("?AA9#")
			time.sleep(0.3)
			write_to_serial("?AA9#")
			mod_flag = 0
			# It will wait until cycle over doesn't happen and controller willn't send start exe string.
			count_out = 1
			while (start_exe_flag):
				time.sleep(1)
				write_to_serial("?AA9#")
				if (count_out >= 10):
					break
				count_out += 1
				continue
			start_exe_flag = 1

		except Exception as e:
			print("Got error......", e)

		threading.Thread(target=va_sva_mode, args=(9,)).start()  # Start VA Mode through this thread.
		modeid = 9

def reconnect_junction():
	while True:
		######------------------API Reconnect-------------------------------###########
		try:

			time.sleep(2)
			
			sql_1 = "select * from atcs.spread_api_reconnect('ref1');fetch all in \"ref1\";"
			sql_2 = "SELECT * from atcs.spupdate_api_reconnect({})"

			#cam_reconnect_1 = "select * from atcs.spread_api_camerareconnect('ref1');fetch all in \"ref1\";"       #HARSHAD
			#cam_reconnect_2 = "SELECT * from atcs.spupdate_api_camerareconnect({})"                                 #HARSHAD
			

			reconnect_flag = ReadDatabase(sql_1)[0][0]
			print("reconnect_flag:",reconnect_flag)

			reconnect_count = ReadDatabase(sql_1)[0][1]
			print("reconnect_count:",reconnect_count)

			if reconnect_flag == True:
				#os.system("sudo killall python")
				#os.system("screen -L -d -m sudo python /home/atcs-03/Documents/ATCS/Events_API_finals_6.py")
				WriteToDatabase(sql_2.format(reconnect_count))
				#os.system("sudo reboot")
				os.system("sudo python3 /home/{}/Documents/ATCS/reboot.py".format(device_name))

			
			#cam_reconnect_flag = ReadDatabase(cam_reconnect_1)[0][0]      #HARSHAD
			#print("cam_reconnect_flag:",cam_reconnect_flag)

			#cam_reconnect_count = ReadDatabase(cam_reconnect_1)[0][1]
			#print("cam_reconnect_count:",cam_reconnect_count)
			#time.sleep(0.1)



			#if cam_reconnect_flag == True:

				#time.sleep(0.1)
				#os.system("sudo screen -X -S Camera quit")
				#time.sleep(0.1)
				#os.system("sudo screen -X -S Detector quit")
				#print("::::::::::::::::::::::::::::::::::::::::::::Detector Killed::::::::::::::::::::::::::::::::::::::::")
				#time.sleep(.5)
				#WriteToDatabase(cam_reconnect_2.format(cam_reconnect_count))
				#time.sleep(1)
				#os.system("sudo screen -S Detector -d -m /home/{}/Documents/ATCS/ATCS_GMC_DetectorRawData/publish/ATCS_GMC_DetectorRawData".format(device_name))
				#time.sleep(0.1)
				#os.system("sudo screen -S Camera -d -m /home/{}/Documents/ATCS/ATCS_GMC_CameraRawData/publish/ATCS_GMC_CameraRawData".format(device_name))
				#print("::::::::::::::::::::::::::::::::::::::::::::Detector Started::::::::::::::::::::::::::::::::::::::::")        #HARSHAD
		except Exception as e:
			print("Error in reconnect_junction function::", e)


# This whole function will take timing slots of regular plan with priority_flag = 0 which means not to take plan which is set from 
# dashboard and today_date variable will be date of latest available data(regular plans) in database.


def CheckDatabase():

	global total_stage
	global modeid
	global update_flag
	global va_timing_slots
	global va_stage_skip_timing_slots     #new mode 23-03-2023 for mode 8
	global sva_stage_skip_timing_slots    # new mode 23-03-2023 for mode 9
	global va_offset_timing_slots
	global sva_timing_slots
	global fix_timing_slots
	global fix_offset_timing_slots
	global atcs_timing_slots 
	global event_timing_slots
	global today_date # For fetching plan of only one date (today_date)
	global mode_flag
	global mode_id
	global modeid
	global current_seq_no
	global event_mode
	global va_conditions
	global va_offset_conditions
	global sva_conditions
	global fix_conditions
	global fix_offset_conditions
	global atcs_conditions
	global event_conditions
	global blinker_conditions
	global va_stage_skip_conditions    # new mode 23-03-2023 mode-8
	global sva_stage_skip_conditions   # new mode 23-03-2023 mode-9
	global prevous_priority
	global ar_flag
	global condition_flag
	global priority_flag
	global condition_count

	va_timing_slots = {}
	va_stage_skip_timing_slots = {}  # new mode 23-03-2023 mode-8
	sva_stage_skip_timing_slots = {}  # new mode 23-03-2023 mode-9
	va_offset_timing_slots = {}
	sva_timing_slots = {}
	fix_timing_slots = {}
	fix_offset_timing_slots = {}
	atcs_timing_slots = {}
	event_timing_slots = {}
	blinker_timing_slots = {}
	
	offset_day = 1 # for previous plans if no latest plan available
	today_date = date.today() - timedelta(days=offset_day)# For comparision with previous day for  plandate 
	# va_flag = 0
	mode_flag = 0
	# event_flag = 0
	event_sequence_flag_2 = 1
	priority_flag = 0 # Increment flag in Database( Only use when mode and sequence change from dashboard ( it will be zero in case of regular day plan.))
	current_priority = 1 # just comparing in if conditions of event_conditions
	prevous_priority = 0
	modeid = 5
	
	while  True:
		if(update_flag == 1): # If Sequence is not updated in the controller then restart the Checkdatabase function
			update_flag = 0
			print("Breaking the checkdatabase loop...............", update_flag)
			break
		else:
			update_flag = 0
#---------------------------Run Regular Plan-----------------------------------#
		try:
			print("Plan_Date-------",today_date)
			sql1 = "SELECT plandate from atcs.daywise_planoperations WHERE plandate > '{}' and priorityflag = {}"
			sql2 = "SELECT MAX(stageid) from atcs.daywise_planoperations WHERE slotno = '{}' and plandate = '{}'"
			sql4 = "SELECT slotno, fromtime::time, totime::time, modeid from atcs.daywise_planoperations WHERE priorityflag = '{}' and plandate = '{}'"
			#sql8 = "SELECT slotno, fromtime::time, totime::time, modeid from atcs.daywise_planoperations WHERE onetimeflag = '{}' and plandate = '{}'"
			sql6 = "SELECT slotno from atcs.daywise_planoperations WHERE priorityflag = '{}' and plandate = '{}'"
			sql7 = "SELECT coalesce(MAX(priorityflag),0) from atcs.daywise_planoperations WHERE plandate = '{}'"
			
			today_b = ReadDatabase(sql1.format(today_date,priority_flag)) # Priority flag zero means only regular day plan not plan from live dashboard.
			# print(result)
			if( len(today_b) > 0 ): # check date if changed (this should be true at midnight)

				today_date = today_b[0][0]
				#mode_flag = 0   
				priority_flag = 0
				event_timing_slots = {} # Changes from dashboard e.g, Mode Changed, Hurry call, Reconnect, etc.
				
				total_stage = ReadDatabase(sql2.format(1,today_date))[0][0] # total stage for slot 1.
				
				res1 = ReadDatabase(sql4.format(0,today_date))

				if(len(res1)>0 and (OTA_flag != 1)):			#krusha
					va_timing_slots = {}
					va_stage_skip_timing_slots = {}  # new mode 23-03-2023 mode-8
					sva_stage_skip_timing_slots = {}  # new mode 23-03-2023 mode-9
					va_offset_timing_slots = {}
					sva_timing_slots = {}
					fix_timing_slots = {}
					fix_offset_timing_slots = {}
					blinker_timing_slots = {}
					atcs_timing_slot = {}

					for row in res1:

						slotno = str(row[0])
						fromtime = str(row[1])
						totime = str(row[2])
						totime  =  totime[:6] + '58'
						mode_id = str(row[3])
					
						if(int(mode_id) == 1):
							fix_timing_slots[slotno] = []
							fix_timing_slots[slotno].append(fromtime)
							fix_timing_slots[slotno].append(totime)

						if(int(mode_id) == 2):
							va_timing_slots[slotno] =[]
							va_timing_slots[slotno].append(fromtime)
							va_timing_slots[slotno].append(totime)

						if(int(mode_id) == 3):
							sva_timing_slots[slotno] = []
							sva_timing_slots[slotno].append(fromtime)
							sva_timing_slots[slotno].append(totime)

						if(int(mode_id) == 4):
							atcs_timing_slots[slotno] = []
							atcs_timing_slots[slotno].append(fromtime)
							atcs_timing_slots[slotno].append(totime)
							
						if(int(mode_id) == 5):
							blinker_timing_slots[slotno] = []
							blinker_timing_slots[slotno].append(fromtime)
							blinker_timing_slots[slotno].append(totime)
							
						if(int(mode_id) == 6):
							va_offset_timing_slots[slotno] =[]
							va_offset_timing_slots[slotno].append(fromtime)
							va_offset_timing_slots[slotno].append(totime)
							
						if(int(mode_id) == 7):
							fix_offset_timing_slots[slotno] = []
							fix_offset_timing_slots[slotno].append(fromtime)
							fix_offset_timing_slots[slotno].append(totime)

						if (int(mode_id) == 8):        # new mode 23-03-2023
							va_stage_skip_timing_slots[slotno] = []
							va_stage_skip_timing_slots[slotno].append(fromtime)
							va_stage_skip_timing_slots[slotno].append(totime)

						if (int(mode_id) == 9):       # new mode 23-03-2023
							sva_stage_skip_timing_slots[slotno] = []
							sva_stage_skip_timing_slots[slotno].append(fromtime)
							sva_stage_skip_timing_slots[slotno].append(totime)

				print("VA timings:",va_timing_slots)
				print("va offset timing:",va_offset_timing_slots)
				print("SVA timings:",sva_timing_slots)
				print("Fix timings:",fix_timing_slots)
				print("fix offset timing:",fix_offset_timing_slots)
				print("ATCS timings:",atcs_timing_slots)
				print("BLINKER timings:",blinker_timing_slots)
				print("VA With STAGE SKIP timings:", va_stage_skip_timing_slots)  #new mode 23-03-2023
				print("SVA With STAGE SKIP timings:", sva_stage_skip_timing_slots) #new mode 23-03-2023

			#----- It will decrease value of today_date until we don't get timing of fix, va and sva ------#   krusha
			elif(len(sva_stage_skip_timing_slots) == 0 and len(va_stage_skip_timing_slots) == 0 and len(va_timing_slots) == 0 and len(sva_timing_slots) == 0 and len(fix_timing_slots) == 0 and len(atcs_timing_slots) == 0 and len(blinker_timing_slots) == 0 and len(va_offset_timing_slots) == 0 and len(fix_offset_timing_slots) == 0 and (OTA_flag != 1)):

				today_date = date.today() - timedelta(days=offset_day)# For comparision with previous day for  plandate
				offset_day += 1 # for previous plans if no latest plan available
				print("offset_day.............",offset_day)

			today_date_event = date.today()
			max_priority = ReadDatabase(sql7.format(today_date_event))[0][0]
			print("Max priority :",max_priority)
			print("priority flag :",priority_flag)
			
			if(priority_flag < max_priority):

				for i in range(priority_flag,int(max_priority)):

					priority_flag += 1
					# print("priorityflag------------------",priority_flag)
					res2 = ReadDatabase(sql4.format(priority_flag,today_date_event))	

					if(len(res2)>0):

						print("Got Events flag set---------priority",priority_flag)
						
						event_timing_slots[priority_flag] = []
						row = res2[0]							
						slotno = str(row[0])
						event_start_time = str(row[1])
						event_end_time = str(row[2])
						mode_id = str(row[3])
						print("Event mode_id---------",mode_id)
						event_timing_slots[priority_flag].append(mode_id)
						event_timing_slots[priority_flag].append(event_start_time)
						event_timing_slots[priority_flag].append(event_end_time)

				print(event_timing_slots)

			else:
				print("No result from querry...................")

			fix_conditions,slt1 = check_conditions(fix_timing_slots)
			va_conditions,slt2 = check_conditions(va_timing_slots)
			sva_conditions,slt3 = check_conditions(sva_timing_slots)
			atcs_conditions,slt4 = check_conditions(atcs_timing_slots)
			blinker_conditions,slt5=check_conditions(blinker_timing_slots)
			va_offset_conditions,slt6 = check_conditions(va_offset_timing_slots)
			fix_offset_conditions,slt7 = check_conditions(fix_offset_timing_slots)
			va_stage_skip_conditions,slt8 = check_conditions(va_stage_skip_timing_slots)  # new mode 23-03-2023
			sva_stage_skip_conditions,slt9 = check_conditions(sva_stage_skip_timing_slots)   # new mode 23-03-2023
			event_conditions,current_priority,event_mode = check_event_conditions(event_timing_slots)
	
			print("fix_conditions:",fix_conditions)
			print("va_conditions:",va_conditions)
			print("sva_conditions:",sva_conditions)
			print("atcs_conditions:",atcs_conditions)
			print("Blinker_conditions:",blinker_conditions)
			print("fix_offset_conditions:",fix_offset_conditions)
			print("va_offset_conditions:",va_offset_conditions)
			print("va_stage_skip_conditions:", va_stage_skip_conditions)   #new mode 23-03-2023
			print("sva_stage_skip_conditions:", sva_stage_skip_conditions)  # new mode 23-03-2023
			print("event_conditions:",event_conditions)
			print("mode_flag : ",mode_flag)
			print("Current_time:", time.strftime("%Y-%m-%d %H:%M:%S"))

			# if(ar_flag == 1 and event_conditions): 
			# 	ar_flag = 0
			# 	print("Controller Reboot and resetting ar_flag")
			# 	write_to_serial("reboot#")
			
			#else:
				#fix_conditions = False
				#va_conditions = False
				#sva_conditions = False
				#atcs_conditions = False
				#Blinker_conditions = True
				#fix_offset_conditions = False
				#va_offset_conditions = False
				#event_conditions = False
				#print("ELSE:::::::::::>>>>>>>>>>>>>>>>>>>:::::::::::::>>>>>>>>>>>>>>>>>")
				#print("fix_conditions:",fix_conditions)
				#print("va_conditions:",va_conditions)
				#print("sva_conditions:",sva_conditions)
				#print("atcs_conditions:",atcs_conditions)
				#print("Blinker_conditions:",blinker_conditions)
				#print("fix_offset_conditions:",fix_offset_conditions)
				#print("va_offset_conditions:",va_offset_conditions)
				#print("event_conditions:",event_conditions)
				#print("mode_flag : ",mode_flag)
				#print("Current_time:", time.strftime("%Y-%m-%d %H:%M:%S"))

			if(fix_conditions == False and va_conditions == False and sva_conditions == False and atcs_conditions == False and blinker_conditions == False and va_offset_conditions == False and fix_offset_conditions == False and va_stage_skip_conditions == False and sva_stage_skip_conditions == False and event_conditions == False):
				condition_flag += 1
				time.sleep(1)
				print("condition_flag...",condition_flag)
				if(condition_flag == 20 and condition_count < 2):
					condition_count += 1
					print("Enter in forcefully Blinker mode...........")
					querry = "SELECT count(1) as totalarm from atcs.global_configurations;"
					totalarm = ReadDatabase(querry)[0][0]
					time.sleep(0.05)
					write_to_serial("?AA5#")
					time.sleep(0.2)
					write_to_serial("?AA5#")
					time.sleep(0.2)
					write_to_serial("$" + chr(1) + chr(2)  + "#")#+ chr(0) + chr(0) + chr(2) + "#")
					time.sleep(0.2)
					# write_to_serial("$01002#")
					write_to_serial("$" + chr(1) + chr(2)  + "#")
					# write_to_serial("$" + chr(0) + chr(1) + chr(0) + chr(0) + chr(2) + "#")
					for i in range(1,totalarm+1):
						seq = "@"+chr(i)+chr(0)+chr(1)+chr(1)+chr(2)+chr(1)+chr(1)+chr(1)+chr(1)+chr(1)+chr(1)+chr(1)+chr(1)+"#"  #format(chr(int(i)))
						print("blinker_hardcoded_Sequence",seq.encode())
						write_to_serial(seq)
						time.sleep(0.01)
					
					time.sleep(0.1)

					for i in range(1,totalarm+1):
						seq = "@"+chr(i)+chr(0)+chr(1)+chr(1)+chr(2)+chr(1)+chr(1)+chr(1)+chr(1)+chr(1)+chr(1)+chr(1)+chr(1)+"#"  #format(chr(int(i)))
						print("blinker_hardcoded_Sequence",seq.encode())
						write_to_serial(seq)
						time.sleep(0.01)
					write_to_serial("?AA5#")
					condition_flag = 0	
			else: 
				condition_flag = 0
				condition_count = 0

			if(event_conditions):  # If there will be Some Event Condition.
				#if(current_priority > prevous_priority):#So it will not execute again and again or execute for greater priority only.
				if(current_priority != prevous_priority):
					mode_flag = 0
					prevous_priority = current_priority

					slot = ReadDatabase(sql6.format(current_priority,today_date_event))[0][0]

					handle_mode_change(slot,today_date_event,event_mode)

			else:   # Regular Plan  

				if((va_conditions or sva_conditions) and (mode_flag == 0)):  
				
					if(va_conditions):  # For Mode-2
						
						handle_mode_change(slt2,today_date,mode_id=+--2)

					else:  # For Mode-3
						
						handle_mode_change(slt3,today_date,mode_id=3)

				if((fix_conditions or atcs_conditions) and (mode_flag == 0)):

					if(fix_conditions): # For Mode-1
					
						handle_mode_change(slt1,today_date,mode_id=1)

					else:  # For Mode-4
 							
 						handle_mode_change(slt4,today_date,mode_id=4)

					
				if(blinker_conditions and (mode_flag == 0)): #For Mode-5
					
					handle_mode_change(slt5,today_date,mode_id=5)
					
				if((fix_offset_conditions or va_offset_conditions) and (mode_flag == 0)):

					if(fix_offset_conditions): # For Mode-7
					
						handle_mode_change(slt7,today_date,mode_id=7)

					else: # For Mode-6
 							
 						handle_mode_change(slt6,today_date,mode_id=6)

				if ((va_stage_skip_conditions or sva_stage_skip_conditions) and (mode_flag == 0)):    # Added by HARSHAD 17-03-2023

					if (va_stage_skip_conditions):  # For Mode-8

						handle_mode_change(slt8, today_date, mode_id=8)

					else:  # For Mode-9

						handle_mode_change(slt9, today_date, mode_id=9)

			time.sleep(1)			
			
		except Exception as e :
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)

def blinkmode_mode():

	global mode_flag
	global controller_reboot
	global power_on
	global start_exe_flag

	mode_flag = 1
	time.sleep(3)
	print("Blinker conditions.....",blinker_conditions)

	while ((blinker_conditions or  event_conditions) and mode_flag):
		if(int(controller_reboot) or int(power_on)):
			controller_reboot = '00'
			power_on = '00'
		
		if(int(start_exe_flag) == 0):
			start_exe_flag = 1

		time.sleep(3)

	mode_flag = 0

def fix_mode():

	global mode_flag
	global controller_reboot
	global power_on
	global start_exe_flag

	mode_flag = 1
	time.sleep(3)
	
	while ((fix_conditions or  event_conditions) and mode_flag):
		
		if(int(controller_reboot) or int(power_on)):
			controller_reboot = '00'
			power_on = '00'
		
		if(int(start_exe_flag) == 0):
			start_exe_flag = 1

		time.sleep(3)

	mode_flag = 0	


def atcs_mode():
		
		print("Enter in ATCS Function--------------")
		time.sleep(1)
		global list_total_cycle_from_db
		global list_split_time_from_db
		global list_atcs_time_from_db
		global tmp_total_cycle 
		global mode_flag
		global event_mode
		global split_cylce
		global atcs_exe_flag
		mode_flag = 1

		sql_reset_updation_flag = "UPDATE atcs.adaptiveoutputdata SET updationflag = %s WHERE updationflag = %s"
		WriteToDatabase(sql_reset_updation_flag,True,False)
		while ((atcs_conditions or  event_conditions) and mode_flag):
			sqladf="SELECT updationflag from atcs.adaptiveoutputdata limit 1" 
			updatflg = ReadDatabase(sqladf)
			print(updatflg[0][0])

			print("Event mode",event_mode)
			if((event_mode != 4 and  event_mode != 6 and event_mode != 7 and event_mode > 0) or atcs_exe_flag == 1):
				print("atcs_exe_flag inside the Loop2", atcs_exe_flag)
				atcs_exe_flag = 0
				break
				
			if(updatflg[0][0]== True):
				list_total_cycle_from_db = []  
				list_atcs_time_from_db = []   
				list_split_time_from_db = []   
				
				get_atcs_data_from_db()
				
				sql_reset_updation_flag = "UPDATE atcs.adaptiveoutputdata SET updationflag = %s WHERE updationflag = %s"
				WriteToDatabase(sql_reset_updation_flag,False,True)
				
				sqladf="SELECT updationflag from atcs.adaptiveoutputdata limit 1" # Updated By Amit
				updatflg = ReadDatabase(sqladf)
				print("updatflg flag:----------",updatflg)
				
				print("list_total_cycle_from_db", list_total_cycle_from_db)
				print("list_split_time_from_db", list_split_time_from_db)
				print("list_atcs_time_from_db", list_atcs_time_from_db)
				print ("Total Cycle Count From data base----: ",list_total_cycle_from_db[0])

				split_cylce = list_total_cycle_from_db[0]

			if(int(list_total_cycle_from_db[0]) == 0 or split_cylce == 0):
				global tmp_atcs_stage  
				print("List of ATCS Time : ",list_atcs_time_from_db)
				
				tmp_atcs_stage = 0

				sql_arm_no = "SELECT COUNT(armno) AS armno from atcs.global_configurations"

				arm_at_junc = ReadDatabase(sql_arm_no)[0][0]

				stage_at_junc = arm_at_junc * 2

				print("arm_at_junc::",arm_at_junc , "stage_at_junc:::", stage_at_junc)
				while(tmp_atcs_stage < stage_at_junc):
					if((event_mode != 4 and event_mode != 6 and event_mode != 7 and event_mode > 0) or atcs_exe_flag == 1):
						atcs_exe_flag = 0
						print("atcs_exe_flag inside the Loop2", atcs_exe_flag)
						break
					write_to_serial("1,0" + str(int(tmp_atcs_stage)) + "#")
					print("Stage : ",tmp_atcs_stage ,"ATCS Timing : ",list_atcs_time_from_db[tmp_atcs_stage])

					atcs_time_1 = int(list_atcs_time_from_db[tmp_atcs_stage])

					try:
						wait(lambda : False, timeout_seconds=atcs_time_1)
					except TimeoutExpired:
						pass

					tmp_atcs_stage += 1
					
					if(tmp_atcs_stage == (stage_at_junc - 1) ):
						break
			
			elif (int(list_total_cycle_from_db[0]) > 0 and split_cylce > 0):
				global tmp_split_stage  

				tmp_split_stage = 0

				split_cylce = list_total_cycle_from_db[0]

				sql_arm_no = "SELECT COUNT(armno) AS armno from atcs.global_configurations"

				arm_at_junc = ReadDatabase(sql_arm_no)[0][0]
				
				stage_at_junc = arm_at_junc * 2

				print("arm_at_junc::",arm_at_junc, "stage_at_junc:",stage_at_junc)

				while(tmp_atcs_stage < stage_at_junc):
					if((event_mode != 4 and  event_mode != 6 and event_mode != 7 and event_mode > 0) or atcs_exe_flag == 1):
						atcs_exe_flag = 0
						print("atcs_exe_flag inside the Loop2", atcs_exe_flag)
						break
					write_to_serial("1,0" + str(int(tmp_split_stage)) + "#")
					print("Stage : ",tmp_split_stage ,"Split Timing : ",list_split_time_from_db[tmp_split_stage])

					atcs_time_2 = int(list_split_time_from_db[tmp_split_stage])
					try:
						wait(lambda : False, timeout_seconds=atcs_time_2)
					except TimeoutExpired:
						pass

					tmp_split_stage += 1
					
					if(tmp_split_stage == (stage_at_junc - 1)):
						if split_cylce > 0:
							split_cylce -= 1
						break
# For exceptional handling #
		if((event_mode != 4 and  event_mode != 6 and event_mode != 7 and event_mode > 0) or atcs_exe_flag == 1):
			mode_flag = 1
		else:	
			mode_flag = 0

def va_sva_mode(id,slot,today_date):

	global mode_flag
	global start_exe_flag
	global controller_reboot
	global power_on
	global killexe

	print("//////////Entered in VA_SVA functions////////////////////////")

	sql_va_time = "SELECT currentstage from atcs.va_operations WHERE (totaloffsetflag = '{}')".format(1)# and (controllercode == {}))".format(controller_id)
	sql_reset_time_flag = "UPDATE atcs.va_operations SET totaloffsetflag = %s WHERE totaloffsetflag = %s"
	reset_flag  = "UPDATE atcs.va_operations SET timeflag = false"

	mode_flag = 1
	stage_9_flag = 0
	detector_fault_err_count = 0
	killexe = 0

	WriteToDatabase(sql_reset_time_flag,0,1)

	write_to_serial("1,00#")

	threading.Thread(target=start_va_sva_logic,args=(id,slot,today_date,)).start()
	print("Currently in VA SVA functions....")
	
	tmp_current_stage = 1
	
	while ((va_conditions or sva_conditions or event_conditions ) and mode_flag):

		if(int(controller_reboot) or int(power_on)):
			controller_reboot = '00'
			power_on = '00'
		
		if(int(start_exe_flag) == 0):
			start_exe_flag = 1

		try:
			row = ReadDatabase(sql_va_time)
			if(len(row)>0):
				print("Got changed in VA time at "+time.strftime('%d-%m-%Y %H:%M:%S')+"-------------")

				print(row[0])

				write_to_serial("1,0" + str(int(row[0][0])-1) + "#")

				tmp_current_stage = int(row[0][0])
				
				WriteToDatabase(sql_reset_time_flag,0,1)
					
		except Exception as e:
			print(e)
			
	print("Exiting VA_SVA Mode-----------------------")
	os.system("sudo killall -9 ATCS_GMC_NewVALogic")
	os.system("sudo killall -9 ATCS_GMC_NewVAWithBRTLogic") # Kill VA Exe if running.(mileen)
	mode_flag = 0
	WriteToDatabase(sql_reset_time_flag,0,1)
	

def start_va_sva_logic(id,slotno,date):# this Function is for both VA and SVA
	
	global exe_status_flag
	global seqid
	
	sql99 = "SELECT distinct sequenceid FROM atcs.daywise_planoperations WHERE slotno = '{}' and plandate = '{}'"
	seqid = ReadDatabase(sql99.format(slotno,date))[0][0]


	if(id == 3): # SVA mode
		if (seqid == 9999999):
    			print("started with seq 9999999 mode 3",seqid)
    			os.system("/home/{}/Documents/ATCS/ATCS_GMC_VALogic/publish/ATCS_GMC_NewVALogic 3 1 3".format(device_name))
		else :
    			print("started with seq default mode 3",seqid)
    			os.system("/home/{}/Documents/ATCS/ATCS_GMC_NewVAWithBRTLogic/publish/ATCS_GMC_NewVAWithBRTLogic 3 1 3".format(device_name))
				
	

	if(id == 2): # VA mode
		if (seqid == 9999999):
    			print("started with seq 9999999 mode 2",seqid)
    			os.system("/home/{}/Documents/ATCS/ATCS_GMC_VALogic/publish/ATCS_GMC_NewVALogic 2".format(device_name))
				
		else :
    			print("started with seq default mode 2",seqid)
    			os.system("/home/{}/Documents/ATCS/ATCS_GMC_NewVAWithBRTLogic/publish/ATCS_GMC_NewVAWithBRTLogic 2".format(device_name))
				

	if(id == 8): # VA with stage_skip mode 23-03-2023
		if (seqid == 9999999):
    			print("started with seq 9999999 mode 8",seqid)
    			os.system("/home/{}/Documents/ATCS/ATCS_GMC_VAWithStageSkipLogic/publish/ATCS_GMC_VAWithStageSkipLogic 2".format(device_name))
		else :
    			print("started with seq default mode 8",seqid)
    			os.system("/home/{}/Documents/ATCS/ATCS_GMC_VAWithStageSkipLogic/publish/ATCS_GMC_VAWithStageSkipLogic 4".format(device_name))
	
	if(id == 9): # SVA with stage_skip mode 23-03-2023
		if (seqid == 9999999):
    			print("started with seq 9999999 mode 9",seqid)
    			os.system("/home/{}/Documents/ATCS/ATCS_GMC_VAWithStageSkipLogic/publish/ATCS_GMC_VAWithStageSkipLogic 3".format(device_name))
		else :
    			print("started with seq default mode 9",seqid)
    			os.system("/home/{}/Documents/ATCS/ATCS_GMC_VAWithStageSkipLogic/publish/ATCS_GMC_VAWithStageSkipLogic 5".format(device_name))

	print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@sqid@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",seqid,id,slotno)




def start_camera_raw_data():
	#os.system("sudo killall -9 ATCS_GMC_CameraRawData")
	time.sleep(1)
	# os.system(os.path.abspath("ATCS_GMC_CameraRawData/publish/ATCS_GMC_CameraRawData"))
	os.system("screen -S Detector -L -d -m sudo /home/{}/Documents/ATCS/ATCS_GMC_Detector/publish/ATCS_GMC_DetectorRawData".format(device_name))
	time.sleep(1)
	os.system("screen -S Camera -L -d -m sudo /home/{}/Documents/ATCS/ATCS_GMC_Camera/publish/ATCS_GMC_CameraRawData".format(device_name))


def start_console_data():
	time.sleep(2)
	os.system("/home/{}/Documents/ATCS/ATCS_GMC_Console/publish/ATCS_GMC_Console".format(device_name))

def get_atcs_data_from_db():

	global list_total_cycle_from_db
	global list_split_time_from_db
	global list_atcs_time_from_db    

	sql5 = "SELECT* from atcs.adaptiveoutputdata where updationflag = true;"
	
	res2 = ReadDatabase(sql5.format(0,date.today()))
	if(len(res2)>0):
 		for row in res2:
 			list_total_cycle_from_db.append((row[4]))
 			list_split_time_from_db.append(str(row[2]))
 			list_atcs_time_from_db.append(str(row[3]))
	 	return list_total_cycle_from_db , list_split_time_from_db , list_atcs_time_from_db
	 	
 	
def write_to_serial(data):
	global respond_flag
	global ser

	if(OTA_flag != 1):				#krusha
		
		ser.write(data.encode())

		#ser.flushOutput()
		d_q_sqser = "DELETE from atcs.send_serialtomasterlog WHERE createdon < (now() - interval '2 days')"
		WriteToDatabase(d_q_sqser)
		sqserial = "INSERT INTO atcs.send_serialtomasterlog (serial_data, createdon ) VALUES(%s,%s)"
		WriteToDatabase(sqserial, str(data), time.strftime('%Y-%m-%d %H:%M:%S'))
		print(data,"data send to controller")
	time.sleep(0.11)   #jds
	#time.sleep(1)


def format_byte(a,l): # This used to add extra 0 to make fixed byte as decided

	if(len(a)<l):
		b = a
		while (len(b) != l):
			b = '0'+ b
		return b
	else:
		return a

def check_ramaining_stage_in_previous_mode(modeid):

	print("checking previous mode-----------")
	print("current_mode.............", current_mode)
	print("modeid.........", modeid)

	if(int(current_mode) == modeid):
		if((int(current_mode) == 4 and  modeid == 4) or (int(current_mode) == 6 and  modeid == 6) or (int(current_mode) == 7 and  modeid == 7) ):
			check_remaining_for_atcs(int(current_stage_no)+1)
		else:
			send_remaining_stage_time(int(current_stage_no)+1)
		return 1
	else:
		return 1

def check_remaining_for_atcs(tmp_current_stage):

	global controller_reboot
	global power_on

	even_stage_time = 15
	print("*******controller_reboot : ",controller_reboot," power_on : ",power_on) # skip thesupdate_flage processes if controller reboots.

	while(tmp_current_stage <= int(total_stage)):
		print("Enter in Manual completing cycle condition......")

		write_to_serial("1,0" + str(int(tmp_current_stage)-1) + "#") # Because stage accepted from controllers starts from 0 thats why we've to subtract 1
		
		if((tmp_current_stage % 2) == 0):
			time.sleep(3)
		else:
			time.sleep(even_stage_time)

		tmp_current_stage += 1
		print("*******controller_reboot : ",controller_reboot," power_on : ",power_on)

	controller_reboot = '00'
	power_on = '00'

def check_hc_events():
	while(HC_Flag == 1):
		print("waiting to completing hurrycall")
		time.sleep(0.1)
		

def send_remaining_stage_time(tmp_current_stage):

	global controller_reboot
	global power_on

	even_stage_time = 15
	print("*******controller_reboot : ",controller_reboot," power_on : ",power_on)# skip these processes if controller reboots.

	while ((tmp_current_stage <= int(total_stage)) and (int(controller_reboot) == 0) and (int(power_on) == 0) and (int(current_stage_no)) and (int(start_exe_flag))):
		print("Enter in Manual completing cycle condition......")

		write_to_serial("1,0" + str(int(tmp_current_stage)-1) + "#") # Because stage accepted from controllers starts from 0 thats why we've to subtract 1
		 
		if((tmp_current_stage % 2) == 0):
			time.sleep(3)
		else:
			time.sleep(even_stage_time)

		tmp_current_stage += 1
		print("*******controller_reboot : ",controller_reboot," power_on : ",power_on)

	controller_reboot = '00'
	power_on = '00'

def invert(a): # For controller because it needs invert value in sequence strings.
	if(int(a) == 0):
		return 1
	elif(int(a) == 1):
		return 0
	else:
		return a

def brt_invert(a): # For controller because it needs invert value in sequence strings.
	if(int(a) == False):
		return 0
	elif(int(a) == True):
		return 1
	elif(int(a) == None):
		return 0
	else:
		return a

def check_n_send_global_variables():
	sql5 = "SELECT 	autoswitchtime,juncon_amberflash,juncon_amberpriority,juncon_amberseconds,\
					juncon_redflash,juncon_redpriority,juncon_redseconds,modechange_amberflash,modechange_amberpriority,modechange_amberseconds,\
					modechange_redflash,modechange_redpriority,modechange_redseconds\
    				from atcs.global_configurations limit 1;"
	res1 = ReadDatabase(sql5)
	print(res1)             
	if(len(res1) == 0 or res1[0][2] == None):	
		print("Global Data not found in database...")
		autotimeout = int(5) #'005' #format_byte(str(res1[0][0]),3)#print(autotimeout)
		jun_aflash = int(1)  # flash on/off cmd (mileen)
		jun_aprio  =  int(1) #'001' #format_byte(str(res1[0][2]),3)#globalcon[0][2]
		jun_asec   = int (3) #'003' #format_byte(str(res1[0][3]),3)#globalcon[0][3]
		jun_rflash = int(1)  # flash on/off cmd (mileen)
		jun_rprio  = int (2) #'002' #format_byte(str(res1[0][5]),3)#globalcon[0][5]
		jun_rsec   = int (3) #'003' #format_byte(str(res1[0][6]),3)#globalcon[0][6]
		mod_aflash = int(1)  # flash on/off cmd (mileen)
		mod_aprio  = int (1) #'001' #format_byte(str(res1[0][8]),3)#globalcon[0][8]
		mod_asec   =  int(3) #'003' #format_byte(str(res1[0][9]),3)#globalcon[0][9]
		mod_rflash = int(1)  # flash on/off cmd (mileen)
		mod_rprio  =  int(2) #'002' #format_byte(str(res1[0][11]),3)#globalcon[0][11]
		mod_rsec   =  int(3) #'003' #format_byte(str(res1[0][12]),3)#globalcon[0][12]
		
	else:
		autotimeout = (res1[0][0])  #format_byte(str(res1[0][0]),3)#print(autotimeout)
		jun_aflash = (res1[0][1])   #flash on/off cmd (mileen)
		jun_aprio  =  (res1[0][2])  #format_byte(str(res1[0][2]),3)#globalcon[0][2]
		jun_asec   =  (res1[0][3])  #format_byte(str(res1[0][3]),3)#globalcon[0][3]
		jun_rflash = (res1[0][4])   #flash on/off cmd (mileen)
		jun_rprio  =  (res1[0][5])  #format_byte(str(res1[0][5]),3)#globalcon[0][5]
		jun_rsec   =  (res1[0][6])  #format_byte(str(res1[0][6]),3)#globalcon[0][6]
		mod_aflash = (res1[0][7])   #flash on/off cmd (mileen)
		mod_aprio  =  (res1[0][8])  #format_byte(str(res1[0][8]),3)#globalcon[0][8]
		mod_asec   =  (res1[0][9])  #format_byte(str(res1[0][9]),3)#globalcon[0][9]
		mod_rflash = (res1[0][10])  #flash on/off cmd (mileen)
		mod_rprio  =  (res1[0][11]) #format_byte(str(res1[0][11]),3)#globalcon[0][11]
		mod_rsec   =  (res1[0][12]) #format_byte(str(res1[0][12]),3)#globalcon[0][12]

	querry = "SELECT eventid,datanotreceived_min FROM atcs.incident_master"
	res = ReadDatabase(querry)
	arm_health  = (5) #'005'
	lamp_health  = (25) #'025'
	counter_health = (10) #'010'
	
	for row in res:

		if(int(row[0]) == 18):#Arm Health
			if (row[1])> 125:
				arm_health = int(125)
			else:
				arm_health = (row[1]) #format_byte(str(row[1]),3)
		print("arm_health....",arm_health)

		if(int(row[0]) == 20):#Controller Health
			controller_health = (row[1]) #str(row[1])
			#print("controller_health....",str(row[1]))

		if(int(row[0]) == 15):#Lamp Health
			if (row[1]) > 125:
				lamp_health = (125)
			else:
				lamp_health = (row[1]) #format_byte(str(row[1]),3)
		print("lamp_health....",lamp_health)

		if(int(row[0]) == 5):#Detector Health
			detector_health = (row[1]) #str(row[1])

		if(int(row[0]) == 16):#Counter Health
			if (row[1]) > 125:
				counter_health = int(125)
			else:
				counter_health = (row[1]) #format_byte(str(row[1]),3)
		print("counter_health....",counter_health)

	#counter_health = chr(25)

	#glob_config = "%,"+chr(arm_health)+chr(lamp_health)+chr(counter_health)+chr(autotimeout)+chr(jun_aprio)+chr(jun_asec)+chr(jun_rprio)+chr(jun_rsec)+chr(mod_aprio)+chr(mod_asec)+chr(mod_rprio)+chr(mod_rsec)+chr(jun_rflash)+chr(jun_aflash)+chr(mod_rflash)+chr(mod_aflash)+",#"
	glob_config = "%," + chr(arm_health) + chr(lamp_health) + chr(counter_health) + chr(autotimeout) + chr(
		jun_aprio) + chr(jun_asec) + chr(jun_rprio) + chr(jun_rsec) + chr(mod_aprio) + chr(mod_asec) + chr(
		mod_rprio) + chr(mod_rsec) + chr(jun_rflash) + chr(jun_aflash) + chr(mod_rflash) + chr(mod_aflash) + ",#"
	print(str(glob_config))
	write_to_serial(glob_config)


def check_detector_health():
	global detector_health_flag
	sql1 = "select (now() - insertedtime)::interval > '{} minutes'::interval,ipaddress,armno from atcs.camerarawdata where \
			ipaddress = '{}'  order by insertedtime desc limit 1"
	sql2 = "SELECT datanotreceived_min FROM atcs.incident_master WHERE eventid = {}"

	time_interval = ReadDatabase(sql2.format(5))[0][0]
	
	for i in range(len(detector_ip)):
		res = ReadDatabase(sql1.format(str(time_interval),detector_ip[i]))
		print(res)

		try:
			if(len(res) <1 or res[0][0]==1):
				if(detector_health_flag[i] == 0): # Because event should be post only one time.
					detector_health_flag[i] = 1
					send_detector_events((i+1),detector_ip[i],0) #temperory
					print("Detector is not working")
			else:
				detector_health_flag[i] = 0 
				print("detector is working..")

		except Exception as e:
			print(e)
			print(i," : Detector is working.............and Error")


def read_lamp_ids_from_db():

	lamp_ids_list = []
	result = ReadDatabase("SELECT lampcode from atcs.lamp_master")
	for row in result:
		lamp_ids_list.append(row[0])
	return lamp_ids_list


def post_online(url,data,string):

	print(">>>>>>>>>>>>>>>>>>>> Send Data to server >>>>>>>>>>>>>>>")

	global temp_key_from_software
	global token_id
	global final_token

	json_data = {}
	# json_data1 = {}
	# headers1 = {'content-type' : 'application/json'}
	# json_data1 = {"username":urname,"password":passwrd}
	# data1=json.dumps(json_data1)
	
	# token_id = requests.post(url=url_login, data=data1, headers=headers1,timeout=10)
	# token = token_id.json()  #print("token>>>>>",token_id.json())
	
	# final_token = str(token['token'])  
	 
	print("Sending over api......",final_token)
	if(data[-1] != '#'):
		data = data + time.strftime('%d%m%Y%H%M%S') + "#"	
	headers = {
	'Authorization' : 'Bearer'+ ' ' + final_token ,
	'content-type' : 'application/json'}
	#print("Headers>>>>", headers)
	json_data[string] = data
	print("Final String := ",data)
	# r = requests.post(url = url, data = msg)
	print(json.dumps(json_data))
	r = requests.post(url=url, data=json.dumps(json_data), headers=headers,timeout=20)
	# pastebin_url = r.text
	pastebin_url = r.json()
	print("The pastebin URL is:%s"%pastebin_url)
#---This is because software team will send unique key in against of each hurry call events which have to respond us during hurry call events--------------#			  
	if(pastebin_url["statusCode"] == 200):
		if(len(pastebin_url["result"].split(",")) == 7):
			print(pastebin_url["result"].split(",")[-1][:-1])
			temp_key_from_software = pastebin_url["result"].split(",")[-1][:-1] #+ "," # Last byte from response from software side.
	

#Read status.txt to close the port for OTA and setting a flag to hold the threading
def OTA():					#krusha				
	global OTA_flag
	global device_name
	close_flag = 2
	while(1):
		
		time.sleep(3)
		fl_name = '/home/{}/Desktop/status.txt'.format(device_name)
		fl = open(fl_name,"r")
		OTA_f = fl.read()
		fl.close()
		if (OTA_f == '1'):
			print('OTA Mode.............................................................................................')
			if(close_flag != 1):
				OTA_flag = 1
				close_flag = 1
				ser.close()
				# threading.Thread(target=OTA_Test).start()

		elif (OTA_f == '0'):

			# print("OTA FLAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGGGGGG............................................................")
			if(close_flag != 0):
				detect_port()				
				OTA_flag = 0
				close_flag = 0
				print("Port connected...............................................................................")
				# threading.Thread(target=OTA_Test).start()
				#threading.Thread(target=read_serial).start()

		# print('Flag')
		# print(OTA_flag)
		# print(OTA_flag)
		# print(OTA_flag)
		# print(OTA_flag)

def Generation_of_Token_id():
	global urname
	global passwrd
	global url_login
	global final_token

	while True:
		try:
			# print("Token Generated..........................................................",final_token)
			json_data = {}
			json_data1 = {}
			headers1 = {'content-type' : 'application/json'}
			json_data1 = {"username":urname,"password":passwrd}
			data1=json.dumps(json_data1)
			
			token_id = requests.post(url=url_login, data=data1, headers=headers1,timeout=10)
			token = token_id.json()  
			# print("token>>>>>",token_id.json())
			
			final_token = str(token['token'])
			print("Token Generated..........................................................",final_token)
			time.sleep(6600)
		except Exception as e:
			print("Error while getting token",e)




if __name__ == "__main__" :
	initialize_detector_health_flag() # This will initialize all value in list(list of flag for each detector) to zero w.r.t set IPs of detector
	detect_port()   # Detect processor port
	os.system("sudo killall -9 ATCS_GMC_CameraRawData")
	os.system("sudo killall -9 ATCS_GMC_NewVALogic")
	os.system("sudo killall -9 ATCS_GMC_NewVAWithBRTLogic") # Kill VA Exe if running.(mileen)
	write_to_serial("reboot#")
	time.sleep(5)
	write_to_serial("slavereboot#")

	threading.Thread(target=Generation_of_Token_id).start()
	threading.Thread(target=start_console_data).start() #added 4/5/2020
	threading.Thread(target=CheckDatabase).start()
	#threading.Thread(target=read_serial).start()
	threading.Thread(target=new_read_serial).start()
	threading.Thread(target=reconnect_junction).start()

	# threading.Thread(target=OTA).start()
	# threading.Thread(target=OTA_Test).start()
