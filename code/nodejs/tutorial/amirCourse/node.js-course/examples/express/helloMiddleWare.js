module.exports = (func) => {

        return function(req, res, next){
                console.log("dummy filter...");
                res.setHeader("X-Dummy-Header",func());
                next();
        };
};


