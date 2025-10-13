module.exports = (param) => {

    return function(req, res, next){
            // route filter which validates the given id
            if (req.params[param].length > 4) {
                    next();
            } else {
                    next({message: "Error: not valid param", status: 400});
            }
    };
};



