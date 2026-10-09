# BerserkFetch

A quick, dirty, and zero-dependency system fetch script for Windows. Think of it as `winfetch` or `neofetch`, but written in pure Python.

I didn't want to deal with `pip install` or external libraries, so this uses **only Python's built-in modules**. 

To be completely honest, this isn't a serious project and the code is pretty messy. I just wrote it to get the job done. Don't expect clean architecture or best practices here.

## What it does
- **Windows Only:** Don't even try running this on Linux or Mac.
- **Zero Dependencies:** No `requirements.txt`, no virtual environments. Just pure Python standard library.
- **Shows basic specs:** Grabs your OS, CPU, RAM, and whatever else I managed to pull from Windows, and prints it to the terminal.

<img width="997" height="417" alt="Ekran görüntüsü 2026-10-09 172408" src="https://github.com/user-attachments/assets/5398e160-bd2e-4751-9a56-9a25732eed71" />

```cmd
python berserkfetch.py
