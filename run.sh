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
    response="$(/Users/stay/miniconda3/bin/python chatgpt.py --mode bill)"
    echo $response
    exit
fi

# save prompt and response to two newly created files in /tmp
tmp_file_suffix=$(cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)

# get prompt from command line argument
prompt=$2
# if no command line argument, get prompt from clipboard
if [ -z "$prompt" ]; then
    prompt=$(pbpaste)
fi


# get reponse from python script "--debug"
response=$(/Users/stay/miniconda3/bin/python chatgpt.py --mode oneshot --prompt "$prompt" --type $type)

# copy response to macos clipboard
printf "%s" "$response" | pbcopy

# if type is revise, use .txt otherwise use .md
if [ "$type" = "revise" ]; then
    prompt_file="/tmp/cai/prompt_$tmp_file_suffix.txt"
    response_file="/tmp/cai/response_$tmp_file_suffix.txt"
else
    prompt_file="/tmp/cai/prompt_$tmp_file_suffix.md"
    response_file="/tmp/cai/response_$tmp_file_suffix.md"
fi

# create the directory if it doesn't exist
mkdir -p /tmp/cai

printf "%s" "$prompt" > "$prompt_file"
printf "%s" "$response" > "$response_file"

# for revise mode, use vscode to diff the two files
if [ "$type" = "revise" ]; then
    code --diff $prompt_file $response_file
    exit
fi

# open the markdown file in vscode, use command + shift + v to preview
code $response_file