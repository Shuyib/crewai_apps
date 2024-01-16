# https://github.com/mattharrison/sample_nb_code_project/blob/main/Makefile
# .ONESHELL tells make to run each recipe line in a single shell
.ONESHELL:

# .DEFAULT_GOAL tells make which target to run when no target is specified
.DEFAULT_GOAL := all

# Specify python location in virtual environment
# Specify pip location in virtual environment
# Specify the name of the docker container for easy edits.
PYTHON := .venv/bin/python3
PIP := .venv/bin/pip3
DOCKER_CONTAINER_NAME := crewai_app:v0.0.0


venv/bin/activate: requirements.txt #requirements.txt is a requirement, otherwise this command won't run
	# create virtual environment
	python3 -m venv .venv
	# make command executable
	# chmod is a bash command, +x is giving the ADMIN user permission to execute it
	# if it's a+x, that means anyone can run it, even if you aren't an ADMIN
	chmod +x .venv/bin/activate 
	# activate virtual environment
	. .venv/bin/activate

activate:
	# activate virtual environment
	. .venv/bin/activate

install: venv/bin/activate requirements.txt # prerequisite
	# install commands
	# tells pip to install from remote repository which is pip, instead of from the local cached version
	$(PIP) --no-cache-dir install --upgrade pip &&\
		$(PIP) --no-cache-dir install -r requirements.txt

docstring: activate
	# format docstring, might have to change this as well
	# write a template using a numpydoc convention and output it to my python file 
	# so basically just document functions, classes etc. in the numpy style
	pyment -w -o numpydoc *.py

format: activate 
	# format code
	black *.py 

clean:
	# clean directory of cache
	# files like pychache are gen'd after running py files
	# the data speeds up execution of py files in subsequent runs 
	# reduces size of repo 
	# during version control, removing them would avoid conflicts with other dev's cached files
	# add code to remove ipynb checkpoints
	# the &&\ is used to say, after running this successfully, run the next...
	echo @cleaning up your directory
	rm -rf __pycache__ &&\
	rm -rf .pytest_cache &&\
	rm -rf .venv
	rm -rf .ipynb_checkpoints

lint: activate install format
	#flake8 or #pylint
	# In this scenario it'll only tell as errors found in your code
	# R - refactor 
	# C - convention
	echo @linting your code
	pylint --disable=R,C --errors-only *.py 

run: activate install format
	# run test_app
	# run each file separately, bc if one fails, all fail
	@echo @running your code
	streamlit run app.py


docker_build: Dockerfile
	#build container
	sudo docker build -t $(DOCKER_CONTAINER_NAME) .

docker_run_test: Dockerfile
	# linting Dockerfile
	sudo docker run --rm -i hadolint/hadolint < Dockerfile

docker_clean: Dockerfile
	# remove dangling images, containers, volumes, networks 
	sudo docker system prune -a

docker_run: Dockerfile docker_build
	# run docker
	# this is basically a test to see if a docker image is being created successfully
	sudo docker run --rm -it $(DOCKER_CONTAINER_NAME) 

setup_readme:  ## Create a README.md
	@if [ ! -f README.md ]; then \
		echo "# Project Name\n\
Description of the project.\n\n\
## Installation\n\
- Step 1\n\
- Step 2\n\n\
## Usage\n\
Explain how to use the project here.\n\n\
## Contributing\n\
Explain how to contribute to the project.\n\n\
## License\n\
License information." > README.md; \
		echo "README.md created."; \
	else \
		echo "README.md already exists."; \
	fi

docker_push: docker_build
	#deploy
	
# .Phony is used to tell make that these targets are not files
.PHONY: activate format clean lint test build run docker_build docker_run docker_push docker_clean docker_run_test

all: setup_readme install format lint test run docker_build docker_run docker_push
