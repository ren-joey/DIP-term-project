有夠破的code僅做為紀錄留存。
執行：
python GenerateRP.py secret.png
python VACHVC_1.py
python VACHVC_2.py
python preprocess.py [file1] [res1]
python preprocess.py [file2] [res2]
python Dither.py [res1] TA1.png [X1]
python Dither.py [res2] TA2.png [X2]
重疊：
python decode.py [X1] [X2] [res]
