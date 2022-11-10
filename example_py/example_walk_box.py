#!/usr/bin/python

import sys
import time
import math

sys.path.append('../lib/python/amd64')
import robot_interface as sdk


if __name__ == '__main__':

    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff

    udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)

    cmd = sdk.HighCmd()
    state = sdk.HighState()
    udp.InitCmdData(cmd)

    motiontime = 0
    while True:
        time.sleep(0.002)
        motiontime = motiontime + 1

        udp.Recv()
        udp.GetRecv(state)
        
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
        
        # First leg of box
        if ( motiontime > 0 and motiontime < 2000 ):
            cmd.mode = 2
            cmd.gaitType = 1
            cmd.velocity = [0.2, 0]
            cmd.footRaiseHeight = 0.1

        if ( motiontime > 3000 and motiontime < 4000 ):
            cmd.mode = 10

        # Second leg of box
        if ( motiontime > 9000 and motiontime < 10000 ):
            cmd.mode = 2
            cmd.gaitType = 1
            cmd.velocity = [0.2, 0]
            cmd.footRaiseHeight = 0.1

        if ( motiontime > 11000 and motiontime < 12000 ):
            cmd.mode = 10

        # Third leg of box
        if ( motiontime > 17000 and motiontime < 19000 ):
            cmd.mode = 2
            cmd.gaitType = 1
            cmd.velocity = [0.2, 0]
            cmd.footRaiseHeight = 0.1

        if ( motiontime > 20000 and motiontime < 21000 ):
            cmd.mode = 10

        # Forth leg of box
        if ( motiontime > 26000 and motiontime < 28000 ):
            cmd.mode = 2
            cmd.gaitType = 1
            cmd.velocity = [0.2, 0]
            cmd.footRaiseHeight = 0.1

        if ( motiontime > 29000 and motiontime < 30000 ):
            cmd.mode = 10

        # Return to default standing position
        if ( motiontime > 35000 ):
            cmd.mode = 1

        udp.SetSend(cmd)
        udp.Send()
