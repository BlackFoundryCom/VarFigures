#!/bin/bash

set -e  # abort on errors
set -x  # echo command

rcjk2ufo figArnaud.rcjk figArnaud.ufo -f FigArnaud -s Regular
fontmake -m figArnaud.designspace -o variable
buildvarc figArnaud.designspace variable_ttf/figArnaud-VF.ttf
