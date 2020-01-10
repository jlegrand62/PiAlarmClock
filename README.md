# Meza: A Modern Exploration of the Alarm Clock

Meza (derived from 目覚, a hybrid of the Japanese words for "brilliant" and "alarm clock"), is a standalone python-based alarm clock system, which runs natively on Raspberry Pi in conjunction with several APIs. 

## Requirements

Create a conda environment:
```bash
conda create -n alarmclock
conda activate alarmclock
```

Install `kivy`, `newspaper3k` & `pyowm`:
```bash
conda install ipython kivy newspaper3k -c conda-forge
pip install pyowm
```