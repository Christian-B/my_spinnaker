#!/bin/bash
RC="global_strict"
STRICT_RC="foo.py"
RELAXED_RC="bar.py"

if [ "$RC" = "global_relaxed" ]; then
  RC="$RELAXED_RC"
  echo "Using global relaxed rcfile $RC"
elif [ "$RC" = "global_strict" ]; then
  RC="$STRICT_RC"
  echo "Using global strict rcfile $RC"
else
  echo "Using local rcfile $RC"
fi

