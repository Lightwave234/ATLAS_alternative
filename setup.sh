#! /bin/bash
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 [-i|-u]"
    echo "  -i: Install"
    echo "  -u: Uninstall"
    exit 1
fi
set -e
while [ "$#" -gt 0 ]; do
    case "$1" in
        -i)
            apt install python3.10 pip nodejs npm -y
            npm install -g lora-packet
            pip install requests requests.auth pytz pandas
            break
            ;;
        -u)
            pip uninstall -y requests requests.auth pytz pandas
            npm uninstall -g lora-packet
            apt remove python3.10 pip nodejs npm -y
            break
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [-i|-u]"
            echo "  -i: Install"
            echo "  -u: Uninstall"
            exit 1
            break
            ;;
    esac
done