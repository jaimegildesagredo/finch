var RoboHydraHead = require('robohydra').heads.RoboHydraHead;

exports.getBodyParts = function (conf) {
    return {
        heads: [
            new RoboHydraHead({
                path: '/users',
                handler: function(req, res) {
                    var result;

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
            })
        ]
    }
};
