#!/usr/bin/env bash

function jdcd() { cd     "$(jdGetIndexPath.py "${1}")" }
function jdls() { ls     "$(jdGetIndexPath.py "${1}")" }
function jdll() { ls -la "$(jdGetIndexPath.py "${1}")" }
function jdla() { ls -a  "$(jdGetIndexPath.py "${1}")" }

# Example usage:
# $ jdcd 23   # change directory to area 23
