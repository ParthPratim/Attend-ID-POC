# Attend-ID-POC
Attend-ID POC repo - A decentralised bio-metric digital identity management and verification system

**WARNING : This is a private project and under the copyright laws, without the legit permission of the author of the project using any code associated with this repository will be considered an act of offence and will be definitely followed by a law suit**

**Project Status : POC (semi-productional)**

# Features Implemented : 
* User Creation
* Organization Creation
* Adding Users 
* Transferring user assets to other organizations (Trans-ID)
* Attendance Session - creation, marking, indexing
* Dynamic Face Recogniton Model Training

# Upcoming Features (not merged into git) : 
* Leave application (Leave-In)
* POSE 

# Special Mentions
* Intellignence and deployment : Microsoft Azure Cloud Cognitive Services
* Face Intelligencce : Google Facenet - open source implementation by @davidsandberg 
* Blockchain :  Hyperledger Sawtooth
* Mass-Storage : IPFS
* Blochain Storage : BigchainDB
* Android Dev : The Cordova Project
* Vision :  OpenCV 

# Prerequisites :
Make sure you are in the root directory of the project.

* A laptop/PC with a fast enough processor (Intel i5 or higher) and if possible a GPU. This Project requires such a high performance machine because it involves training Machine learning models on the go and also involves a high amount of inference with the trained model. Having a slow PC can result in frequent crashes and lags.
* Docker and Docker-Compose installed 
* A Linux Distribution (tested on Ubuntu 18.04, should work on all versions of Ubuntu)

# Step 1 :

Clone the official repo and cd into it:
```
git clone https://github.com/ParthPratim/Attend-ID-POC.git

cd Attend-ID-POC
```

Let's compose the AttendID network

Open up the compose-network.yaml file present in the root directory of the project.

**Replace the path present in the last line of script with the complete path to your directory where the Attend-ID-POC repo was cloned**

Now open up a terminal and execute the following:

```
docker build -t base_attendid

docker-compose -p attendid -f compose-network.yaml up
```

# Step 2 :
Fire up a terminal and type
```
docker exec -it base_attendid /bin/bash
```
This will open up a shell into the attendid base docker container. Now execute the following command (This step is needed to be done just once.) :
```
cd /src/scripts
python3 begin.py

cd /src/web
npm install
```
Now in the same terminal window execute the following:
**Note: The following two commands are needed to be executed everytime you want to run the AttendID system. Just open a shell into the *base_attendid* docker container and execute the following.**

```
cd /src
supervisord -c supervisord.conf
```

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
We will not be clicking pictures. We need atleast 10 clear images with *good lighting conditions* for the Face Recognition Model to work. For this we have provided you with a tools named img_snap but for it to work we need to give it a video to generate images from.

**Imp NOTE : When you run the record.py app remember to just move your face to the left, right, up and down at a medium speed and once you have done that press *q***

```
# MAKE SURE YOU HAVE python 3.6 or above installed
python3 -m pip install ecapture
cd tools
python3 record.py 

# Video has been recorded. Now generate the pictures
# Now you need to Wait while the tool processes the video you just recorded
docker exec -it base_attendid /bin/bash
cd src/tools
python3 img_snap.py
# Your images are generated under the directory /src/tools/{The-Name-Which-You-Entered-In-Img-Snap-Tool}

# Now follow the tool's instructions and you will have your images in a folder of a name of your choice

```

Now back in the web portal when you click on *Create User*, you need to enter the name of user to be created and upload the images generated by img_snap, wait for a few seconds and the new user is created. When the new suer is created, an SSL client certificate will be automatically downloaded on your browser.

Open *Settings >> Advanced >> Manage Certificates*

Import this downloaded certificate. This certificate is signed by our CA and this will validate all your requests sent to our servers.

Before creating another user give the system some time, usuallly just a few seconds, to retrain the face recognition model on your face so that it can recognize you next time.

# Step 5 - (Create Organization)
Since now you have imported the certificate and have authenticated yourself, you can now create a new organization. The UI is pretty straight forward. You only need to submit the name of the new org and it's done but a valid SSL Certificate (just like the one which you imported recently) is required for creating an organization.

When the organization is created an SSL Certificate is downloaded to the Browser which is only for Organization adminstration purposes and not for regular use. You need to again go to the *Manage Certificates*  section of your browser and replace the previously imported certificate with the new one and now you will be sending request as the organization which you just created.

# Step 6- (View Dashboard)

**This feature requires that you import the SSL certificate of an Organization. This feature will not work with a normal user SSL certificate. Please remember to check the imported certificate before oprning the dashboard.**

The dashboard provides the following features (as of now) :
* Add User
* Transfer Asset(Member)

The Add User interface is similar to the create user as in you need to give images of the user who you wan't to add and he would be recognized by our Global Facial Recognition Engine and be added to your member list but you also need to specify is the user that is being added has the privilidge of marking attendance using our *Attendance marking service* .

The Transfer asset is a utility which requires you to know the Organization ID of the organization you wan't to transfer it to using the **TRANSFER** button below every user in your member list.

NOTE : The OrgID can be found on the top left corner of the dashboard.

# Step 7 - (Attendance Marking - Mobile App)

**Android APK :** *CordovaProject/platforms/android/app/app-debug.apk*

Install the APK on your phone by connecting your phone to your laptop/PC and execute the following :
**(adb should be installed)**
```
adb install CordovaProject/platforms/android/app/app-debug.apk
```
Make sure that your phone and the laptop running the docker setup share same the same WLAN network.

On running the mobile app you will be given an option on the home screen to **Set Server Host** .

Select that option and enter the IP address of the laptop/host. You can find your IP address by running *ipconfig* (Windows) or *ifconfig* (Linux).

You need to then click on **Login** to click a picture of yourself and our servers would authenticate you using Face Recognition. If you have attendance marking previlidges then you can take the attendance of our membres in the member list by creating named attendance sessions on the App where students/employees click their selfie one by one and get authenticated/rejected acccordingly.
