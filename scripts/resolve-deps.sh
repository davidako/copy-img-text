#!/bin/bash

### Cross-distro package manager script ###

# Inspired by https://ilhicas.com/2018/08/08/bash-script-to-install-packages-multiple-os.html

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

for dep in ${dependencies}; do
  dpkg-query -W "*$dep*"  &> /dev/null
  if [ $? != 0 ]; then
    echo "Missing dependency package. Please install the following package: ${dep}"
    exit 1
  fi
done

echo "All packages are present."
echo

echo "Installing the app..."
pip3 install .

