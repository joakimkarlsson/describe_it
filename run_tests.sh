echo 'Running tests...'
./setup.py test
if [[ $? -ne 0 ]]; then
    osascript -e 'display notification "Tests Failed!" with title "FAIL!"'
else
    osascript -e 'display notification "Tests succeeded" with title "SUCCESS!"'
fi
