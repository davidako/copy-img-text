#!/bin/bash

# Inspired by https://ilhicas.com/2018/08/08/bash-script-to-install-packages-multiple-os.html


# Red color for errors.
RED='\033[0;31m'
# Green background color for success messages.
GR_BG="\e[42m%s\e[0m"
# No Color.
NC='\033[0m'

# Contains an associative list of operating systems.
declare -A distros
distros[/etc/debian_version]="debian"
distros[/etc/centos-release]="centos"
distros[/etc/fedora-release]="fedora"
distros[/etc/arch-release]="arch"

# Assume debian-based by default.
os_type='debian'

for f in "${!distros[@]}"; do
  if [[ -f $f ]]; then
    os_type=${distros[$f]}
  fi
done

echo "Operating system: ${os_type}"

# TODO add centos, ferdora and macOS support.


# Dependency packages specific to an OS.
declare -A os_packages
os_packages[debian]="build-essential libcairo2-dev tesseract-ocr tesseract-ocr-all libtesseract-dev libgirepository1.0-dev python3-pip"
os_packages[arch]="base-devel cairo tesseract tesseract-data-eng gobject-introspection-runtime python3-pip"

dependencies="${os_packages[${os_type}]}"

echo "Checking dependencies..."
echo "${dependencies}" | sed 's/\s/\n- /g'
echo

# List of missing dependent packages.
declare -a missing_deps

for dep in ${dependencies}; do
  dpkg-query -W "*$dep*"  &> /dev/null
  if [ $? != 0 ]; then
    missing_deps+=("${dep}")
  fi
done

if [ ${#missing_deps[@]} != 0 ]; then
  printf "${RED}[ERROR]${NC} Missing dependencies. Please install the following packages:\n"
  for package in "${missing_deps[@]}"; do
      echo "- ${package}"
  done
fi

echo "All packages are present."
echo

echo "Installing the app..."
pip3 install .

install_path=$(which cpimgtxt)
if [ $? == 0 ]; then
  printf " ✔ ${GR_BG}\n" "Successfully installed to ${install_path}"
fi
