#!/bin/bash
echo alias wtc-lms-clinic="$PWD/run.sh" >> ~/.bashrc
source ~/.bashrc
echo alias wtc-lms-clinic="$PWD/run.sh" >> ~/.zshrc
exec /bin/zsh
