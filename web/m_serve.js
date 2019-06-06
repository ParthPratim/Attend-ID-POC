const express = require('express')
const fs = require('fs')
const path = require('path')
const request = require('request')
const bodyParser = require('body-parser')
const multer = require('multer')
const FormData = require('form-data');
const mime=require('mime-types');
const public = path.join(__dirname, 'public')
const cbor = require('cbor');
const crypto = require('crypto');

const opts = {
  requestCert: false,
  rejectUnauthorized: false
}

const app = express()

const upload = multer({dest: 'public/uploads'}).array('images')
//app.use(express.json());

var headers = {
    'Content-Type' : 'application/json'
};


app.get('/', (req, res) => {
	res.send("M_SERVER")
})

app.post('/app/login' , upload, function (req, res, next) {
  console.log(req.files[0])
  var form = new FormData();
  if(req.files.length > 0){
    form.append("images", fs.createReadStream(req.files[0].path));
    var r = request.post('http://172.30.0.1:2020/api/v1/whoisit/global', headers= headers, requestCallback);
    r._form = form;

    function requestCallback(err, response, body) {
      console.log(body)
      res.send(body)
      res.end()
    }

  }
})

function forward_post(params,URL,handler){
  request.post({
    headers: {'content-type' : 'application/json'},
    url:     'http://172.30.0.1:2020'+URL,
    body:    params,
    json :  true,
  }, handler);

}

app.post('/app/attendance/new_session', upload , function(req,res,next){
  console.log(req.body)
  forward_post({
    org_id : req.body.org_id,
    sess_name : req.body.sess_name,
    sess_ini_did : req.body.sess_ini_did
  },'/api/v1/org/attendance/new_session',function(error, response, body){
    console.log(body)
    if (response.statusCode == 200) {
      res.send(body)
      res.end()
    }
  })
})

app.post('/app/attendance/verify_user' , upload, function (req, res, next) {
  console.log(req.files[0])
  var form = new FormData();
  if(req.files.length > 0){
    form.append("org_id",req.body.org_id)
    form.append("sess_id",req.body.sess_id)
    form.append("images", fs.createReadStream(req.files[0].path));
    var r = request.post('http://172.30.0.1:2020/api/v1/whoisit/org', headers= headers, requestCallback);
    r._form = form;

    function requestCallback(err, response, body) {

      res.send(body)
      res.end()
    }

  }
})

app.post('/app/attendance/sessions/list', upload, function(req,res,next){

  console.log("Probing Session List Holders for initiator : " + req.body.initiator)
  request.get({
    headers: {'content-type' : 'application/json'},
    url:     'http://172.30.0.1:2020/api/v1/org/attendance/sessions/list',
    body:    {
      'initiator' : req.body.initiator
    },
    json :  true,
  }, function(error, response, body){
    if (response.statusCode == 200) {
      res.send(JSON.stringify(body))
      res.end()
    }
  })
})




app.listen(2017)
