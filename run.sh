#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -l language -y year -d day"
   echo -e "\t-l Programming language to use (python, julia)"
   echo -e "\t-y Year of the Advent of Code competition (2020, 2021)"
   echo -e "\t-d Day of the puzzle (1 to 25)"
   exit 1 # Exit script after printing helpFunction
}

while getopts "l:y:d:" opt
do
   case "$opt" in
      l ) language="$OPTARG" ;;
      y ) year="$OPTARG" ;;
      d ) day="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$language" ] || [ -z "$year" ] || [ -z "$day" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi


function main() {
    formatted_day=$(printf '%02d' $day)

    echo "**********************************************"
    echo "**** YEAR $year - DAY $formatted_day - LANGUAGE $language ****"
    echo "**********************************************"

    if [ $language = "python" ]; then extension="py"; else extension="jl"; fi
    solutions_folder=year_$year/solutions/$language
    filepath=$solutions_folder/day_$formatted_day.$extension

    if [ ! -f "$filepath" ]; then
        echo "ERROR: $filepath does not exist."
        exit 1
    fi

    if [ $language = "python" ]; then
        module=year_$year.solutions.python.day_$formatted_day
        time python -m $module
    elif [ $language = "julia" ]; then
        time julia $filepath
    else
        echo "Programming language $language is not supported. Valid options are: ('python', 'julia')"
    fi
}

main
