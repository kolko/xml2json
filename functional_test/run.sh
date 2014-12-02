#!/bin/bash
set -eu

for inp_file in ./input*.xml; do
	_tmp=${inp_file//*_};
	number=${_tmp//.xml};
	echo -n "Test #${number}...     ";
	cat $inp_file | python ../xml2json.py >/tmp/xml2json_test
	if python json_diff.py /tmp/xml2json_test output_${number}.json; then
		echo "[  ok  ]"
	else
		echo "[ FAIL ]"
		break
	fi
done
