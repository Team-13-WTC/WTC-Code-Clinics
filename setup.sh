#!/bin/bash
echo alias WTC_CLINIC="$PWD/run.sh" >> ~/.bashrc
source ~/.bashrc
echo alias WTC_CLINIC="$PWD/run.sh" >> ~/.zshrc
exec /bin/zsh
