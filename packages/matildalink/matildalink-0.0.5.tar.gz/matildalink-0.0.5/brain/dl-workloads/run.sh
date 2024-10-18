#!/bin/bash
python prepare_directories.py -m remove
python prepare_directories.py -m build -p $1
python main.py -p $1 -i $2
python collect_data.py -cp $1 -i $2 -p $3
