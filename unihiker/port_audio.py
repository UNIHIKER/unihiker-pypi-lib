import os

os.system("brew install portaudio")
os.system("brew link portaudio")
os.system("cp .pydistutils.cfg $HOME/")
# os.system("MY_FILE=$1")
# os.system("MY_PATH=$2")
# os.system("MY_FILE=$3")
# os.system('touch $HOME/.pydistutils.cfg')
# os.system('echo [build_ext] > "$MY_FILE"')
# os.system('echo include_dirs=/opt/homebrew/Cellar/portaudio/19.7.0/include/ > "$MY_FILE"')
# os.system('echo library_dirs=/opt/homebrew/Cellar/portaudio/19.7.0/lib/ > "$MY_FILE"')