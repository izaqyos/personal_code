var expect = require('chai').expect,
        helloWorld = require('../helloWorldClass.js');

describe( 'printHelloWorld', function(){
        it('should print hello world when passed nothing',function(){
                console.log("printHelloWorld=%s",helloWorld.printHelloWorld() );
                expect(helloWorld.printHelloWorld() ).to.equal("Hello World. This is a demo of basic nodejs");
        })
});
