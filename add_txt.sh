#!/bin/bash

seq=`ls`

for x in $seq;do
	mv $x $x.txt
done
