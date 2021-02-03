deps_pi:
	pip3 install -r requirements.txt

deps_mac:
	pip3 install -r requirements-mac.txt

pip_add:
	pip3 install $(i) && pip freeze | grep $(i) >> requirements.txt

pip_mac_add:
	pip3 install $(i) && pip freeze | grep $(i) >> requirements-mac.txt

pip_install_linux:
	sh resources/setup/pip_install.sh linux

pip_install_mac:
	sh resources/setup/pip_install.sh mac