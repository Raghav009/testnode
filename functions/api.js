const express = require('express')
const serverless = require('serverless-http');
const app = express()
const port = 3000;
const router = express.Router();
const axios = require('axios');

// app.use(express.json());
app.get('/', (req, res) => {
  res.send('Get Request!')
})

app.get('/temp', function (req, res) {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
  })
  countdown(res, 10)
})

var id = 'iiotqzna-brewery-v1.0.0';
var secret = 'vZFm1C7j1Htb9JLJGmit0004VVU2dUvvemcmnlYEayX';
var base64token = btoa(id + ':' + secret);
var _provider = id.split('-')[0];
var _appName = id.split('-')[1];
var _version = id.split('-')[2];

let data = JSON.stringify({
  "grant_type": "client_credentials",
  "appName": `${_appName}}`,
  "appVersion": `${_version}`,
  "hostTenant": `${_provider}`,
  "userTenant": `${_provider}`
});

let config = {
  method: 'post',
  maxBodyLength: Infinity,
  url: 'https://gateway.eu1.mindsphere.io/api/technicaltokenmanager/v3/oauth/token',
  headers: {
    'X-SPACE-AUTH-KEY': `Bearer ${base64token}`,
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin':'*',
    'Accept':'*/*',
    'mode':'no-cors'
  },
  data: data
};


app.get('/token', function (req, res) {
  axios.request(config)
  .then((response) => {
    res.send(JSON.stringify(response.data));
  })
  .catch((error) => {
    res.send(error);
  });
})

function getRandomArbitrary(min, max) {
  return Math.random() * (max - min) + min;
}

function countdown(res, count) {
  res.write("data: " + count + " temp:" + getRandomArbitrary(101, 105) + "\n\n")
  if (count)
    setTimeout(() => countdown(res, count - 1), 1000)
  else
    res.end()
}
app.use('/static', express.static('dist'))

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

// app.use('/.netlify/functions/api', router);
// module.exports.handler = serverless(app);

//  curl localhost:3000

// curl --header 'content-type:application/json' localhost:3000/hello --data '{"name":"raghava"}'