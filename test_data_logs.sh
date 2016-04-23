#!/bin/bash

set -ex

function url() {
    echo "http://localhost:9200/logstash"
}

function create_index() {
    local url="$(url)"
    curl -XPUT "$url"
}

function create_mappings() {
    local url="$(url)"
    curl -XPUT "${url}/_mapping/logs" -d '
    {
        "properties": {
            "@timestamp": {
                "type": "date"
            }
        }
    }'
}

function log() {
    # Usage: log <severity> <msg>
    local url="$(url)/logs"
    local timestamp="$(date --rfc-3339=s | sed 's/ /T/')"
    local msg=$2
    local hostname=$(hostname)
    local severity=$1
    local facility="user"
    local tag="${0}[${PID}]:"
    local programname=$0
    local cmdline=$0
    local exe=$0
    local openstack_log=False
    local logger_name=main
    local openstack_process=nova
    local openstack_request_id=1234
    local openstack_user_id=5678
    local code_file=main.py
    local code_func=main
    local code_line=1
    local thread_name=main

    curl -XPOST "$url" -d '
    {
        "@timestamp": "'"$timestamp"'",
        "message": "'"$msg"'",
        "hostname": "'$hostname'",
        "severity": "'$severity'",
        "facility": "'$facility'",
        "tag": "'$tag'",
        "programname": "'$programname'",
        "cmdline": "'$cmdline'",
        "exe": "'$exe'",
        "uid": "'$UID'",
        "gid": "'$GID'",
        "pid": "'$PID'",
        "openstack_log": "'$openstack_log'",
        "logger_name": "'$logger_name'",
        "openstack_process": "'$openstack_process'",
        "openstack_request_id": "'$openstack_request_id'",
        "openstack_user_id": "'$openstack_user_id'",
        "code_file": "'$code_file'",
        "code_func": "'$code_func'",
        "code_line": "'$code_line'",
        "thread_name": "'$thread_name'"
    }'
}

create_index
create_mappings
log info "Hello, world"
sleep 1
log err "Hello, again"
