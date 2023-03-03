#!/bin/bash
IFS=
# You need to set the following environment variables here or somewhere else like Alfred
# export OPENAI_API_KEY=

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd "$SCRIPTPATH"

# get type from command line argument
type=$1

# if type=bill
if [ "$type" = "bill" ]; then
    response="$(python chatgpt.py --mode bill)"
    echo $response
    exit
fi

# get prompt from command line argument
prompt=$2
# if no command line argument, get prompt from clipboard
if [ -z "$prompt" ]; then
    prompt=$(pbpaste)
fi


# get reponse from python script "--debug"
response="$(python chatgpt.py --mode oneshot --prompt "$prompt" --type $type)"

# copy response to macos clipboard
echo $response | pbcopy

# save prompt and response to two newly created files in /tmp
echo $prompt > /tmp/prompt.txt
echo $response > /tmp/response.txt

# use vscode to diff the two files
code --diff /tmp/prompt.txt /tmp/response.txt