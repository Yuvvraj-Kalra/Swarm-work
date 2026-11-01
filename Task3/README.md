Task 3: ROS 2 Drone Sensor Monitoring

This project simulates a drone telemetry system using ROS 2 Jazzy and Python. It has three nodes. The sensor node publishes fake altitude, battery and temperature values once per second. The monitor node reads them, prints them, and publishes a status on /drone/status. The warning node reads the status and publishes warnings on /drone/warnings. The communication graph is in screenshots/ros2_graph.png.

The status is NORMAL unless the battery is below 20 percent (LOW BATTERY), the temperature is above 60 degrees (OVERHEATING), or the altitude is above 30 m (ALTITUDE LIMIT EXCEEDED). Several can be active at once. If a sensor has not sent data yet, the status is WAITING FOR SENSOR DATA. The starting sensor values are ROS parameters, so each test can be run from the command line.

To run it, copy the drone_monitoring folder into ros2_ws/src, then from ros2_ws run a colcon build and sourced setup.bash. In three different terminals, I ran sensor_publisher, telemetry_monitor and warning_publisher.

I tested all six cases: normal, low battery (-p battery_start:=15.0), overheating (-p temperature_base:=65.0), altitude (-p altitude_base:=45.0), multiple limits together, and no sensor running. The screenshots are in the screenshots folder.

The main problems I had were forgetting to source the workspace in each terminal, and building in my home folder instead of a proper workspace. I learned how nodes, topics and timers work together.
