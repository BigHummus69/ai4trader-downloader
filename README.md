# Ai4Trader Downloader
Python script to crawl ai4trader and download both balances and portfolio info. All credit to the boys over at https://ai4trade.ai/ and @HKUDS.

## Setup
Download all the necessary modules, such as Pandas and Playwright, from pip. 

## Easy Way
This is the recommended way to do, but if you're having problems, resort to the Hard Way (just manually setting path).

1. Run folderselector.py, and select your folder. If you selected your folder, and when prompted to type in y or n, and you can't type, just click on the terminal again, it sometimes happens.

2. Run ai4traderscrapperfinal.py and double check that the CSV saved. It's not gonna be in the directory that the program files are running in (unless of course you choose it to be the same directory). Now you got them CSV files!

## Hard Way
This is if you don't trust my coding (respectable) or if the Easy Way ain't cutting it.

1. Don't run folderselector.py, you don't need it.

2. Edit ai4traderscrapperfinal.py, and assign variable `target_dir` the directory you want the files to be stored in. DO NOT INCLUDE QUOTATIONS!!! I've already done it, trust.

