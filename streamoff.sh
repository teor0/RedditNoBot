status_file=/var/log/stream.status.log
status=$(cat $status_file)
if [ $status == "online" ];then
	source /opt/SabakuNoBot/BotEnv/bin/activate
	echo "offline check" | python3 /opt/SabakuNoBot/BotEnv/BotReddit.py
	exit_code=$?
	if [ $exit_code -eq 0 ];then
		echo "offline" > $status_file
		echo "remove post" | python3 /opt/SabakuNoBot/BotEnv/BotReddit.py
		date
	fi
else
	exit 0
fi
