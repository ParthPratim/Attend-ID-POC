# Attend-ID-POC
Attend-ID POC repo - A decentralised bio-metric digital identity management and verification system

Make sure you are in the root directory of the project.

# Step 1 :
Let's compose the AttendID network
```
docker-compose -p attendid -f compose-network.yaml up
```

# Step 2 :
Fire up a terminal and type 
```
docker exec -it base_attendid /bin/bash
```
This will open up a shell into the attendid base docker container. Now execute the following command : 
```
cd src/scripts
python3 init.py
```
This step is needed to be done just once.

# Step 3:
Wait for a couple of minutes or rather grab a coffee and then open up the browser. 
**Please follow the below steps carefully as missing any one of these might end you up into unpredictable working of the system**

In the browser type the following : *https://127.0.0.1:2018/*

**Please note that the *https* is very important**.
On opening this URL you would get an error from the browser. This is very much exepcted. You need to click on *Add Exception* (on Firefox) ot *proceed anyway* (on Chrome).

**Welcome to the AttendID Web Portal**

# Step 4 - (Creating an user):
On the web UI you can see three options, namely:
* Create User
* Create Organization
* View Dashboard

Let's focus on *Create User* : 
But before that open up the root directory of the project and open a terminal.
We will not be clicking pictures. We need atleast 10 clear images with good lighting conditions for the Face Recognition Model to work. For this we have provided you with a tools named img_snap but for it to work we need to give it a video to generate images from. 

```
// MAKE SURE YOU HAVE python 3.6 or above installed
python3 -m pip install ecapture
cd tools
python3 record.py

// Video has been recorded. Now generate the pictures
docker exec -it base_attendid /bin/bash
cd src/tools
python3 img_snap.py 

// Now follow the tool's instructions and you will have your images in a folder of a name of your choice

```

