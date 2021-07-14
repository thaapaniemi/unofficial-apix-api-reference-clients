#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# SendInvocieZIP -method implemented as shell script
# requirements: bash, sha256sum, curl

[ "$#" -eq 6 ] || { echo "Usage: $0 <test/prod/ENDPOINT> <TRANSFER_ID> <TRANSFER_KEY> <SOFTWARE_NAME> <SOFTWARE_VERSION> <FILEPATH>" >&2; exit 1;}

readonly ENVIRONMENT=$1;
readonly TRANSFER_ID=$2;
readonly TRANSFER_KEY=$3;
readonly SOFTWARE_NAME=$4;
readonly SOFTWARE_VERSION=$5;
readonly FILEPATH=$6;

ENDPOINT=$ENVIRONMENT;
if [ "$ENVIRONMENT" = "prod" ]; then
    ENDPOINT="https://api.apix.fi/invoices"
elif [ "$ENVIRONMENT" = "test" ]; then
    ENDPOINT="https://test-api.apix.fi/invoices"
fi

readonly TIMESTAMP=`date --utc +%Y%m%d%H%M%S`;

#awk version
#readonly DIGEST=$(echo -n "$SOFTWARE_NAME+$SOFTWARE_VERSION+$TRANSFER_ID+$TIMESTAMP+$TRANSFER_KEY"|sha256sum|awk '{ print $1 }');

#cut version
readonly DIGEST=$(echo -n "$SOFTWARE_NAME+$SOFTWARE_VERSION+$TRANSFER_ID+$TIMESTAMP+$TRANSFER_KEY"|sha256sum|cut -d ' ' -f 1);

readonly URL="${ENDPOINT}?soft=${SOFTWARE_NAME}&ver=${SOFTWARE_VERSION}&TraID=${TRANSFER_ID}&t=${TIMESTAMP}&d=SHA-256%3A${DIGEST}";

curl -X PUT --data @${FILEPATH} -H "Content-Type: application/octet-stream" $URL

