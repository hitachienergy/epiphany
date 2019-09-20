#!/bin/bash

yum-config-manager --disable epirepo*;
yum makecache;
yum repolist;

