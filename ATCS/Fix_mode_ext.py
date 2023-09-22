#import machine
import time

#uart = machine.UART(0, baudrate=19200, bits=8, parity=None, stop=1, tx=machine.Pin(0), rx=machine.Pin(1))

# Predefine data in the array_list
request_id = 1
intensity = 0
total_stage = 0
GA_Arm = 0
GA_Light = 0
PS_Arm = 0
PS_Light = 0
element_40 = 35
element_41 = 0
element_42 = 0
element_43 = 0
element_44 = 35


# Function to calculate CRC of values of 1 to 28 index in the array_list according to CRC-8 algorithm
def crc8(data):
    crc = 0x00
    polynomial = 0xD8

    for byte in data[0:29]:  # It excludes the value which are on 0 and 29 index
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1

    return crc & 0xFF


with open('database.csv', 'r') as file:
    lines = file.readlines()

# Remove leading and trailing whitespace from each line
lines = [line.strip() for line in lines]

# Split the header line and data lines
header = lines[0].split(',')
data_lines = lines[1:]

# Find the indices of the relevant columns
column_indices = {
    'slotno': header.index('slotno'),
    'stageid': header.index('stageid'),
    'armid': header.index('armid'),
    'totaltime': header.index('totaltime'),
    'throughsign': header.index('throughsign'),
    'leftsign': header.index('leftsign'),
    'rightsign': header.index('rightsign'),
    'stop': header.index('stop'),
    'caution': header.index('caution'),
    'walkman': header.index('walkman'),
    'stopman': header.index('stopman'),
    'modeid': header.index('modeid'),
}

# Initialize a dictionary to store the grouped data
grouped_data = {}

# Iterate through the data lines and group data by slotno and stageid
for data_line in data_lines:
    data = data_line.split(',')
    slotno = data[column_indices['slotno']]
    stageid = data[column_indices['stageid']]

    # Create a unique key based on slotno and stageid
    key = (slotno, stageid)

    if key not in grouped_data:
        grouped_data[key] = []

    grouped_data[key].append(data)

# print("grouped_data>>>>>>",grouped_data)

# Initialize a list to store the final processed data
data_array = []

# Set the delay and active time
delay_between_sends = 0.5  # in seconds

def not_logic(value):
    if value == 0:
        return 1
    elif value == 1:
        return 0
    elif value == 2:
        return 2

# Process each group of similar slotno and stageid values
for group_key, group_data in grouped_data.items():
    #print("group_key>>>>>>>",group_key)
    #print("group_data>>>>>>",group_data)
    data_array.append(0xff)

    for row in group_data:
        throughsign = not_logic(int(row[column_indices['throughsign']]))
        leftsign = not_logic(int(row[column_indices['leftsign']]))
        rightsign = not_logic(int(row[column_indices['rightsign']]))
        stop = not_logic(int(row[column_indices['stop']]))
        # print("stop::::",stop)
        caution = not_logic(int(row[column_indices['caution']]))
        walkman = not_logic(int(row[column_indices['walkman']]))
        stopman = not_logic(int(row[column_indices['stopman']]))
        data_array.append(throughsign)
        data_array.append(leftsign)
        data_array.append(rightsign)
        data_array.append(stop)
        data_array.append(caution)
        data_array.append(walkman)
        data_array.append(stopman)

    data_array.append(int(row[column_indices['modeid']]))
    # Calculate the CRC value for the group's data (excluding 0xff and modeid)
    crc_value = crc8(data_array[0:29])
    data_array.append(crc_value)

    data_array.append(request_id)
    data_array.append(intensity)
    data_array.append(int(group_data[0][column_indices['stageid']]))
    data_array.append(total_stage)
    data_array.append(int(group_data[0][column_indices['totaltime']]))
    data_array.append(GA_Arm)
    data_array.append(GA_Light)
    data_array.append(PS_Arm)
    data_array.append(PS_Light)
    data_array.append(element_40)
    data_array.append(element_41)
    data_array.append(element_42)
    data_array.append(element_43)
    data_array.append(element_44)
    # Send the data_array over UART every 500 msec and keep it active for a defined time
    active_time = data_array[35]  # Assuming the active time is stored at index 35
    start_time = time.time()

    while time.time() - start_time <= active_time:
        print(data_array)
        print(bytes(data_array))  # Send the data over UART
        #uart.write(data_array)
        #uart.write("\n)")
        #uart.write(bytes(data_array))
        time.sleep(0.5)  # Wait for 500 msec

    # Clear the array for the next group
    data_array = []
