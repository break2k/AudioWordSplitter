echo "Creating virtual env"
python3 -m venv .venv

echo "Source it"
source .venv/bin/activate

echo "Install dependencies"
pip install -r requirements.txt

echo "Enjoy!"