#!/bin/sh

# The purpose of this script is to import students from the ECS
# enrollements system into a given course.
if [ -z $1 ]
then
	echo "usage: importStudents course year"
	exit 1;
fi

need admin-tools

echo "Creating temporary file: $1.students.$2..."
enrolments -y $2 10:$1 9:$2 | cut -f 1,19,21 --output-delimiter=',' | sed -e "s/, /,/" | sed -e "s/ ,/,/" > $1.students.$2

export PYTHONPATH="src/"
python -c "import admin; admin.importStudentsFromCSV('test.db','$1','$1.students.$2')"

