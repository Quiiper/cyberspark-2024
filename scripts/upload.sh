#!/bin/bash

categories=("crypto"  "foren"  "misc"  "pwn"  "rev"  "web")

for category in "${categories[@]}"
do
    echo "Uploading $category"
    mapfile -t challenges < <(ls ../challenges/$category)
    if [ ${#challenges[@]} -ne 0 ]; then
        for challenge in "${challenges[@]}"
        do
            echo "Uploading $challenge"
        done
    fi
done