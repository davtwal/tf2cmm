# tf2cmm Setup Makefile
# Used to install all required python modules via pip
# If it failes, you can change what python with make all PYTHON=python3

PYTHON=

#windows
ifeq ($(OS),Windows_NT)
	PYTHON+=py
#linux
else
	PYTHON+=python
endif

PACKAGES=cherrypy django

ifneq ($(DONT_INSTALL_OPTIONAL),true)
	PACKAGES+=requests
endif
# INSTALLED PIP MODULES
# Cherrypy	: Web server
# Django		: Framework
# Requests 	: used for testing purposes via python local interpreter
all:
	$(PYTHON) -m pip install $(PACKAGES)

#run:
#	$(PYTHON) server.py