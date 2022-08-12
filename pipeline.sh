#!/bin/bash
set -ex

test_method_pattern="*"
test_class_pattern="test_*.py"

# Prevent xray patching in test
export IS_TEST=TRUE

# Type checking
export MYPYPATH=src
pipenv run mypy src

# format if -f is present
formatted=0;

while getopts ":c:m:f :u" opt; do
case $opt in
    f) pipenv run black . ; formatted=1; ;;
    c) test_class_pattern="$OPTARG.py" ;;
    m) test_method_pattern="$OPTARG" ;;
    u) export IS_UPDATE=true; ;;
   \?) echo "Invalid option: -$OPTARG" >&2 && exit 1 ;;
esac
done

# Style Guide Enforcement
pipenv run flake8 .

# Code coverage
pipenv run coverage erase

echo -e "\nTEST CASE FILTER :\n\tclass: '${test_class_pattern}'\n\tmethod: '${test_method_pattern}'\n"
# Unit tests
pipenv run coverage run --branch "--omit=*/test*,*/__init__.py" --source=src -a -m unittest discover -v --pattern "${test_class_pattern}" -k "${test_method_pattern}"

# Enforce formatting
! (( $formatted )) && (pipenv run black . --check || (echo "Files are not formatted correctly, see README for details on auto formatting" && exit 1))