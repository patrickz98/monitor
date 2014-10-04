#!/bin/bash

NOW=$(date +"%Y-%m-%d")

DB_USER="monitor"
DB_PASS="test123"
DB_NAME="monitor"
DB_FILE="monitor.$NOW.sql"

mysqldump -u$DB_USER -p$DB_PASS $DB_NAME > $DB_FILE

