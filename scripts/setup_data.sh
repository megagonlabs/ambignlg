set -ex
mkdir -p ./data/raw

wget https://github.com/allenai/natural-instructions/archive/refs/tags/v2.8.tar.gz
tar -xvzf v2.8.tar.gz && rm v2.8.tar.gz
mv natural-instructions-2.8/tasks ./data/raw
rm -rf natural-instructions-2.8
