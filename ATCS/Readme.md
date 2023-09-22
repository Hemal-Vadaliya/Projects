Script: Fix_mode_ext

Description:
This Python script is designed to integrate an Arduino-based traffic light control system with a data source stored in a CSV file. The traffic light system's behavior is controlled based on the data in the CSV file. The script performs the following tasks:

1. **Data Parsing**: The script reads data from a CSV file called 'database.csv', which is assumed to contain information about the behavior of traffic lights at different stages.

2. **Data Grouping**: The data is grouped based on unique combinations of 'slotno' and 'stageid', allowing for the organization of traffic light behavior for different scenarios.

3. **Data Processing**: For each group of traffic light scenarios, the script processes the data to determine the status of various traffic light signals, such as 'throughsign,' 'leftsign,' 'rightsign,' 'stop,' 'caution,' and more.

4. **Data Packaging**: The processed traffic light signals are packaged into a data array that includes CRC (Cyclic Redundancy Check) values, request IDs, intensity levels, and other control parameters.

5. **Serial Communication**: The script simulates sending this data to the Arduino via UART (Universal Asynchronous Receiver-Transmitter) serial communication. In the commented code section, you can find the lines that would typically send the data to the Arduino.

6. **Timing Control**: The script takes into account the 'active_time' parameter from the data and maintains the traffic light behavior for the specified duration.

This script provides a bridge between a data source (CSV file) and an Arduino-based traffic light control system, making it possible to automate and simulate traffic light scenarios based on real-world data. The data in the CSV file can be customized to model various traffic conditions and scenarios, enhancing the versatility of the traffic light control system.

Script: CAM_data_ext

Description:
This Python script establishes a connection between an Arduino Nano and a PostgreSQL database, allowing you to capture data from the Arduino and store it in a structured manner in the database. The code utilizes the `psycopg2` library to interact with PostgreSQL and the `serial` library to communicate with the Arduino via a serial port.

Here's how the script works:

1. It establishes a serial connection to the Arduino Nano, specifying the serial port and baud rate.

2. After a brief initialization delay, it reads data from the Arduino over the serial connection. The data is expected to be a comma-separated string containing information about different parameters.

3. The script then processes the received data to extract relevant information, such as the arm ID, the number of cameras, and camera positions.

4. Based on the number of cameras and their positions, it organizes the data into a dictionary.

5. It establishes a connection to a PostgreSQL database and creates a table if it doesn't already exist. The table schema is dynamically generated based on the dictionary keys.

6. Finally, it inserts the processed data into the PostgreSQL table, ensuring that the data is properly structured and stored.
