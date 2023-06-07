# TEAM18 Visual Cryptography
👋 We are TEAM18 of NTU Digital Image Processing course
<br/>
## Introduction
🏆 Our term project consists of two parts:
1. Visual Cryptography main program
2. User Interface
## How to run
### Visual Cryptography main program
1. Locate the main program file at [./main-program/VACHVC.py](./main-program/VACHVC.py)
2. Execute the following command in your terminal:
```bash
python VACHVC.py [secret] [file1] [file2]
```
You may find the test file from `./main-program/Sample_210x148` or `./main-program/Sample_297x210`
3. If you would like to stack 2 crypto images into 1, execute the following command:
```bash
python decode.py [X1] [X2] [res]
```
### User Interface
1. Install node 18.12.1 from [https://nodejs.org/en/blog/release/v18.12.1](https://nodejs.org/en/blog/release/v18.12.1)
2. Execute the following command in your terminal:
```bash
cd ./user-interface
npm run start
```
