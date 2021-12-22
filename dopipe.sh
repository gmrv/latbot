#!/bin/bash

rm ./common/commandpipe
mkfifo ./common/commandpipe

while true;
  do eval "$(cat ./common/commandpipe)" &> ./common/output;
done
