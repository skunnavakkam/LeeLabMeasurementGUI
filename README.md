# Measurment Interface for Howard Lee Nano-optics Lab at UCI

We use a Keithley SMU2450 sourcemeter and a Yokagawa AQ6374 spectrometer to look at tunable devices. This software interfaces with those devices. We sweep across voltage ranges. 

## Basic Settings: 
- Min Voltage (for sweep)
- Max Voltage (for sweep)
- Num of Steps
- Current Limit

## Advanced Settings (to be implemented)
- Log sweep (default no)
- Delay between steps (default 100ms)
- Calculate n&k (in progress)

The program will plot readings after it is done. It will also save I/V values. It will generate one file for I/V values, and one file for each spectrometer scan. 

There is **NO** protection whatsoever built in yet. Be careful!!


# Installation

You should have Python and Git installed. First, install required packages

```
pip install pyvisa tqdm pandas
```
Then start the program:

```
git clone https://github.com/skunnavakkam/LeeLabMeasurementGUI.git
cd LeeLabMeasurementGUI
python main.py
```

