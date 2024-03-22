# Testing RX and TX

To verify you can get 2 radios talking to each other, at least one of which needs to be a HackRF, you should be able to do the following:

1.  Plug in both radios via USB and attach antennas
2.  Start the rxdemo.py
3.  Transmit a tone via hackrf_transfer


Let's assume we have 2 HackRF radios on different machines.  On the RX machine run:

```
python3 rxdemo.py HackRF 2e6 230e6
```


On the TX machine, run

```
hackrf_transfer -f 229600000 -s 1000000 -p 1 -a 1 -c 100 -x 20
```

The trick appears to be getting the power high enough so the receiver can "see" the signal.  
