# v3.4
The unitree_legged_sdk is mainly used for communication between PC and Controller board.
It also can be used in other PCs with UDP.

### Notice
support robot: Go1

not support robot: Laikago, Aliengo, A1. (Check release [v3.2](https://github.com/unitreerobotics/unitree_legged_sdk/releases/tag/v3.2) for support)

### Dependencies
* [Boost](http://www.boost.org) (version 1.5.4 or higher)
* [CMake](http://www.cmake.org) (version 2.8.3 or higher)
* [LCM](https://lcm-proj.github.io) (version 1.4.0 or higher)
```bash
cd lcm-x.x.x
mkdir build
cd build
cmake ../
make
sudo make install
```

### Build
```bash
mkdir build
cd build
cmake ../
make
```

### Usage
1.  Cpp

    Run examples with 'sudo' for memory locking.

2. Python

    To run the robot with Python scripts, open scripts/Robot_Python.py, then edit the path to "build" folder.

    After that, running Robot_Python.py. Right now, the provided Python scripts are only for A1 robot. To use other type robots, edit the "LeggedType" in src/python_interface_high_cmd.cpp, and recompile the project.
