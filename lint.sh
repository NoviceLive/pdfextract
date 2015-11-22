#!/usr/bin/env bash


#
# Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
#


TARGETS='setup.py run.py ./pdfextract'
pylint $TARGETS
cloc $TARGETS
