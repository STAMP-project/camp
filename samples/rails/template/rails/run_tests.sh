#!/usr/bin/env sh

#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

# Start the services needed to run test on Ruby on Rails
# documentation at:
# https://edgeguides.rubyonrails.org/development_dependencies_install.html

set -o errexit
set -o errtrace
set -o pipefail
set -o nounset

# Configure and Start MySQL
sed -i "a [mysqld]\nbind-address=127.0.0.1\n" /etc/mysql/my.cnf
service mysql start
mysql -u root <<EOF
   CREATE  USER 'rails'@'localhost'; 
   GRANT ALL PRIVILEGES ON activerecord_unittest.* to 'rails'@'localhost'; 
   GRANT ALL PRIVILEGES ON activerecord_unittest2.* to 'rails'@'localhost'; 
   GRANT ALL PRIVILEGES ON inexistent_activerecord_unittest.* to 'rails'@'localhost'; 
EOF

# Configure and start PostgreSQL
service postgresql start
su postgres -c "createuser --superuser root"

# Start the redis server
service redis-server start

# Start the memcached service
service memcached start

# Initialise the databases
(cd activerecord && bundle exec rake db:create)

# Run all the test
bundle exec rake test TESTOPTS="--ci-report"
