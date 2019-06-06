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

 var AccessToken = ""
 var OrganizationName = ""
 var OrganizationID = ""
 var SessionID = ""
 var AppUsername = ""
 var DigitalID = ""
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
      document.getElementById('new_session').addEventListener('click',InititateSession)
        document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
    },

    // deviceready Event Handler
    //
    // Bind any cordova events here. Common events are:
    // 'pause', 'resume', etc.
    onDeviceReady: function() {
        _init()
        loadSessionVariables();
    },

    // Update DOM on a Received Event
    receivedEvent: function(id) {

    }
};

function loadSessionVariables(){
  ss.get(
  function(key) {
    AccessToken = key
    ss.get(
    function(key) {
      OrganizationName = key
      ss.get(
      function(key) {
        OrganizationID = key

        ss.get(
        function(key) {
          DigitalID = key
          alert(DigitalID)
          alert(window.DigitalID)
          ss.get(
          function(key) {
            AppUsername = key
            document.getElementById('user-name-show').innerHTML = AppUsername
            RefreshSessionList()
          },
          function(error) {
            console.log("Error " + error);
          },
          "AppUsername"
        );

        },
        function(error) {
          console.log("Error " + error);
        },
        "DigitalID"
      );


      },
      function(error) {
        console.log("Error " + error);
      },
      "OrganizationID"
    );


    },
    function(error) {
      console.log("Error " + error);
    },
    "OrganizationName"
  );


  },
  function(error) {
    console.log("Error " + error);
  },
  "AccessToken"
);

}


function RefreshSessionList(){

  var formData = new FormData();
  formData.append("initiator",DigitalID)

  $.ajax({
   url : 'http://'+localStorage.getItem("ServerHost")+':2017/app/attendance/sessions/list',
   type : 'POST',
   data : formData,
   processData: false,  // tell jQuery not to process the data
   contentType: false,  // tell jQuery not to set contentType
   timeout: 10000000,
   success : function(data) {
     data = JSON.parse(data)
     list_data = data.Sessions
     table_data = ""
     for(i = 0 ; i < list_data.length  ;i++){
       table_data += "<tr><td>"+list_data[i].Name+"</td><td>"+list_data[i].Date+"</td><td>"+list_data[i].Time+"</td><td>"+list_data[i].Present+"</td></tr>"
     }
     document.getElementById('session_list_data').innerHTML = table_data
   }
 });
}

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


function InititateSession(){
  navigator.notification.prompt(
    'Enter the name of Attendance Session',  // message
    handlePrompt,                  // callback to invoke
    'New Attendance Session',            // title
    ['Ok','Cancel'],             // buttonLabels
 );

 function handlePrompt(result){
   text = result.input1.trim()
   if(text.length == 0 ){
     navigator.notification.alert("Enter a valid session name")
   }
   else{
     if(ss == undefined){
       setTimeout(function(){handlePrompt(result)}, 50);//wait 50 millisecnds then recheck
       return;
     }

             var formData = new FormData();
             formData.append("org_id",OrganizationID)
             formData.append("sess_name",text)
             formData.append("sess_ini_did",DigitalID)
             setTimeout(function () {
               window.plugins.spinnerDialog.show("Attendance Session", "Creating New Session",true);
             }, 500);
             $.ajax({
              url : 'http://'+localStorage.getItem("ServerHost")+':2017/app/attendance/new_session',
              type : 'POST',
              data : formData,
              processData: false,  // tell jQuery not to process the data
              contentType: false,  // tell jQuery not to set contentType
              timeout: 10000000,
              success : function(data) {
                  window.plugins.spinnerDialog.hide()
                  if("error" in data){
                    alert("Error" + data.error)
                  }
                  else{
                    alert("Session Created with ID : " + data.SessionID)
                    SessionID = data.SessionID
                    document.getElementById('sessionid').innerHTML = SessionID
                    document.getElementById('sessionname').innerHTML = result.input1.trim()
                    document.getElementById('new_session_btn').style.display = "inline"
                    document.getElementById('new_session').style.display = "none"
                    document.getElementById('new_session_btn').addEventListener("click",cameraTakePicture)
                    document.getElementById('hero-disp').style.display = "block"
                    document.getElementById('button-holder').style.display = "block"
                    document.getElementById('stop_this_session').addEventListener("click",function(){
                      document.getElementById('new_session_btn').style.display = "none"
                      document.getElementById('new_session').style.display = "block"
                      document.getElementById('hero-disp').style.display = "none"
                      document.getElementById('button-holder').style.display = "none"
                    })
                  }
                }
            });


   }

 }

}

function cameraTakePicture() {

   navigator.camera.getPicture(onSuccess, onFail, {
      quality: 50,
      destinationType: Camera.DestinationType.DATA_URL
   });

   function onSuccess(imageData) {
      //var image = document.getElementById('login_img');

      var blob = b64toBlob(imageData,'image/jpeg')
      var formData = new FormData();
      formData.append("images",blob,'user_login.jpeg')
      formData.append("org_id",OrganizationID)
      formData.append("sess_id",SessionID)
      setTimeout(function () {
        window.plugins.spinnerDialog.show("Attendance Session ", "Marking Attendance",true);
      }, 500);
      $.ajax({
       url : 'http://'+localStorage.getItem("ServerHost")+':2017/app/attendance/verify_user',
       type : 'POST',
       data : formData,
       processData: false,  // tell jQuery not to process the data
       contentType: false,  // tell jQuery not to set contentType
       timeout: 10000000,
       success : function(data) {
         setTimeout(function () {
           window.plugins.spinnerDialog.hide()
         }, 500);
         data = JSON.parse(data)
         if(data.code.localeCompare('ATTENDANCE_MARKED') == 0 ){
           alert("Marked Attendance for : " + data.name)
         }
         else{
           alert("Error : " + data.error)
         }

         RefreshSessionList()
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


app.initialize();
