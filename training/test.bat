call .\build.bat

rmdir /S "%~dp0..\inference\artifact\"
mkdir "%~dp0..\inference\artifact\"

docker run --rm --gpus all^
 --memory=128g --memory-swap=128g^
 --cap-drop=ALL --security-opt="no-new-privileges"^
 --network none --shm-size=32g --pids-limit 1024^
 -v %1:/input/^
 -v %~dp0..\inference\artifact\:/output/^
 stoictrain
