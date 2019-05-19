const request = require('request')
const cbor = require('cbor');

request.get("http://localhost:8008/state/f56705daba9209c9c17f49b9d964772aba016c2f91bbcc966bd1c394a046c06c98dc0x",function(err,resp,body){

  data = JSON.parse(body)
  if(data.error){
    console.log("ERROR")
  }
  let buff = new Buffer(data.data, 'base64');
  cborx = cbor.decodeAllSync(buff)[0];
  console.log(cborx)
})
