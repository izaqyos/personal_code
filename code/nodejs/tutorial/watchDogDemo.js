const evtEmitter = require('events');

class MyEmitter extends evtEmitter {
  constructor() {
    super(); //must call super for "this" to be defined.
  }
}

console.log('simple emmitter demo');
const myEmitter = new MyEmitter();
myEmitter.on('event1', () => {
                console.log('************');
  console.log('an event occurred!');
                console.log('************');
});
myEmitter.emit('event1');

class WatchDog extends evtEmitter{

        constructor(){
                super(); //defines this
                console.log('WatchDog::constructur() ');
                this.envVarToWatch = 'NODE_ENV';
                this.envVarToWatchValue = process.env.NODE_ENV;
                this.fileToWatch = 'test';
                this.shouldStop=false;
        }

        emitEnvVarChanged(envName){
                console.log('WatchDog::emitEnvVarChanged() ');
                this.emit('envVarHasChanged', 'NODE_ENV'); 
        }

        checkEnvVarHasChanged(){
                console.log('WatchDog::checkEnvVarHasChanged() ');
                this.curVal = process.env.NODE_ENV;
                if (this.curVal !== this.envVarToWatchValue){
                    console.log('WatchDog::checkEnvVarHasChanged() detected change'); 
                    //this.emitEnvVarChanged('NODE_ENV'); 
                }
                this.emitEnvVarChanged('NODE_ENV'); // for real check put in above condition. I want to simulate change so emit always
        }

        sleep(ms) {
          return new Promise(resolve => setTimeout(resolve, ms));
        }

        async startWatch(ms){
                console.log('WatchDog::startWatch() for the night is cold and full of terror');
                this.shouldStop = false; //stop by calling stopWatch 
                while (!this.shouldStop){
                    //console.log('WatchDog::startWatch() before sleep');
                        await this.sleep(ms);
                        this.checkEnvVarHasChanged();
                    //console.log('WatchDog::startWatch() after sleep');
                }
        }

        stopWatch(){
                console.log('WatchDog::stopWatch() ');
                this.shouldStop = true; 
        }
}

const wd = new WatchDog();
wd.on('envVarHasChanged', function(envName){
                console.log('************');
                console.log('WatchDog::on(envVarHasChanged) called for env var %s', envName);
                console.log('************');
        });


//watchdog using setTimeout.
//wd.startWatch(1000); //ms

//watchdog using setInterval - more efficient since manual loop implementation is not required
const intervalId = setInterval(function() { wd.checkEnvVarHasChanged();}, 2000);
//wd.emit('envVarHasChanged');


console.log('more complex emmitter demo. A WatchDog thread the checks for a condition ever x ms and emits an event when condition is met');
