#!/usr/bin/env bash

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - — - - - -
# Script to execute "Camus" to consume and upload kafka messages to HDFS
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - — - - - - 

cd /usr/local/hadoop/etc/hadoop/
hadoop jar camus-example-0.1.0-SNAPSHOT-shaded.jar com.linkedin.camus.etl.kafka.CamusJob -P /usr/local/camus/camus-example/src/main/resources/camus.properties



