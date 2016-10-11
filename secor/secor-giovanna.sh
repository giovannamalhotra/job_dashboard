#!/usr/bin/env bash

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - — - - - - - - - - -
# Script to execute "Secor" to consume and upload kafka messages to Amazon S3
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - — - - - - - - - - -

cd /usr/local/secor/bin
sudo java -ea -Dsecor_group=secor_backup -Dlog4j.configuration=log4j.prod.properties -Dconfig=secor.prod.backup.properties -cp secor-0.23-SNAPSHOT.jar:lib/* com.pinterest.secor.main.ConsumerMain
