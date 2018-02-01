#!/bin/sh
# vim: sw=2 ai expandtab
#    start.sh exists as part of the pipcache repository.
#    It's used to start the actual devpi-server and ensure proper locking so
#    more than once instance is not started inadvertently.
#
#    Copyright (C) 2018  Billy Holmes
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

: ${DEVPI_DATA_VOLUME:="/opt/app-root/data"}
: ${DEVPI_SERVER_PORT:="8080"}
: ${DEVPI_EXTRA_ARGS:=}

LOCK_FILE="$DEVPI_DATA_VOLUME/.lockfile"
USER_DATA="$DEVPI_DATA_VOLUME/userdata"

DEVPI=/opt/app-root/bin/devpi-server
ARGS=" --serverdir=$USER_DATA"
ARGS+=" --host=0.0.0.0"
ARGS+=" --port=$DEVPI_SERVER_PORT"

err() {
	echo "$@" >&2
	exit 1
}

mkdir -p $USER_DATA || err "Unable to create $USER_DATA"

exec 200>>$LOCK_FILE
flock -xn 200 || err "Unable to acquire lock on $LOCK_FILE - only one instance can run at a time!"

NUM_FILES=$(find $USER_DATA -type f | wc -l)
set $NUM_FILES
NUM_FILES=$1

if [ $NUM_FILES -eq 0 ] ; then
  echo "Initializing $USER_DATA" 
  $DEVPI $ARGS --init || err "Unable to initialize $USER_DATA"
fi

echo "Starting Server..."
exec $DEVPI $ARGS $DEVPI_EXTRA_ARGS
