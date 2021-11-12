#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# ListInvoiceZIPs -method implemented as shell script
# requirements: bash, sha256sum, curl

[ "$#" -eq 3 ] || { echo "Usage: $0 <test/prod/ENDPOINT> <TRANSFER_ID> <TRANSFER_KEY>" >&2; exit 1;}

readonly ENVIRONMENT=$1;
readonly TRANSFER_ID=$2;
readonly TRANSFER_KEY=$3;

ENDPOINT=$ENVIRONMENT;
if [ "$ENVIRONMENT" = "prod" ]; then
    ENDPOINT="https://terminal.apix.fi/list2"
elif [ "$ENVIRONMENT" = "test" ]; then
    ENDPOINT="https://test-terminal.apix.fi/list2"
fi

readonly TIMESTAMP=`date --utc +%Y%m%d%H%M%S`;

#awk version
#readonly DIGEST=$(echo -n "$TRANSFER_ID+$TIMESTAMP+$TRANSFER_KEY"|sha256sum|awk '{ print $1 }');

#cut version
readonly DIGEST=$(echo -n "$TRANSFER_ID+$TIMESTAMP+$TRANSFER_KEY"|sha256sum|cut -d ' ' -f 1);

readonly URL="${ENDPOINT}?TraID=${TRANSFER_ID}&t=${TIMESTAMP}&d=SHA-256%3A${DIGEST}";

curl -X GET $URL

