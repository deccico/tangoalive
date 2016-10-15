if pidof -s run.sh > /dev/null; then
    echo 'It is already running!'
else
    echo 'process not found...'
    /home/adrian/run.sh
fi
