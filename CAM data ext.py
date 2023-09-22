import psycopg2
import serial
import time

# Define the serial port and baud rate for Arduino Nano
serial_port = 'COM5'  # Update this with the correct port
baud_rate = 115200

# Create a serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Wait for the Arduino to initialize
time.sleep(2)
dt = []


try:
    while True:
        data = ser.readline().decode('utf-8').strip()
        if(data!="" and data!="Camera Controller ON"):
            dt = [int(i) for i in data if i!="," and i!="$" and i!="#"]
            break

except KeyboardInterrupt:
    # Close the serial connection when the script is interrupted
    ser.close()
    print("Serial connection closed.")
#print(len(dt))


dt = [1, 3, 2, 1, 2, 2, 0, 0, 0, 0, 3, 1, 2, 0, 0, 4, 2, 2, 2, 0, 5, 0, 0, 0, 0, 6, 1, 2, 0, 0, 7, 1, 1, 0, 0, 8, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0]

cm_dt = dt[40:]
#print(cm_dt)
dt_dict = {
    "arm_id":dt[0:36:5],
    "No_of_Cameras":dt[1:37:5],
    "c1_z":dt[2:38:5],
    "c2_z":dt[3:39:5],
    "c3_z":dt[4:40:5],
    "c1_z1":[0,0,0,0,0,0,0,0],
    "c1_z2":[0,0,0,0,0,0,0,0],
    "c2_z1":[0,0,0,0,0,0,0,0],
    "c2_z2":[0,0,0,0,0,0,0,0],
    "c3_z1":[0,0,0,0,0,0,0,0],
    "c3_z2":[0,0,0,0,0,0,0,0],
}

