const express = require('express')
const serverless = require('serverless-http');
const app = express()
const port = 3000;
const router = express.Router();

// app.use(express.json());
app.get('/', (req, res) => {
  res.send('Get Request!')
})

app.get('/temp', function(req, res) {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
  })
  countdown(res, 10)
})


function getRandomArbitrary(min, max) {
  return Math.random() * (max - min) + min;
}

function countdown(res, count) {
  res.write("data: " + count + " temp:" + getRandomArbitrary(101, 105) +"\n\n")
  if (count)
    setTimeout(() => countdown(res, count-1), 1000)
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