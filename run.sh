#!/bin/bash

function helpFunction() {
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

function run_day() {
    _language=$1
    _year=$2
    _day=$3

    formatted_day=$(printf '%02d' $_day)

    if [ $_language = "python" ]; then
        formatted_language="$_language"
        solutions_folder="year_$_year/solutions/python"
        filepath="$solutions_folder/day_$formatted_day.py"
        module=year_$_year.solutions.python.day_$formatted_day
        command="python -m $module"
    elif [ $_language = "julia" ]; then
        formatted_language="$_language "
        solutions_folder="year_$_year/solutions/julia"
        filepath="$solutions_folder/day_$formatted_day.jl"
        command="julia $filepath"
    fi

    if [ ! -f "$filepath" ]; then
        echo "ERROR: $filepath does not exist."
        exit 1
    fi

    echo "**********************************************"
    echo "**** YEAR $_year - DAY $formatted_day - LANGUAGE $formatted_language ****"
    echo "**********************************************"

    time $command
}

function main() {

    if [ $language = "python" ]; then
        solutions_folder="year_$year/solutions/python"
        extension="py"
    elif [ $language = "julia" ]; then
        solutions_folder="year_$year/solutions/julia"
        extension="jl"
    else
        echo "Programming language $language is not supported. Valid options are: ('python', 'julia')"
        exit 1
    fi

    if [ "$day" = "all" ]; then
        for file in $solutions_folder/*.$extension
        do
            _day=$(echo $file | awk '{n=split($0,parts,"[._]"); print parts[n-1]}' | sed 's/^0*//')
            run_day $language $year $_day
        done
    else
        run_day $language $year $day
    fi
}

main
