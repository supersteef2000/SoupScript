@echo off
set arg1=%1
set arg2=%2
shift
shift
if [%arg1%] == [] set arg1=source.soup
if [%arg2%] == [] set arg2=a.exe
python compile.py %arg1%
clang out.c -o %arg2%
del out.c
echo Compiling completed.