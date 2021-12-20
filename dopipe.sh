#!/bin/bash

rm commandpipe
mkfifo commandpipe

while true;
  do eval "$(cat ./common/commandpipe)" &> ./common/output;
done
