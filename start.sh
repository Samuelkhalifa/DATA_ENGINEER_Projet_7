#!/bin/zsh



VAR=$(pwd)



osascript -e "
    tell application \"Terminal\" 
        do script \"cd $VAR/infra && docker compose down -v && docker compose up -d\"
    end tell
    "



sleep 15



osascript -e "
tell application \"Terminal\"
    do script \"cd $VAR && source .venv/bin/activate && python $VAR/infra/kafka/consumer/consumer.py\"
end tell"



sleep 3



osascript -e "
tell application \"Terminal\"
    do script \"cd $VAR && source .venv/bin/activate && python $VAR/infra/kafka/producer/producer.py\"
end tell"
