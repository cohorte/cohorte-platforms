#!/bin/bash

echo "[INFO] COHORTE sutup.."
echo "[INFO] exporting the COHORTE_HOME environment variable..."

# Keep the current working directory
old_pwd="$(pwd)"

# Compute the path to this file
cd "$(dirname $0)"
export COHORTE_HOME="$(pwd)"

if test -e "$HOME/.bashrc"; then
    echo "[INFO] there is already a .bashrc file in your home folder."
    if grep "COHORTE_HOME" $HOME/.bashrc &> /dev/null; then
        echo "[INFO] COHORTE_HOME environment variable already declared! We will update it"
        echo "`sed  /COHORTE_HOME/d  $HOME/.bashrc`" > $HOME/.bashrc
    else
        echo "[INFO] COHORTE_HOME not declared! We will add it"
    fi
else
    echo "[INFO] .bashrc doest not exist on your home folder. We will create it"

fi
echo "export COHORTE_HOME='$COHORTE_HOME'" >> $HOME/.bashrc
source $HOME/.bashrc
echo "[INFO] Done."