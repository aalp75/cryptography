## Enigma
Model M3 - German Army WWII


## Contents
I   - M3  
II  - Code   
III - How to run    
IV  - Examples    

## I - M3 machine

The M3 machine is composed of  
- 1 reflector (choose between 2 options)
- 3 rotors selected from 5 available rotors
- 1 plugboard allowing up to 10 letter pair connections

Configuration parameters:

- Plugboard (example): ('AV', 'DE', 'HO', 'JK', 'LS', 'XQ')
- Rotors used and their order (example): ('I', 'VI', 'II')
- Initial rotor positions (example): (25, 6, 4)
- Reflector used (example): 'RefB'

## II - Code

Implemented in Python 3 as a class 

The plugboard, rotors, and reflectors are implemented as lists of integers.
Each list represents a permutation corresponding to the wiring of the component.

For example, plugboard[1] = 5, means that the letter B (index 1) is encoded as F (index 5).  

## III - How to run

Create your Enigma machine
```python
enigma = Enigma()
```
Set up your configuration
  ```python
plug = ['AW', 'HX', 'CO', 'JP', 'EK', 'FR']
rotorpos = ['M', 'R', 'Z']
rotsetup = [5, 2, 3]
refsetup = 1

enigma.setup(plug, rotorpos, rotsetup, refsetup)
``` 
Write the message you want to encrypt in *message_clean.txt*.

  ```python
enigma.encrypt_file('message_clean.txt', 'message_encrypted.txt')
``` 

And when you want to decrypt
  ```python
enigma.encrypt_file('message_encrypted.txt', 'message_decrypted.txt')
``` 

## IV - Examples

**Clean message**:
I WANT TO MEET YOU AT MIDNIGHT TOMORROW

**Encrypted message**:
Y NGUM DS ZSHB BJI SH LCHFXXXD ZDISLPGU

-----------------

**Clean message**:
I REALLY DON T LIKE YOUR NEW FRIEND

**Encrypted message**:
Y SXCWSP YHL B PEMG SGHZ FJU LKMRXI
