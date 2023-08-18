@echo off
curl https://www.python.org/ftp/python/3.10.11/python-3.10.11.exe > python-3.10.11-installer.exe
for /f %%A in ('wmic os get osarchitecture ^| find "bit"') do (
    set "architecture=%%A"
)
if "%architecture%"=="32-bit" (
    echo "This is a 32-bit (x86) system."
    curl https://nodejs.org/dist/v18.16.1/node-v18.16.1-x86.msi > nodejs-v18.16.1-installer.msi
    rem Insert your 32-bit specific commands here
) else if "%architecture%"=="64-bit" (
    echo "This is a 64-bit (x64) system."
    curl https://nodejs.org/dist/v18.16.1/node-v18.16.1-x64.msi > nodejs-v18.16.1-installer.msi
    rem Insert your 64-bit specific commands here
) else (
    echo "Unable to determine system architecture."
)
python-3.10.11-installer.exe
del python-3.10.11-installer.exe
nodejs-v18.16.1-installer.msi
del nodejs-v18.16.1-installer.msi
echo "Are you installing or uninstalling dependancies? (I/U)"
choice /c iu /n
if errorlevel 2 (
    pip uninstall requests requests.auth pytz pandas -y
    npm uninstall -g lora-packet -y
) else (
    pip install requests requests.auth pytz pandas
    npm install -g lora-packet
)
cls
echo "Process complete."