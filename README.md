# Wedding Audio Book
# ALL CODE TESTED USING PYTHON 3.9

## BOM
### Required
  - Raspberry Pi (tested on 4B but should work on any raspberry pi [note this does use RPI internal Pull Up/Down logic so board must be compatible])
  - Rotary Phone [https://www.amazon.com/dp/B01I4SOFGO?ref=ppx_yo2ov_dt_b_product_details&th=1]
  - Wire Strippers 
  - Jumper Cables
  - Soldering Iron and lead free solder
  - 3.5mm TRS Aux Cables [https://www.amazon.com/dp/B08LMY7H64?psc=1&ref=ppx_yo2ov_dt_b_product_details]
  - 3.5mm Speaker Headpone and Microphone Jack [https://www.amazon.com/dp/B00NMXY2MO?psc=1&ref=ppx_yo2ov_dt_b_product_details]

### Helpful
  - Helping hands for soldering
  - Digital Multimeter with audible continuity 
  - Mini HDMI to HDMI
  
 ## Setup 1-2hr total
 ### AUX SETUP
  1. Cut cables so you have abou 12in of cable then strip the protective black coating
  2. If you did not buy cables listed then it is recommended you test to mark which wires in the aux cord is equivelant to its TRS position
  
Position | Wire Color
--- | --- 
Tip | White 
Ring | Red 
Sleeve | Yellow 

Headset Wiring
Position | Wire Color
--- | --- 
Positive | Tip 
Negative | Ring 

Microphone Wiring
Phone Wire | Aux Wire
--- | --- 
Positive | Tip 
Negative | Sleeve 

### PHONE SETUP
##### Headset Setup
  1. Remove Screws from bottom of phone and remove to from case.
  2. Detatch any cables going from rotatry to circuit board
  3. Look for leads going from handset input port to board. Mark down which color goes where
  4. Cut all cables as close to the board as possible and strip to expose the wire.
    - I recommend placing a heat shrink cable on the wire now out of the to shrink later
  5. Solder the microphone and headset wire according to charts above
  6. Heat shrink tubing over soldered connections
  
##### Lever Setup
This section depends heavily on the lever connector type. There are many different options and thus connecting to the board will be different. I will go over 2 different options I have run across in testing but each case will depend on the phone. 

##### 2 Pin JWST Connector (SIMPLEST)
  1. Connect a M-F jumper from one pin to pin 7 on the board (I chose black -> 7)
  2. Connect a M-F jumper from the other pin to a gnd bin on the board (I chose red -> 6)
  
##### Physcial lever on cicuit board with multiple bars/pins (Requires soldering)
Using a digital multimeter look for continuity between the pins. Look for pins that have continuity when the lever is depressed but not when released. Strip a jumper cable so there is bare cable on one end and a female connector on the other end. Solder the wire to one of the pins and plug to 7. Solder the other and plug to gnd.

### Program Setup (This was done using the GUI but could be done via SSH sesion)
  1. Login to pi and clone this repo
  2. Plug Aux to USB connector to the Raspberry Pi
  3. Cd into cloned repo
  4. Install requirements 
    - > pip3 install -r requirements.txt
  5. Get sound device info
     - > python3 -m sounddevice
     - Device will be listed as Plugable USB Audio Device
  6. Update device number in settings json 
     - #### THIS IS IMPORTATNT OR THE CODE WILL NOT RUN. Unless it just so happens to be the same device number
  7. To test run 
     - python3 weddingAudioBook.py
     - If the phone reciever lever is acting inverted then you must update the settings json pinInfo -> inverted variable
