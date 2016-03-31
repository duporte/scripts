#!/bin/bash
# helice em ASCII
# 

# torna o cursor invisivel
tput civis

while true
do
   for i in / - \\ \|
   do
      sleep .1
      echo -ne "\e[1D$i"
   done
done
# restaura o cursor
tput cnorm