for arm in range(0,8):

    # For only 1 Camera
    if(dt_dict["No_of_Cameras"][arm] == 1):
        if (dt_dict["c1_z"][arm] == 1):
            dt_dict["c1_z1"][arm]=cm_dt[0]
            cm_dt.remove(cm_dt[0])
        elif(dt_dict["c1_z"][arm] == 2):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c1_z2"][arm] = cm_dt[1]
            cm_dt.remove(cm_dt[0])
            cm_dt.remove(cm_dt[1])

    # For 2 Cameras
    elif(dt_dict["No_of_Cameras"][arm] == 2):
        if (dt_dict["c1_z"][arm] == 1 and dt_dict["c2_z"][arm] == 1):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c2_z1"][arm] = cm_dt[1]
            cm_dt.remove(cm_dt[0])
            cm_dt.remove(cm_dt[1])
        elif(dt_dict["c1_z"][arm] == 2 and dt_dict["c2_z"][arm] == 1):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c1_z2"][arm] = cm_dt[1]
            dt_dict["c2_z1"][arm] = cm_dt[2]
            cm_dt.remove(cm_dt[0])
            cm_dt.remove(cm_dt[1])
            cm_dt.remove(cm_dt[2])
        elif(dt_dict["c1_z"][arm] == 1 and dt_dict["c2_z"][arm] == 2):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c2_z1"][arm] = cm_dt[1]
            dt_dict["c2_z2"][arm] = cm_dt[2]
            cm_dt.remove(cm_dt[0])
            cm_dt.remove(cm_dt[1])
            cm_dt.remove(cm_dt[2])
        elif(dt_dict["c1_z"][arm] == 2 and dt_dict["c2_z"][arm] == 2):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c1_z2"][arm] = cm_dt[1]
            dt_dict["c2_z1"][arm] = cm_dt[2]
            dt_dict["c2_z2"][arm] = cm_dt[3]
            cm_dt.remove(cm_dt[0])
            cm_dt.remove(cm_dt[1])
            cm_dt.remove(cm_dt[2])
            cm_dt.remove(cm_dt[3])

    # For 3 Cameras
    elif(dt_dict["No_of_Cameras"][arm] == 3):
        if (dt_dict["c1_z"][arm] == 1 and dt_dict["c2_z"][arm] == 1 and dt_dict["c3_z"][arm] == 1):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c2_z1"][arm] = cm_dt[1]
            dt_dict["c3_z1"][arm] = cm_dt[2]
        elif (dt_dict["c1_z"][arm] == 1 and dt_dict["c2_z"][arm] == 1 and dt_dict["c3_z"][arm] == 2):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c2_z1"][arm] = cm_dt[1]
            dt_dict["c3_z1"][arm] = cm_dt[2]
            dt_dict["c3_z2"][arm] = cm_dt[3]
            cm_dt.remove(cm_dt[0])
            cm_dt.remove(cm_dt[1])
            cm_dt.remove(cm_dt[2])
            cm_dt.remove(cm_dt[3])
        elif (dt_dict["c1_z"][arm] == 1 and dt_dict["c2_z"][arm] == 2 and dt_dict["c3_z"][arm] == 1):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c2_z1"][arm] = cm_dt[1]
            dt_dict["c2_z2"][arm] = cm_dt[2]
            dt_dict["c3_z1"][arm] = cm_dt[3]
            cm_dt.remove(cm_dt[0])
            cm_dt.remove(cm_dt[1])
            cm_dt.remove(cm_dt[2])
            cm_dt.remove(cm_dt[3])
        elif (dt_dict["c1_z"][arm] == 1 and dt_dict["c2_z"][arm] == 2 and dt_dict["c3_z"][arm] == 2):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c2_z1"][arm] = cm_dt[1]
            dt_dict["c2_z2"][arm] = cm_dt[2]
            dt_dict["c3_z1"][arm] = cm_dt[3]
            dt_dict["c3_z2"][arm] = cm_dt[4]
            cm_dt.remove(cm_dt[0])
            cm_dt.remove(cm_dt[1])
            cm_dt.remove(cm_dt[2])
            cm_dt.remove(cm_dt[3])
            cm_dt.remove(cm_dt[4])
        elif (dt_dict["c1_z"][arm] == 2 and dt_dict["c2_z"][arm] == 1 and dt_dict["c3_z"][arm] == 1):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c1_z2"][arm] = cm_dt[1]
            dt_dict["c2_z1"][arm] = cm_dt[2]
            dt_dict["c3_z1"][arm] = cm_dt[3]
            cm_dt.remove(cm_dt[0])
            cm_dt.remove(cm_dt[1])
            cm_dt.remove(cm_dt[2])
            cm_dt.remove(cm_dt[3])
        elif (dt_dict["c1_z"][arm] == 2 and dt_dict["c2_z"][arm] == 1 and dt_dict["c3_z"][arm] == 2):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c1_z2"][arm] = cm_dt[1]
            dt_dict["c2_z1"][arm] = cm_dt[2]
            dt_dict["c3_z1"][arm] = cm_dt[3]
            dt_dict["c3_z2"][arm] = cm_dt[4]
            cm_dt.remove(cm_dt[0])
            cm_dt.remove(cm_dt[1])
            cm_dt.remove(cm_dt[2])
            cm_dt.remove(cm_dt[3])
            cm_dt.remove(cm_dt[4])
        elif (dt_dict["c1_z"][arm] == 2 and dt_dict["c2_z"][arm] == 2 and dt_dict["c3_z"][arm] == 1):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c1_z2"][arm] = cm_dt[1]
            dt_dict["c2_z1"][arm] = cm_dt[2]
            dt_dict["c2_z2"][arm] = cm_dt[3]
            dt_dict["c3_z1"][arm] = cm_dt[4]
            cm_dt.remove(cm_dt[0])
            cm_dt.remove(cm_dt[1])
            cm_dt.remove(cm_dt[2])
            cm_dt.remove(cm_dt[3])
            cm_dt.remove(cm_dt[4])
        elif (dt_dict["c1_z"][arm] == 2 and dt_dict["c2_z"][arm] == 2 and dt_dict["c3_z"][arm] == 2):
            dt_dict["c1_z1"][arm] = cm_dt[0]
            dt_dict["c1_z2"][arm] = cm_dt[1]
            dt_dict["c2_z1"][arm] = cm_dt[2]
            dt_dict["c2_z2"][arm] = cm_dt[3]
            dt_dict["c3_z1"][arm] = cm_dt[4]
            dt_dict["c3_z2"][arm] = cm_dt[5]
            cm_dt.remove(cm_dt[0])
            cm_dt.remove(cm_dt[1])
            cm_dt.remove(cm_dt[2])
            cm_dt.remove(cm_dt[3])
            cm_dt.remove(cm_dt[4])
            cm_dt.remove(cm_dt[5])
    else:
        continue

db_params = {
    'host': 'localhost',
    'database': 'CAM',
    'user': 'postgres',
    'password': 'postgres'
}

connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

table_name = 'CAM_data'

# Generate column definitions
column_definitions = ', '.join([f"{column} VARCHAR" for column in dt_dict.keys()])

# Create the table
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
cursor.execute(create_table_query)

# Insert data into the table
for i in range(len(dt_dict["arm_id"])):
    insert_data_query = f"INSERT INTO {table_name} ({', '.join(dt_dict.keys())}) VALUES ({', '.join(['%s']*len(dt_dict))})"
    insert_data_values = [dt_dict[column][i] for column in dt_dict.keys()]
    cursor.execute(insert_data_query, insert_data_values)

# Commit changes and close the connection
connection.commit()
cursor.close()
connection.close()

print(f"Table '{table_name}' created and data inserted successfully.")