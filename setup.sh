#!/bin/bash

# dependency transfer
sudo mkdir -p /usr/local/lib
sudo mkdir -p /usr/local/lib/leeroy

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

rm -rf .git .gitignore
sudo mv * /usr/local/lib/leeroy/

# creating an executable file
sudo cat <<EOF | sudo tee /usr/local/bin/leeroy >/dev/null
#!/bin/bash
/usr/local/lib/leeroy/venv/bin/python /usr/local/lib/leeroy/main.py "\$@"
EOF

sudo chmod +x /usr/local/bin/leeroy