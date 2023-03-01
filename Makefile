.ONESHELL:
SHELL=/bin/bash

BASE=/opt/SabakuNoBot
VENV_NAME=BotEnv

all:
	$(MAKE) help
help:
	@echo "--------------"
	@echo "		HELP     "
	@echo "--------------"
	@echo "make help"
	@echo "		Display help"
	@echo "make install"
	@echo "		Install everything"
	@echo "make clean"
	@echo "		Delete all the files"
	@echo "--------------"

install:
	@mkdir $(BASE)
	@python3 -m venv $(BASE)/$(VENV_NAME)
	@source $(BASE)/$(VENV_NAME)/bin/activate
	@$(MAKE) requirements
	@$(MAKE) setup
	@echo "Install done"

setup:
	@cp BotReddit.py $(BASE)/$(VENV_NAME)
	@cp Moduli/RedditModule.py $(BASE)/$(VENV_NAME)
	@cp Moduli/YoutubeModule.py $(BASE)/$(VENV_NAME)
	@cp Moduli/TwitchModule.py $(BASE)/$(VENV_NAME)
	@cp streamon.sh $(BASE)/$(VENV_NAME)
	@cp streamoff.sh $(BASE)/$(VENV_NAME)
	@touch /var/log/stream.status.log
	@echo "online" > /var/log/stream.status.log

requirements:
	$(BASE)/$(VENV_NAME)/bin/pip install -r requirements.txt

clean:
	@rm -rf $(BASE)
	if [ -e /var/log/steam.status.log ];then
		@rm /var/log/stream.status.log
	fi
	@echo "Files deleted"

.PHONY: help install clean
