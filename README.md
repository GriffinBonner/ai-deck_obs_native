# AI-Deck Native Obstacle Detection
![logo](https://github.com/GriffinBonner/ai-deck_obs_native/blob/main/Images/eehpc.png)

## Description

## Hardware Dependencies
| Device | Link |
| ------ | ------ |
| Crazyflie 2.1 | [https://store.bitcraze.io/collections/kits/products/crazyflie-2-1][PlDb] |
| AI-Deck 1.1 | [https://store.bitcraze.io/collections/decks/products/ai-deck-1-1?variant=32485907890263][PlGh] |
| Flow Deck v2 | [https://store.bitcraze.io/collections/decks/products/flow-deck-v2][PlGd] |
| ARM-USB-TINY-H | [https://www.mouser.com/ProductDetail/olimex-ltd/arm-usb-tiny-h/?qs=hO3QYTFrOd1mn8wWiW1byg%3D%3D&countrycode=US&currencycode=USD][PlOd] |
| ARM-JTAG-20-10 | [https://www.mouser.com/ProductDetail/olimex-ltd/arm-jtag-20-10/?qs=DUTFWDROaMbVQp3WoAdijQ%3D%3D&countrycode=US&currencycode=USD][PlMe] |

## Software Dependencies
| Name | Instructions |
| ------ | ------ |
| bitcraze/crazyflie-lib-python | [https://github.com/bitcraze/crazyflie-lib-python/blob/master/docs/installation/install.md][PlDb] |
| anaconda3 | [https://docs.anaconda.com/anaconda/install/linux/][PlDb] |

## Setup

### Ubuntu 18.04 LTS
It is recommended to install Ubuntu 18.04 LTS natively for Crazyflie and AI-Deck development. Bitcraze provides 
virtual machines with the relevant software included however, I have experienced persistent compatability issues 
especially with building AI-Deck firmware. 

### Anaconda
Download the anaconda installer from the link provided above. Follow the installation instructions, first 
install the *Debian* prerequisites if using Ubuntu 18.04 LTS. Setup an environment with python version (3.8) and 
tensorflow version (2.5) to use the current model. If a newer neural network model is to be used, the tensorflow
or python version may need to be updated in the anaconda virtual environment. 

```sh
conda create -n aideck python=3.8 tensorflow=2.5
```
