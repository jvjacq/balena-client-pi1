##This repository contains a the tools to build a balena container designed to run on a Raspberry Pi Zero W.

This project is designed to buld a Sensor-client device, running the Pi1.py file on a raspberry Pi connected to an MCP3008 ADC, which is in turn converting readings from a tempreature and light sensor. This device acts as a client in a Server-client architecure, connecting to a second 'Server' device, running a Python Flask server, also inside a Balena container. The sensor samples collected by this device are sent using Python TCP sockets.

The project contains a dockerfile template, which creates a Dockerfile used to install the libraries necessary for sampling from the MCP3008 ADC, and to run the python script Pi1.py.

This project should not print any messages, other than a final "Client exiting..." message when it shuts down.

The server-client interaction can be monitored from the Balena webportal.

## Authors: James Burness (BNRJAM019), Jacq van Jaarsveld (VJRJAC003)
