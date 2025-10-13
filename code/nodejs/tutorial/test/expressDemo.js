var request = require('supertest');
var app = require('../server/index.js');
var expect = require('chai').expect;
var sinon = require('sinon');

describe('get /', function(){
        it('should return correct users', function(){
                request(app)
                .get( '/api/users')
                .expect('Content-Type', /json/)
                .expect({ '0': 'boris', '1': 'dean', '2': 'asaf', '3': 'yosi' })
                .expect(200);
                });
        });


