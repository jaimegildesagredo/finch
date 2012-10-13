var RoboHydraHead = require('robohydra').heads.RoboHydraHead;

exports.getBodyParts = function (conf) {
    return {
        heads: [
            new RoboHydraHead({
                name: 'users',
                path: '/users',
                handler: function(req, res) {
                    var result;

                    // HTTP Basic Auth for user 'admin' and password 'admin'
                    if (req.queryParams.auth) {
                        if (req.headers.authorization != 'Basic YWRtaW46YWRtaW4=') {
                            res.statusCode = 401;
                            res.send('Unauthorized');
                        }
                    }

                    if (req.method == 'POST') {
                        result = JSON.parse(req.rawBody.toString());
                        result.id = 1;
                    } else {
                        result = [
                            {name: 'Jack', id: 1},
                            {name: 'Jack', id: 2}
                        ];
                    }

                    res.send(JSON.stringify(result));
                }
            }),
            new RoboHydraHead({
                name: 'user',
                path: '/users/:id',
                handler: function(req, res) {
                    // HTTP Basic Auth for user 'admin' and password 'admin'
                    if (req.queryParams.auth) {
                        if (req.headers.authorization != 'Basic YWRtaW46YWRtaW4=') {
                            res.statusCode = 401;
                            res.send('Unauthorized');
                        }
                    }

                    res.send(JSON.stringify({name: 'Jack', id: req.params.id}));
                }
            })
        ]
    }
};
