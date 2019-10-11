# PVSimulator

This repository is for Mobility House's test. It represents a service that reads energy values from a mock meter and communicates them to a Photovoltaic Simulator that outputs the power. 

## Local deployment
To deploy locally, make sure you have: 
1. `docker version 19+ `
1. `docker-compose version 3`
## Components

- `messaging` 
This package contains the logic for the layer that is responsible for messaging, sending/receiving messages to/from a broker. 
 - `meter`
This package contains the logic of the mock Meter. The only mock meter we have is a meter that produces readings based on a Gaussian Distribution. 
 - `pv`
 This package contains the logic for the mock PV Simulator, for now we only have just one that gets an energy input and outputs it multiplied by an efficiency factor.
 - `start_meter` is the entry point for starting the Meter and sending readings to the messaging broker. Here you decide the rate at which the Meter gets polled, and instantiate the appropriate meter and broker that you want to use.
 - `start_receiver` is the entry point for starting the receiver that receives readings from the meter and outputs the generated power to a file.

## Local deployment

1. Run `docker-compose up rabbitmq` to create a docker container that hosts a RabbitMQ broker which handles communication between the Meter and the PVSimulator.  
	> **Note:** Make sure that the RabbitMQ server runs before starting the other containers, check the logs with `docker logs rabbitmq` and see if it started up successfully. 
2. Run `docker-compose up receiver` to create a docker container that hosts the receiver.
3. Run `docker-compose up sender` to create the docker container that hosts the sender.
> **Note** If you need to force rebuild the images run `docker-compose up --build [image]`

After running you should see a new folder called **output** which contains a directory structure based on when the application was running , accessing the folder that represents a specific day will contain a `.csv` file with the appropriate outputs for that day in the format `Time,Measured Power,Output Power,Total Power`. 
> Example `output/2019/10/11.csv`



## Cleanup

To clean up the project run, in the same folder as the docker-compose file of this project.  


`docker-compose down -v --rmi all --remove-orphans`


## Container Specs
Receiver and Sender containers pull from python:3.7. All containers install the python required modules from the requirements.txt file. 
RabbitMQ pulls from RabbitMQ:3