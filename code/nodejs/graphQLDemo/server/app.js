const express = require('express');
const gqlHTTP = require('express-graphql');

const app = express();

const port = 4000;

app.use('/graphql', gqlHTTP({
})
);

app.listen(port, ()=>{
    console.log('server listen on port ', port);
});

