#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from flask import Flask



app = Flask("Greetings")


@app.route('/hello/<name>')
def hello(name):
    return "Hello '%s'!" % name


if __name__ == '__main__':
    app.run(host="0.0.0.0")
