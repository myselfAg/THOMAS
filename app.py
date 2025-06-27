import streamlit as st
import serial
import time

# Setup Serial Communication
@st.cache_resource
def get_serial_connection():
    try:
        arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)
        time.sleep(5)
        return arduino
    except serial.SerialException:
        return None

arduino = get_serial_connection()

st.title("🔧 Real-Time Ultrasonic Sensor Readings")

placeholder = st.empty()

if arduino:
    try:
        while True:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').strip()
                if line:
                    placeholder.markdown(f"Distance: `{line}`")
                time.sleep(0.1)
    except KeyboardInterrupt:
        st.warning("🔌 Connection interrupted.")
    finally:
        arduino.close()
else:
    st.error("⚠️ Could not connect to Arduino on COM5. Check the port or connection.")





















# import streamlit as st
# import serial
# import time
# from streamlit_autorefresh import st_autorefresh

# st_autorefresh(interval=250, limit=None, key="refresh")

# @st.cache(allow_output_mutation=True)
# def get_serial():
#     try:
#         ser = serial.Serial('COM5', 9600, timeout=0.1)
#         time.sleep(2)
#         ser.reset_input_buffer()
#         return ser
#     except serial.SerialException:
#         return None

# ser = get_serial()

# if 'density' not in st.session_state:
#     st.session_state['density'] = None
# if 'seats' not in st.session_state:
#     st.session_state['seats'] = None
# if 'error' not in st.session_state:
#     st.session_state['error'] = None

# st.title("🚆 Train Carriage Density & Seat Availability Monitor")

# if ser:
#     try:
#         lines = []
#         for _ in range(5):
#             if ser.in_waiting > 0:
#                 line = ser.readline().decode('utf-8', errors='ignore').strip()
#                 if line:
#                     lines.append(line)
#             else:
#                 break

#         if lines:
#             last_line = lines[-1]
#             if last_line.startswith("Density:") and "|Seats:" in last_line:
#                 try:
#                     density_part, seats_part = last_line.split('|')
#                     density_val = int(density_part.split(':')[1].replace('%', '').strip())
#                     seats_val = int(seats_part.split(':')[1].strip())

#                     if (st.session_state['density'] != density_val or
#                         st.session_state['seats'] != seats_val):
#                         st.session_state['density'] = density_val
#                         st.session_state['seats'] = seats_val
#                         st.session_state['error'] = None

#                 except Exception:
#                     st.session_state['error'] = "Parsing error in Arduino data."

#         if st.session_state['density'] is not None and st.session_state['seats'] is not None:
#             st.markdown(f"### Current Density: **{st.session_state['density']}%**")
#             st.markdown(f"### Seats Available: **{st.session_state['seats']}**")
#         else:
#             st.info("⏳ Waiting for data...")

#         if st.session_state['error']:
#             st.error(st.session_state['error'])

#     except Exception as e:
#         st.error(f"Serial read error: {e}")
# else:
#     st.error("⚠️ Could not open serial port COM5")

