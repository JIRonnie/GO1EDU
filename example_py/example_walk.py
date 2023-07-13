#!/usr/bin/python

import sys
import time
import math
import json
import socket

sys.path.append('../lib/python/amd64')
import robot_interface as sdk


def parse_udp_message(udp_message):
    try:
        json_data = json.loads(udp_message)
        prox_data = json.loads(json_data["Prox"])
        gps_data = json.loads(json_data["GPS"])
        imu_data = json.loads(json_data["IMU"])
        
        # Extracting values from each section
        prox_l = prox_data["L"]
        prox_c = prox_data["C"]
        prox_r = prox_data["R"]
        
        gps_lat = gps_data["Lat"]
        gps_lon = gps_data["Lon"]
        gps_alt = gps_data["Alt"]
        gps_vel = gps_data["Vel"]
        gps_heading = gps_data["GpsHeading"]
        
        imu_roll = imu_data["Roll"]
        imu_pitch = imu_data["Pitch"]
        imu_yaw = imu_data["Yaw"]
        imu_heading = imu_data["Heading"]
        
        # Returning the extracted values as a dictionary
        return {
            "Prox": {"L": prox_l, "C": prox_c, "R": prox_r},
            "GPS": {"Lat": gps_lat, "Lon": gps_lon, "Alt": gps_alt, "Vel": gps_vel, "GpsHeading": gps_heading},
            "IMU": {"Roll": imu_roll, "Pitch": imu_pitch, "Yaw": imu_yaw, "Heading": imu_heading}
        }
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing UDP message: {e}")
        return None

if __name__ == '__main__':

    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff

    udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)

    cmd = sdk.HighCmd()
    state = sdk.HighState()
    udp.InitCmdData(cmd)

    ip_address = '192.168.200.234'
    port = 1901

    udp_socket = socket.socket(socket.AF_INIT, socket.SOCK_DGRAM)

    udp_socket.bind(ip_address, port)

    print(f"Listening for UDP messages on {ip_address}:{port}...")

    motiontime = 0
    while True:
        time.sleep(0.002)
        motiontime = motiontime + 1

        udp.Recv()
        udp.GetRecv(state)

        # Receive UDP message and client address
        message, client_address = udp_socket.recvfrom(1024)  # 1024 is the buffer size

        # Decode the message
        decoded_message = message.decode('utf-8')

        # Print the received message and client address
        print(f"Received message: {decoded_message} from {client_address}")
        
        # print(motiontime)
        # print(state.imu.rpy[0])
        # print(motiontime, state.motorState[0].q, state.motorState[1].q, state.motorState[2].q)
        # print(state.imu.rpy[0])

        cmd.mode = 0      # 0:idle, default stand      1:forced stand     2:walk continuously
        cmd.gaitType = 0
        cmd.speedLevel = 0
        cmd.footRaiseHeight = 0
        cmd.bodyHeight = 0
        cmd.euler = [0, 0, 0]
        cmd.velocity = [0, 0]
        cmd.yawSpeed = 0.0
        cmd.reserve = 0

        # cmd.mode = 2
        # cmd.gaitType = 1
        # # cmd.position = [1, 0]
        # # cmd.position[0] = 2
        # cmd.velocity = [-0.2, 0] # -1  ~ +1
        # cmd.yawSpeed = 0
        # cmd.bodyHeight = 0.1

        if(motiontime > 0 and motiontime < 1000):
            cmd.mode = 1
            cmd.euler = [-0.3, 0, 0]
        
        if(motiontime > 1000 and motiontime < 2000):
            cmd.mode = 1
            cmd.euler = [0.3, 0, 0]
        
        if(motiontime > 2000 and motiontime < 3000):
            cmd.mode = 1
            cmd.euler = [0, -0.2, 0]
        
        if(motiontime > 3000 and motiontime < 4000):
            cmd.mode = 1
            cmd.euler = [0, 0.2, 0]
        
        if(motiontime > 4000 and motiontime < 5000):
            cmd.mode = 1
            cmd.euler = [0, 0, -0.2]
        
        if(motiontime > 5000 and motiontime < 6000):
            cmd.mode = 1
            cmd.euler = [0.2, 0, 0]
        
        if(motiontime > 6000 and motiontime < 7000):
            cmd.mode = 1
            cmd.bodyHeight = -0.2
        
        if(motiontime > 7000 and motiontime < 8000):
            cmd.mode = 1
            cmd.bodyHeight = 0.1
        
        if(motiontime > 8000 and motiontime < 9000):
            cmd.mode = 1
            cmd.bodyHeight = 0.0
        
        if(motiontime > 9000 and motiontime < 11000):
            cmd.mode = 5
        
        if(motiontime > 11000 and motiontime < 13000):
            cmd.mode = 6
        
        if(motiontime > 13000 and motiontime < 14000):
            cmd.mode = 0
        
        if(motiontime > 14000 and motiontime < 18000):
            cmd.mode = 2
            cmd.gaitType = 2
            cmd.velocity = [0.4, 0] # -1  ~ +1
            cmd.yawSpeed = 2
            cmd.footRaiseHeight = 0.1
            # printf("walk\n")
        
        if(motiontime > 18000 and motiontime < 20000):
            cmd.mode = 0
            cmd.velocity = [0, 0]
        
        if(motiontime > 20000 and motiontime < 24000):
            cmd.mode = 2
            cmd.gaitType = 1
            cmd.velocity = [0.2, 0] # -1  ~ +1
            cmd.bodyHeight = 0.1
            # printf("walk\n")
            

        udp.SetSend(cmd)
        udp.Send()

udp_socket.close()