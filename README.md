# AI-Deck Native Obstacle Detection
![logo](https://github.com/GriffinBonner/ai-deck_obs_native/blob/main/Images/eehpc.png)
**UMBC Energy Efficient High Performance Computing Lab**
**Faculty:** Tinoosh Mohsenin <tinoosh@umbc.edu>
**Authors:** Griffin Bonner <griffi1@umbc.edu>, Haoran Ren <rhaoran1@umbc.edu>


## Description

## Hardware Dependencies
| Device | Link |
| ------ | ------ |
| **Crazyflie 2.1** | https://store.bitcraze.io/collections/kits/products/crazyflie-2-1 |
| **AI-Deck 1.1** | https://store.bitcraze.io/collections/decks/products/ai-deck-1-1?variant=32485907890263 |
| **Flow Deck v2** | https://store.bitcraze.io/collections/decks/products/flow-deck-v2 |
| **ARM-USB-TINY-H** | https://www.mouser.com/ProductDetail/olimex-ltd/arm-usb-tiny-h/?qs=hO3QYTFrOd1mn8wWiW1byg%3D%3D&countrycode=US&currencycode=USD |
| **ARM-JTAG-20-10** | https://www.mouser.com/ProductDetail/olimex-ltd/arm-jtag-20-10/?qs=DUTFWDROaMbVQp3WoAdijQ%3D%3D&countrycode=US&currencycode=USD |

## Software Dependencies
| Name | Instructions |
| ------ | ------ |
| **bitcraze/crazyflie-lib-python** | https://github.com/bitcraze/crazyflie-lib-python/blob/master/docs/installation/install.md |
| **bitcraze/AIdeck_examples** | https://github.com/bitcraze/AIdeck_examples.git |
| **docker instructions** | https://github.com/bitcraze/AIdeck_examples/blob/master/docs/getting-started/docker-gap8.md |
| **streaming example** | https://github.com/bitcraze/AIdeck_examples/tree/master/GAP8/test_functionalities/wifi_jpeg_streamer |
| **anaconda3** | https://docs.anaconda.com/anaconda/install/linux/ |
| **pygobject** | https://anaconda.org/conda-forge/pygobject |

## Setup

### Ubuntu 18.04 LTS
It is recommended to install Ubuntu 18.04 LTS natively for Crazyflie and AI-Deck development. Bitcraze provides 
virtual machines with the relevant software included however, I have experienced persistent compatability issues 
especially with building AI-Deck firmware. 

### Anaconda
Download the anaconda installer from the link provided above. Follow the installation instructions, first 
install the *Debian* prerequisites if using Ubuntu 18.04 LTS. Create an environment with python version (3.8) and 
tensorflow version (2.5) with the following commands. If a newer neural network model is to be used, 
the tensorflow or python version may need to be updated in the anaconda virtual environment. 
```sh
conda create -n aideck python=3.8 tensorflow=2.5
conda install -c conda-forge pygobject
```
Each time you wish to work on the project or run the demo, you will need to run the following command in the 
terminal to activate the anaconda virtual environment. If you do not activate the environment, the model will 
use the (base) environment which will not have the required versions of python and tensorflow. 
```sh
conda activate aideck
```

### Crazyflie Python Library
The demo program uses the crazyflie python library to control the crazyflie drone. Install the repository by
cloning the github link and follow the steps in the link given above. Note: you do not need to create a new 
virtual environment as you will be using the anaconda virtual environment that you just created, so add the 
dependencies to the anaconda environment. 

### AI-Deck Image Streaming
The AI-Deck is an expansion deck for the crazyflie drone. It includes a camera and application processor
suited for running neural network operations efficiently. This demo does not run the neural network 
onboard the ai-deck. The demo relies on the ai-deck example titled: **wifi_jpeg_streamer**. The ai-deck
ships with this example pre-flashed, but if for some reason it is corrupted you will need to flash it. 
The instructions given above in the link **docker instructions** demonstrate how to set up docker to
flash the **GAP8** chip that is on the ai-deck. It is much easier to use docker instead of installing the 
**GAP8 SDK** natively. Once you have setup docker and installed the ai-deck onto the crazyflie, power the 
crazyflie on *without* the debugger attached. Plug in the debugger to the host pc and the ai-deck. 
Navigate to the directory: 

    /AIdeck_examples/GAP8/test_functionalities/wifi_jpeg_streamer
    
Run the following command to save the streaming example to the ai-deck flash memory: 

    docker run --rm -it -v $PWD:/module/data/ --device /dev/ttyUSB0 --privileged -P bitcraze/aideck /bin/bash -c 'export GAPY_OPENOCD_CABLE=interface/ftdi/olimex-arm-usb-tiny-h.cfg; source /gap_sdk/configs/ai_deck.sh; cd /module/data/;  make clean all image flash'

### Running the Demo
To run the demo you will need the **Crazyflie** with **ai-deck** installed and the **wifi_jpeg_streamer** 
example flashed, the **Crazyradio PA** plugged into the linux pc, the **anaconda** virtual environment, and 
this repository cloned. 

**1.** Turn on the Crazyflie and connect to the wifi access point **Bitcraze AI-deck Example**
**2.** Open two terminals and run the following commands in both terminals to activate anaconda:

    conda activage aideck
**3.** Navigate to this repository in both terminals:
    
    cd ~/ai-deck_obs_native
    
**4.** Run the following commands each in separate terminals:
**Terminal 1** (start the autonomous control)

    python control.py
**Terminal 2** (start streaming and neural-network)

    python stream.py