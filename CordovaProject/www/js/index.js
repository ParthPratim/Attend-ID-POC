/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
var ss;
var localStorage = window.localStorage;

var _init = function() {
  ss = new cordova.plugins.SecureStorage(
    function() {
      console.log("OK");
    },
    function() {
      navigator.notification.alert(
        "Please enable the screen lock on your device. This app cannot operate securely without it.",
        function() {
          ss.secureDevice(
            function() {
              _init();
            },
            function() {
              _init();
            }
          );
        },
        "Screen lock is disabled"
      );
    },
    "AttendID"
  );
};

var app = {
    // Application Constructor
    initialize: function() {

      document.getElementById('login').addEventListener('click',cameraTakePicture)
      document.getElementById('set_server_host').addEventListener('click',SetServerHost)
      document.addEventListener('deviceready', this.onDeviceReady, false);
    },

    // deviceready Event Handler
    //
    // Bind any cordova events here. Common events are:
    // 'pause', 'resume', etc.
    onDeviceReady: function() {
        //this.receivedEvent('deviceready');
        _init()
        LoadDashboard()
    },

    // Update DOM on a Received Event
    receivedEvent: function(id) {

    }
};

function b64toBlob(b64Data, contentType, sliceSize) {
        contentType = contentType || '';
        sliceSize = sliceSize || 512;

        var byteCharacters = atob(b64Data);
        var byteArrays = [];

        for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            var slice = byteCharacters.slice(offset, offset + sliceSize);

            var byteNumbers = new Array(slice.length);
            for (var i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            var byteArray = new Uint8Array(byteNumbers);

            byteArrays.push(byteArray);
        }

      var blob = new Blob(byteArrays, {type: contentType});
      return blob;
}

function LoadDashboard(){
  if(ss == undefined) {//we want it to match
    setTimeout(function(){LoadDashboard()}, 50);//wait 50 millisecnds then recheck
    return;
  }
  ss.get(
  function(value) {
    window.location = "admin_dashboard.html"
  },
  function(error) {

  },
  "AccessToken"
);

}

function ProcessResponse(response){

  if(response.localeCompare("ERR_NO_ATTENDANCE_PRIVILIDGE") == 0 ){
    alert("You don't have attendance taking privilidges !!")
    return
  }
  if(response.localeCompare("ERR_USER_NOT_RECOGNIZED") == 0){
    alert("Who are you ? I don't know you. Are you even registered on AttendID.")
    return
  }
  response = JSON.parse(response)
    if(ss == undefined) {//we want it to match
      setTimeout(function(){ProcessResponse(response)}, 50);//wait 50 millisecnds then recheck
      return;
    }
  ss.set(
  function(key) {

    ss.set(
    function(key) {

      ss.set(
      function(key) {

        ss.set(
        function(key) {
          window.location = "admin_dashboard.html"
        },
        function(error) {
          console.log("Error " + error);
        },
        "DigitalID",
        response.DigitalID
      );

      },
      function(error) {
        console.log("Error " + error);
      },
      "OrganizationID",
      response.Organizations[0][1]
    );


    },
    function(error) {
      console.log("Error " + error);
    },
    "OrganizationName",
    response.Organizations[0][0]
  );


  },
  function(error) {
    console.log("Error " + error);
  },
  "AccessToken",
  response.AccessToken
);

}

function cameraTakePicture() {

   navigator.camera.getPicture(onSuccess, onFail, {
      quality: 50,
      destinationType: Camera.DestinationType.DATA_URL
   });

   function onSuccess(imageData) {
      //var image = document.getElementById('login_img');
      //image.src = "data:image/jpeg;base64," + imageData;

      var blob = b64toBlob(imageData,'image/jpeg')
      var formData = new FormData();
      formData.append("images",blob,'user_login.jpeg')

      alert(localStorage.getItem("ServerHost"))
      $.ajax({
       url : 'http://'+localStorage.getItem("ServerHost")+':2018/app/login',
       type : 'POST',
       data : formData,
       processData: false,  // tell jQuery not to process the data
       contentType: false,  // tell jQuery not to set contentType
       timeout: 10000000,
       success : function(data) {

         ProcessResponse(data);
         },
      error: function(xhr, status, error) {
        var err = eval("(" + xhr.responseText + ")");
        alert(err.Message);
      }
     });
   }

   function onFail(message) {
      alert('Failed because: ' + message);
   }
}

function SetServerHost(){
  navigator.notification.prompt(
    "Enter the IP Adddress of host (please don't) add http or https",  // message
    setHost,                  // callback to invoke
    'Change Server Host Address',            // title
    ['Ok','Cancel'],             // buttonLabels
 );
}

function setHost(result){
  text = result.input1.trim()
  if(text.length == 0 ){
    alert("Enter a valid Host Address")
  }
  else{
    setIP(text)
  }
}

function setIP(ip){
  if(ss == undefined){
    setTimeout(function(){setIP(ip)}, 50);//wait 50 millisecnds then recheck
    return;
  }
  localStorage.setItem("ServerHost", ip);
}

app.initialize();
