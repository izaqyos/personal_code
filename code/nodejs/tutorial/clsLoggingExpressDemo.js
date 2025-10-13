// based on blog https://itnext.io/nodejs-logging-made-right-117a19e8b4ce
//
const { createLogger, format, transports } = require('winston')
//const printf = require('printf')

const addTraceId = format((info) => {
  let message = info.message
  const traceID = clsNamespace.get('taceID')
  if (traceID) {
    message = `[TraceID: ${traceID}]: ${message}`
  }
  return message
})

const logger = createLogger({
  format: addTraceId,
  transports: [new transports.Console()],
})

var  express = require('express');
const cls = require('cls-hooked')
const uuidv4 = require('uuid/v4')

const clsNamespace = cls.createNamespace('app')

const clsMiddleware = (req, res, next) => {
  console.log("setting cls");
  // req and res are event emitters. We want to access CLS context inside of their event callbacks
  clsNamespace.bind(req)
  clsNamespace.bind(res)

  const traceID = uuidv4()

  clsNamespace.run(() => {
    clsNamespace.set('traceID', traceID)

    next()
  })
}

const controller = (req) => {
  console.log("controller getting traceID");
  const traceID = clsNamespace.get('traceID')
  console.log("controller traceID ", traceID);
  return traceID;
}

var app = express();

app.use(clsMiddleware);

app.get('/', function(req, res){
        let traceID = controller(req);
        res.send(`Hello CLS namespace. context ID ${traceID} !!`);
});

var server = app.listen(8081, function(){
        var host = server.address().address ;
        var port = server.address().port ;

        console.log("Example server listening at http://%s:%s",host, port);
});



