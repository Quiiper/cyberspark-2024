#!/bin/bash

categories=("crypto"  "foren"  "misc"  "pwn"  "rev"  "web")

for category in "${categories[@]}"
do
    echo "Uploading $category"
    mapfile -t challenges < <(ls ../challenges/$category)
    if [ ${#challenges[@]} -ne 0 ]; then
        for challenge in "${challenges[@]}"
        do
            if [ ! -f ../challenges/$category/$challenge/challenge.yml ]; then
                echo "Skipping $challenge, no challenge.yml found"
                continue
            fi
            ctf challenge install "challenges/$category/$challenge"
        done
    fi
done