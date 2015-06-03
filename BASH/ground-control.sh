date="$(date "+%Y%m%d").log"

tmux_running=$(pgrep tmux > /dev/null)

if [ ! "$(pidof tmux)" ] ; then
    echo "Please start tmux first, then run this script again"
    exit 1
fi

if [ ! -f "/usr/bin/ground-control.py" ] ; then
    echo "/usr/bin/ground-control.py is not present! Failing out..."
    exit 1
fi

ground_logs="/home/logs/COMMANDER$date /home/logs/NETMAN$date"
sat_logs="/home/logs/GROUND_COMMANDER$date /home/logs/GROUND_NETMAN$date"

# Create today's files in case they don't exist so next part doesn't fail
touch $ground_logs
touch $sat_logs

tmux neww -n GND 'ground-control.py'
tmux split-window -v -p 50 "tail -f $ground_logs"
tmux split-window -h -p 50 "tail -f $sat_logs"

