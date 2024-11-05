# Balena Client Pi1

This repository contains all the tools to build a Balena container project designed to run on a Raspberry Pi Zero W.

This project is designed to build a Sensor-client device, running the Pi1.py file on a Raspberry Pi connected to an MCP3008 ADC, which is in turn converting readings from a temperature and light sensor. This device acts as a Client in a Server-client architecture, connecting to a second 'Server' device, running a Python Flask server, also inside a Balena container. The sensor samples collected by this device are sent using Python TCP sockets.

The project contains a Dockerfile template, which creates a Dockerfile used to install the libraries necessary for sampling from the MCP3008 ADC, and to run the python script Pi1.py.

This project should not print any messages, other than a final "Client exiting..." message when it shuts down.

The server-client interaction can be monitored from the Balena webportal.

**Authors**: James Burness, Jacq van Jaarsveld

**Project**: EEE3095S Practical 6
