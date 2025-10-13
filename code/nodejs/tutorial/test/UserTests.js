var expect = require('chai').expect;
var assert = require('chai').assert;
const User = require('../sinonDemo.js');
const Manager = require('../sinonDemoManager.js');

var sinon = require('sinon');

//spy keeps tab on target function calls. letting you know how many times it was called and with which arguments
describe ("getName", function(){

        it('should call getName once', function(){
                yosi = new User('yosi', 'izaq');
                var getNameSpy = sinon.spy(User.prototype, "getName"); //stub class getName
                //var getNameSpy = sinon.spy(yosi, "getName"); //stub single instance getName

                yosi.getName();

                getNameSpy.restore();
                assert(getNameSpy.calledOnce);
        });
});



//sinon stubs repace a method so we can verify the method was called but avoid running blocking methods (like waiting for external server response)
//describe.skip and xit instead of it -> skip tests 
describe("saveToDB", function(){

        it('should call saveToDB but use a stub to avoid waiting', function(){
                yosi = new User('yosi', 'izaq');
                var saveToDBStub = sinon.stub(yosi, "saveToDB");

                yosi.saveToDB();

                //saveToDBStub.should.have.been.called();
                saveToDBStub.restore();
                assert(saveToDBStub.called);
        });
});

//sinon mock gives full power to mimic method calls expected results.
describe ('hireNewEmployee', function(){
        it('should create a user and call hireNewEmployee', function(){
        yosi = new User('yosi', 'izaq');
        var userMock = sinon.mock(yosi) ;
        //var userMock = sinon.mock(User.prototype) ;

        userMock.expects('setName').once().withArgs(yosi.fname, yosi.lname);
        userMock.expects('saveToDB').once().withArgs();
        userMock.expects('getName').once().withArgs().returns('yosi');
        manager = new Manager("guy mosko");
        manager.hireNewEmployee(yosi);

        userMock.verify();
        userMock.restore();

        });

});

//describe ('Manager constructor', function(){
//        it('should call manager constructor', function(){
//
//        })
//});

