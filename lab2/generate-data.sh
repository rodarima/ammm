#!/bin/bash

python P1.py < data.json
python P2a.py < data.json
python P2c.py < data-p2.json
#for K in 0 1 2 3; do echo "K=$K"; python P2d.py $K < data-p2.json; done
python P2d.py 1 < data-p2.json
python P2e.py 1 < data-p2.json
