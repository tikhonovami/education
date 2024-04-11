#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "task11" --file "create_table.sql"

