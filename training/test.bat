call .\build.bat

rmdir /S "%~dp0..\inference\artifact\"
mkdir "%~dp0..\inference\artifact\"

docker run --rm --gpus all^
 --memory=16g --memory-swap=16g^
 --cap-drop=ALL --security-opt="no-new-privileges"^
 --network none --shm-size=128m --pids-limit 256^
 -v %1:/input/^
 -v %~dp0..\inference\artifact\:/output/^
 stoictrain
