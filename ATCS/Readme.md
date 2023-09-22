Script: CAM_data_ext
Title: Arduino Data to PostgreSQL Database Integration

Description:
This Python script establishes a connection between an Arduino Nano and a PostgreSQL database, allowing you to capture data from the Arduino and store it in a structured manner in the database. The code utilizes the `psycopg2` library to interact with PostgreSQL and the `serial` library to communicate with the Arduino via a serial port.

Here's how the script works:

1. It establishes a serial connection to the Arduino Nano, specifying the serial port and baud rate.

2. After a brief initialization delay, it reads data from the Arduino over the serial connection. The data is expected to be a comma-separated string containing information about different parameters.

3. The script then processes the received data to extract relevant information, such as the arm ID, the number of cameras, and camera positions.

4. Based on the number of cameras and their positions, it organizes the data into a dictionary.

5. It establishes a connection to a PostgreSQL database and creates a table if it doesn't already exist. The table schema is dynamically generated based on the dictionary keys.

6. Finally, it inserts the processed data into the PostgreSQL table, ensuring that the data is properly structured and stored.
