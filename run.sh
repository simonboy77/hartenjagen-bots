# sudo apt install python3-tk

python3 -m venv ./venv
source venv/bin/activate
pip install -r python_packages.txt

python3 collect_brains.py
python3 game/main.py
