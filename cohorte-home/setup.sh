#!/bin/bash

echo "[INFO] COHORTE setup.."
echo "[INFO] exporting the COHORTE_HOME environment variable..."

cd "$(dirname "$0")"

# Export for local shell
export COHORTE_HOME="$(pwd)"
export PATH="$COHORTE_HOME/bin":$PATH

echo "[INFO] COHORTE_HOME=$COHORTE_HOME"
if test -e "$HOME/.bashrc"; then
    echo "[INFO] there is already a .bashrc file in your home folder."
    if grep "COHORTE_HOME" $HOME/.bashrc &> /dev/null; then
        echo "[INFO] COHORTE_HOME environment variable already declared! We will update it"
        echo "`sed  /COHORTE_HOME/d  $HOME/.bashrc`" > $HOME/.bashrc
    else
        echo "[INFO] COHORTE_HOME not declared! We will add it"
    fi
    if grep "COHORTE_PATH" $HOME/.bashrc &> /dev/null; then
        echo "[INFO] COHORTE_PATH already set! But we will update it"
        echo "`sed  /COHORTE_PATH/d  $HOME/.bashrc`" > $HOME/.bashrc
    else
        echo "[INFO] COHORTE_PATH not set! We will set it"
    fi

else
    echo "[INFO] .bashrc doest not exist on your home folder. We will create it"
fi
echo "export COHORTE_HOME=\"$COHORTE_HOME\" #COHORTE_HOME" >> $HOME/.bashrc
tmp='export PATH=$COHORTE_HOME/bin:$PATH'
echo "$tmp #COHORTE_PATH" >> $HOME/.bashrc

# Mac OSX exception
if test -e "$HOME/.bash_profile"; then
    if grep "#COHORTE" $HOME/.bash_profile &> /dev/null; then
        echo
    else
        echo "source $HOME/.bashrc #COHORTE" >> $HOME/.bash_profile        
    fi
fi

# install jpype
bash "$COHORTE_HOME/bin/cohorte-setup"

# source .bashrc
source ~/.bashrc

# Get back where we were
cd -

echo "[INFO] Done."
