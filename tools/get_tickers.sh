#!/bin/bash

# Grab stock tickers from the exchanges api
#
# heavily inspired by: https://github.com/rreichel3/US-Stock-Symbols/blob/main/.github/workflows/fetch-stocks.yml
#
# Expected to be run from the tools directory of this project and will populate the tickers list in resources

if [[ ! -x $(which jq) ]]; then
    echo "This requires the 'jq' command"
    return -1
fi

if [[ ! -x $(which curl) ]]; then
    echo "This requires the 'curl' command"
    return -1
fi



USER_AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'

NASDAQ_FILE="https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/refs/heads/main/nasdaq/nasdaq_tickers.txt"
NYSE_FILE="https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/refs/heads/main/nyse/nyse_tickers.txt"


RESOURCE_PATH="../resources"

if [[ ! -d $RESOURCE_PATH ]]; then
	mkdir -p $RESOURCE_PATH
fi



curl --user-agent "$USER_AGENT" $NASDAQ_FILE > $RESOURCE_PATH/nasdaq_tickers.txt
curl --user-agent "$USER_AGENT" $NYSE_FILE > $RESOURCE_PATH/nyse_tickers.txt


