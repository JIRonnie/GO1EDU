/*****************************************************************
 Copyright (c) 2020, Unitree Robotics.Co.Ltd. All rights reserved.
******************************************************************/

#include "unitree_legged_sdk/unitree_legged_sdk.h"
#include <math.h>
#include <iostream>
#include <unistd.h>
#include <string.h>

using namespace UNITREE_LEGGED_SDK;

class Custom
{
public:
    Custom(uint8_t level, string rotateDirection, int rotateSeconds): 
      safe(LeggedType::Go1),
      rotateDirection(rotateDirection),
      rotateSeconds(rotateSeconds),
      udp(level, 8090, "192.168.123.161", 8082) {
        udp.InitCmdData(cmd);
    }
    void UDPRecv();
    void UDPSend();
    void RobotControl();

    Safety safe;
    UDP udp;
    HighCmd cmd = {0};
    HighState state = {0};
    int motiontime = 0;
    float dt = 0.002;     // 0.001~0.01

    int rotateSeconds = 1;
    string rotateDirection = "right";
};


void Custom::UDPRecv()
{
    udp.Recv();
}

void Custom::UDPSend()
{  
    udp.Send();
}

void Custom::RobotControl() 
{
    motiontime += 2;
    udp.GetRecv(state);

    cmd.mode = 0;      // 0:idle, default stand      1:forced stand     2:walk continuously
    cmd.gaitType = 0;
    cmd.speedLevel = 0;
    cmd.footRaiseHeight = 0;
    cmd.bodyHeight = 0;
    cmd.euler[0]  = 0;
    cmd.euler[1] = 0;
    cmd.euler[2] = 0;
    cmd.velocity[0] = 0.0f;
    cmd.velocity[1] = 0.0f;
    cmd.yawSpeed = 0.0f;
    cmd.reserve = 0;

    if (motiontime > 0 && motiontime < rotateSeconds * 1000) {
        cmd.mode = 2;
        cmd.gaitType = 2;

        if (rotateDirection == "left") {
            cmd.yawSpeed = 2;
        } else if (rotateDirection == "right") {
            cmd.yawSpeed = -2;
        }

        cmd.footRaiseHeight = 0.1;
    }

    if (motiontime > (rotateSeconds+1) * 1000) {
        cmd.mode = 1;
    }

    udp.SetSend(cmd);
}

int main(int argc, char *argv[]) 
{
    
    std::cout << "Communication level is set to HIGH-level." << std::endl
              << "WARNING: Make sure the robot is standing on the ground." << std::endl
              << "Press Enter to continue..." << std::endl;
    std::cin.ignore();

    // Usage: ./example_rotate_in_place left 5
    Custom custom(HIGHLEVEL, argv[1], atoi(argv[2]));

    // InitEnvironment();
    LoopFunc loop_control("control_loop", custom.dt,    boost::bind(&Custom::RobotControl, &custom));
    LoopFunc loop_udpSend("udp_send",     custom.dt, 3, boost::bind(&Custom::UDPSend,      &custom));
    LoopFunc loop_udpRecv("udp_recv",     custom.dt, 3, boost::bind(&Custom::UDPRecv,      &custom));

    loop_udpSend.start();
    loop_udpRecv.start();
    loop_control.start();

    while(1){
        sleep(10);
    };

    return 0; 
}
