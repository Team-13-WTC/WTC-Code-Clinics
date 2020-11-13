#!/bin/bash
echo alias WTC_CLINIC="$PWD/run.sh" >> ~/.bashrc
echo alias WTC_CLINIC="$PWD/run.sh" >> ~/.zshrc
source ~/.bashrc
exec /bin/zsh