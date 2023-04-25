#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# AuthenticateByUser -method implemented as shell script
# requirements: bash, sha256sum, curl

[ "$#" -eq 3 ] || { echo "Usage: $0 <test/prod/ENDPOINT> <email> <password>" >&2; exit 1;}

readonly ENVIRONMENT=$1;
readonly EMAIL=$2;
readonly PASSWORD=$3;

ENDPOINT=$ENVIRONMENT;
if [ "$ENVIRONMENT" = "prod" ]; then
    ENDPOINT="https://api.apix.fi/authuser"
elif [ "$ENVIRONMENT" = "test" ]; then
    ENDPOINT="https://test-api.apix.fi/authuser"
fi

readonly TIMESTAMP=`date --utc +%Y%m%d%H%M%S`;

#cut version
readonly SHAPASS=$(echo -n "$PASSWORD"|sha256sum|cut -d ' ' -f 1);
readonly DIGEST=$(echo -n "$EMAIL+$TIMESTAMP+$SHAPASS"|sha256sum|cut -d ' ' -f 1);

readonly URL="${ENDPOINT}?uid=${EMAIL}&t=${TIMESTAMP}&d=SHA-256%3A${DIGEST}";

curl -X GET $URL

