#!/bin/bash

# This utility converts a simple .dat file to json

FILE="$1"
DIR="$(dirname $0)"
OUTFILE="$DIR/${FILE%.*}.json"

cat "$FILE" | sed -re \
	':a;$!{N;ba};s|/\*[^*]*\*+([^/*][^*]*\*+)*/||' | sed \
	-e 's,\( *//.*$\),,g' \
	-e 's/;/\n/g' | sed \
	-e '/^\s*$/d' \
	-e 's/ *\(.*\) */\1/g' \
	-e 's/\([^ ]*\) *= */"\1":/g' \
	-e 's/\[ */\[/g' \
	-e 's/ *\]/\]/g' \
	-e 's/ /,/g' | \
	paste -d, -s | sed \
	-e 's/^\(.*\)$/\{\1\}/g' | \
	jq . > "$OUTFILE"
