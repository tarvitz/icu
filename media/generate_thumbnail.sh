#!/bin/bash
[ ! -z $1 ] && FORCE=$1

for i in *[!_thmb].png
do
    new_img=${i/.png/_thmb.png}
    if [[ ! -f $new_img && ! $FORCE ]]; then
        convert ${i} -resize 200x150 ${new_img}
    elif [[ -f $new_img && ! $FORCE ]]; then
        # nothing to do
        echo "$i skipped"
    else
        convert ${i} -resize 200x150 ${new_img}
    fi
    echo $i
done
