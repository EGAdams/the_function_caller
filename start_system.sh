#!/bin/bash
# 
# first friday
#
# script to start the agent communication system


# define the aliases used in this script
# source ~/.bashrc;

# go into the correct environment
# so;

# set the OPENAI_API_KEY
export OPENAI_API_KEY=`cat little_panera_cold`

# run the Python start system script
python3 ~/the_function_caller/start_system.py;

# the end; hello first friday
