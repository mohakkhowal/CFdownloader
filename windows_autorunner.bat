:start
cls
echo ********** Installing Dependancies **********
set INPUT= "dependency.txt"
echo INPUT
py -m pip install -r %INPUT%
python script.py
pause