#!/bin/bash


# help message
display_help()
{
    echo
    echo -e '\033[1mSYNTAX\033[0m'
    echo "------"
    echo
    echo -e "\033[1mbash setup.sh\033[0m [\033[1m-h\033[0m] [\033[1m-e\033[0m \033[4mpath_to_dir\033[0m]"
    echo
    echo -e '\033[1mOPTIONS\033[0m'
    echo "-------"
    echo
    echo -e "\033[1m-h\033[0m                        help message"
    echo
    echo -e "\033[1m-e\033[0m \033[4mpath_to_dir\033[0m            directory for virtual environment (default home)"
    echo
}

VDIR=$HOME

# get options
while getopts "he:" option; do
    case $option in
        # display help message
        h)  display_help
            exit 0;;
        # directory for virtual environment
        e)  VDIR=$OPTARG
            if [[ -d $VDIR ]]; then
                echo "Virtual environment will be created in $INPUT_DIR"
            else
                echo "ERROR: please enter a valid directory"
                exit 2
            fi;;
        # exit on invalid options
        \?) echo "ERROR: invalid option usage"
            display_help
            exit 1;;
    esac
done


python3 -m venv ${VDIR}/.venv

source ${VDIR}/.venv/bin/activate

pip3 install --upgrade pip

pip3 install -r data/requirements.txt

deactivate

echo
echo "setup complete"
echo