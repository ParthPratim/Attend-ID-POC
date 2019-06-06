const express = require('express')
const fs = require('fs')
const https = require('https')
const path = require('path')
const request = require('request')
const bodyParser = require('body-parser')
const multer = require('multer')
const FormData = require('form-data');
const mime=require('mime-types');
const public = path.join(__dirname, 'public')
const cbor = require('cbor');
const crypto = require('crypto');
const DIGITAL_ID_ENDPOINT = "/api/v1/core/digital_id/tx_connector"
const ORGS_ENDPOINT = "/api/v1/core/orgs/tx_connector"

const opts = {
  key: fs.readFileSync('../keys/ssl/server.key')
  , cert: fs.readFileSync('../keys/ssl/server.pem')
  , requestCert: true
  , rejectUnauthorized: false
  , ca: [ fs.readFileSync('../keys/ssl/server.pem') ]
}

const upload = multer({dest: 'public/uploads'}).array('images')
const app = express()
app.use(express.static('public/index'))
app.use(express.static('public/dashboard'))
app.use(express.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(function (err, req, res, next) {
  console.log('This is the invalid field ->', err.field)
  next(err)
})

app.get('/', (req, res) => {
	res.sendfile(path.join(public, 'index/index.html'))
})


app.get('/dashboard/org/name', (req, res) => {
	var CN = GetCN(req)
  if(CN.localeCompare("None") == 0 ){
    res.send("Try again by selecting a valid certificate...")
    res.end()
    return
  }
  else{
    state_addr = getORGState(CN)
    getStateData(state_addr,function(response){
      if(response != null){
        res.send(response.Organization)
        res.end()
        return
      }
      else{
        res.send("ERR_BAD_SSL_CERTIFICATE")
        res.end()
      }
    })
  }
})

app.get('/dashboard/org/creator', (req, res) => {
	var CN = GetCN(req)
  if(CN.localeCompare("None") == 0 ){
    res.send("Try again by selecting a valid certificate...")
    res.end()
    return
  }
  else{
    state_addr = getORGState(CN)
    getStateData(state_addr,function(response){
      if(response != null){
        res.send(response.CreatorID)
        res.end()
        return
      }
      else{
        res.send("ERR_BAD_SSL_CERTIFICATE")
        res.end()
      }
    })
  }
})

app.get('/dashboard/org/id', (req, res) => {
   var CN = GetCN(req)
  if(CN.localeCompare("None") == 0 ){
    res.send("Try again by selecting a valid certificate...")
    res.end()
    return
  }
  else{
    res.send(CN);
    res.end();
  }
})


app.get('/dashboard/org/members', (req, res) => {
	var CN = GetCN(req)
  console.log(CN)
  if(CN.localeCompare("None") == 0 ){
    res.send("Try again by selecting a valid certificate...")
    res.end()
    return
  }
  else{
    state_addr = getORGState(CN)
    getStateData(state_addr,function(response){
      if(response != null){
        request.get({
          headers: {'content-type' : 'application/json'},
          url:     'http://127.0.0.1:2020/api/v1/org/members',
          body:    {
            action : 'GET_ORG_MEMBERS',
            org_id : CN
          },
          json :  true,
        }, function(error, response, body){
          console.log(body)
          if (response.statusCode == 200) {
            res.set({'Content-Type' : 'application/json'})
            res.send(body)
            res.end()
            return
          }
        })

      }
      else{
        res.send("ERR_BAD_SSL_CERTIFICATE")
        res.end()
      }
    })
  }
})



app.get('/up', (req, res) => {
	res.sendfile(path.join(public, 'upload.html'))
})

app.get('/dashboard', (req, res) => {
	res.sendfile(path.join(public, 'dashboard/index.html'))
})



var headers = {
    'Content-Type' : 'application/json'
};


app.post('/upload' , upload, function (req, res, next) {
  var CN = GetCN(req)

  var form = new FormData();
  form.append("folder_id", "BHAK !!!");
  form.append("filename", fs.createReadStream(req.files[0].path));
  form.append("filename", fs.createReadStream(req.files[1].path));
  form.getLength(function(err, length){
  if (err) {
    return requestCallback(err);
  }

  var r = request.post("http://127.0.0.1:6667", headers= headers, requestCallback);
  r._form = form;

});

function requestCallback(err, res, body) {
  console.log(body);
}


})

function GetCN(req){
  const cert = req.connection.getPeerCertificate()
  var CN = ""
  console.log(CN)
  if (req.client.authorized) {
    CN = cert.subject.CN
  } else {
    CN = "None"
  }
  return CN
}

var headers = {
    'Content-Type' : 'application/json'
};

app.post(DIGITAL_ID_ENDPOINT , upload, function (req, res, next) {
  var CN = GetCN(req)
   console.log(CN)

    var form = new FormData();
    console.log(req.body)
    form.append("action", req.body.action);
    form.append("uname", req.body.uname);
    form.append("cn", CN);

    console.log(req.files)
    for(i = 0 ; i < req.files.length ; i++){

      form.append("images", fs.createReadStream(req.files[i].path));
    }

    form.getLength(function(err, length){
    if (err) {
      return requestCallback(err);
    }

    var r = request.post('http://127.0.0.1:2020'+DIGITAL_ID_ENDPOINT, headers= headers, requestCallback);
    r._form = form;

  });

  function requestCallback(err, response, body) {

    if (response.statusCode == 200) {
      body = JSON.parse(body)
      res.set(body.Headers)
      res.send(Buffer.from(body.Response, "hex"))
      res.end()
    };
  }
})


app.post(ORGS_ENDPOINT+"/add_new_user" , upload, function (req, res, next) {
  var CN = GetCN(req)
  if(CN.localeCompare("None") == 0 ){
    res.send("Try again by selecting a valid certificate...")
    res.end()
    return
  }
  else{
    state_addr = getORGState(CN)
    getStateData(state_addr,function(response){
      if(response == null){
        res.send("Try again by selecting a valid certificate...")
        res.end()
        return
      }
    })
  }

  console.log("ORGS_ADD_NEW_USER...")
  if(CN.localeCompare("None") != 0 ){

    var form = new FormData();
    console.log(req.body)
    form.append("action", "create");
    form.append("uname", req.body.uname);
    form.append("cn", CN);

    console.log(req.files)
    for(i = 0 ; i < req.files.length ; i++){

      form.append("images", fs.createReadStream(req.files[i].path));
    }

    form.getLength(function(err, length){
    if (err) {
      return requestCallback(err);
    }

    var r = request.post('http://127.0.0.1:2020'+DIGITAL_ID_ENDPOINT, headers= headers, function(err,response,body){
      if(response.statusCode == 200){
        body = JSON.parse(body)
        digital_id = body.DigitalID
        bd = {
          action : 'ADD_NEW_ORG_MEMBER',
          org_name : req.body.org_name,
          creator_id : req.body.creator_id ,
          org_id : CN,
          new_member_id : digital_id,
          can_mark_attendance : req.body.can_mark_attendance
        }
        request.post({
          headers: {'content-type' : 'application/json'},
          url:     'http://127.0.0.1:2020'+ORGS_ENDPOINT,
          body:    bd,
          json :  true,
        }, function(error, response, body){
          console.log(body)
          if (response.statusCode == 200) {
            if(body.Status == 1){
              res.send('True')
            }
            else{
              res.send('False')
            }
            res.end()
          }
        });

      }
    });
    r._form = form;
  })
}
})

app.post(ORGS_ENDPOINT+"/request_model_build" , (req,res) => {
  var CN =  GetCN(req)
  console.log("MUILD");
  console.log(req.body)
  if(CN.localeCompare("None") == 0 ){
    res.send("Try again by selecting a valid certificate...")
    res.end()
    return
  }
  else{
    state_addr = getORGState(CN)
    getStateData(state_addr,function(response){
      if(response == null){
        res.send("Try again by selecting a valid certificate...")
        res.end()
      }
      else{
        bd = {
          action : 'BUILD_FR_MODEL',
          org_id : CN,
          org_name : req.body.org_name,
          creator_id : req.body.creator_id
        }

        request.post({
          headers: {'content-type' : 'application/json'},
          url:     'http://127.0.0.1:2020'+ORGS_ENDPOINT,
          body:    bd,
          json :  true,
        }, function(error, response, body){
          console.log(body)
          if (response.statusCode == 200) {
            if(body.Status == 1){
              res.send('True')
            }
            else{
              res.send('False')
            }
            res.end()
          }
        });

      }
    })
  }
})

app.post(ORGS_ENDPOINT+"/transfer_asset" , (req,res) => {
  var CN = GetCN(req)
  console.log(req.body)
  if(CN.localeCompare("None") == 0 ){
    res.send("Try again by selecting a valid certificate...")
    res.end()
    return
  }
  else{
    state_addr = getORGState(CN)
    getStateData(state_addr,function(response){
      if(response == null){
        res.send("Try again by selecting a valid certificate...")
        res.end()
      }
      else{
        sa_neworg = getORGState(req.body.new_org_id)
        getStateData(sa_neworg,function(response){
          if(response == null){
            res.send("Invalid OrgID. Send a valid orgid to transfer to.")
            res.end()
            return
          }
          else{


            bd = {
              action : 'TRANSFER_ORG_MEMBER',
              org_id : CN,
              org_name : req.body.org_name,
              creator_id : req.body.creator_id ,
              curr_member_id : req.body.curr_member_id,
              new_org_id : req.body.new_org_id,
              new_org_creator : response.CreatorID
            }

            request.post({
              headers: {'content-type' : 'application/json'},
              url:     'http://127.0.0.1:2020'+ORGS_ENDPOINT,
              body:    bd,
              json :  true,
            }, function(error, response, body){
              console.log(body)
              if (response.statusCode == 200) {
                if(body.Status == 1){
                  res.send('True')
                }
                else{
                  res.send('False')
                }
                res.end()
              }
            });


          }
        })
      }
    })
  }


})

app.post(ORGS_ENDPOINT, (req,res) => {
  var CN = GetCN(req)
  end = false;
  if(CN.localeCompare("None") == 0 ){
    res.send("Try again by selecting a valid certificate...")
    res.end()
    end = true
  }
  else{
    state_addr = getDigitalIDState(CN)
    console.log(state_addr)
    getStateData(state_addr,function(response){
      console.log(response)
      if(response == null){
        res.send("Try again by selecting a valid certificate...")
        res.end()
      }
      else{

          console.log("ORGS HANDLER...")
          bd = {

          }
              bd = {
                action : req.body.action,
                org_name : req.body.org_name,
                creator_id : CN
              }

          request.post({
            headers: {'content-type' : 'application/json'},
            url:     'http://127.0.0.1:2020'+ORGS_ENDPOINT,
            body:    bd,
            json :  true,
          }, function(error, response, body){
            console.log(body)
            if (response.statusCode == 200) {
              res.set(body.Headers)
              res.send(Buffer.from(body.Response, "hex"))
              res.end()
            }
          });

      }
    })
  }


})

app.get('/visit', (req, res) => {
  res.set({"Content-Disposition":"attachment; filename=\"Text.txt\""});
  res.send("SAMPLE FILE");
})

function sha512(msg){
  var hash = crypto.createHash('sha512');
  //passing the data to be hashed
  data = hash.update(msg, 'utf-8');
  //Creating the hash in the required format
  gen_hash= data.digest('hex');
  return gen_hash
}

function getORGState(org_id){
  base = sha512("orgs").substring(0,6)
  org_hash = sha512(org_id).substring(64)
  return base+org_hash
}

function getDigitalIDState(creator_id){
  base = sha512("digital_id").substring(0,6)
  creator_hash = sha512(creator_id).substring(64)
  return base+creator_hash
}

function getStateData(state_addr,callback){
  console.log(state_addr)

  request.get("http://172.30.0.1:8008/state/"+state_addr,function(err,resp,body){

    data = JSON.parse(body)
    if(data.error){
      console.log("ERROR")
      callback(null)
      return
    }
    let buff = new Buffer(data.data, 'base64');
    cborx = cbor.decodeAllSync(buff)[0];
    callback(cborx)
  })

}

https.createServer(opts, app).listen(2018)
