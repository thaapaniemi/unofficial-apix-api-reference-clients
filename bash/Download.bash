#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Download -method implemented as shell script
# requirements: bash, sha256sum, curl

[ "$#" -eq 4 ] || { echo "Usage: $0 <test/prod/ENDPOINT> <STORAGE_ID> <STORAGE_KEY> <FILENAME>" >&2; exit 1;}

readonly ENVIRONMENT=$1;
readonly STORAGE_ID=$2;
readonly STORAGE_KEY=$3;
readonly FILENAME=$4;
readonly MARKRECEIVED="no";

ENDPOINT=$ENVIRONMENT;
if [ "$ENVIRONMENT" = "prod" ]; then
    ENDPOINT="https://terminal.apix.fi/download"
elif [ "$ENVIRONMENT" = "test" ]; then
    ENDPOINT="https://test-terminal.apix.fi/download"
fi

readonly TIMESTAMP=`date --utc +%Y%m%d%H%M%S`;

#awk version
#readonly DIGEST=$(echo -n "$MARKRECEIVED+$STORAGE_ID+$TIMESTAMP+$STORAGE_KEY"|sha256sum|awk '{ print $1 }');

#cut version
readonly DIGEST=$(echo -n "$MARKRECEIVED+$STORAGE_ID+$TIMESTAMP+$STORAGE_KEY"|sha256sum|cut -d ' ' -f 1);

readonly URL="${ENDPOINT}?SID=${STORAGE_ID}&t=${TIMESTAMP}&markreceived=${MARKRECEIVED}&d=SHA-256%3A${DIGEST}";

curl -X GET $URL --output $FILENAME

