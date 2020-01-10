# PiAlarmClock

```bash
sudo apt install libsdl2-ttf-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0
```

## Create a virtualenv for `alarmclock`
Installation d'un venv avec python > 3.3

0. Make a `venv` directory:
```bash
mkdir venv
cd venv
```
1. Create a venv named  `alarmclock`:
```bash
python3 -m venv alarmclock --without-pip
```

2. Activate the  `alarmclock` environment
```bash
source ~/venv/alarmclock/bin/activate
```

3. Install `pip`:
```bash
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
rm get-pip.py 
```

4. Restart the virtualenv:
```bash
deactivate
source ~/venv/alarmclock/bin/activate
```

5. Test pip version:
```bash
pip --version
```

## Install requirements

Install `kivy`, `newspaper3k` & `pyowm`:
```bash
pip install kivy
pip install newspaper3k
pip install pyowm
```

### Clone `Meza` GitHub repository:
```bash
mkdir Projects
cd Projects/
git clone https://github.com/jlegrand62/PiAlarmClock.git
```

### Launch the app:
```bash
source ~/venv/alarmclock/bin/activate
python setup.py install
python ~/PiAlarmClock/Projects/main.py
```