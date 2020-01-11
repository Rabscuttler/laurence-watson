+++
date = "2016-03-30"
title = "Small steps to an autonomous future"

+++

**Summary:** Every morning my lights turn themselves on, along with my amplifier which begins playing a random song off my wake up playlist. 

My current setup is a [Raspberry Pi B+](https://www.raspberrypi.org/products/model-b-plus/) with a [HiFiBerry DAC+](https://www.hifiberry.com/dacplus/). The pi runs [Home Assistant ](https://home-assistant.io) for home automation (lights, plugs, scripts), with [Mopidy](https://www.mopidy.com/) and [Mopify](https://github.com/dirkgroenen/mopidy-mopify) providing the music and user interface.

My home assistant dashboard looks like this:

{{< figure src="/img/home_assistant.PNG" title="Blackstock Home Assistant" >}}

While the pi looks like this:

{{< figure src="/img/pi.jpg" title="Raspberry pi and rf chips" >}}

This is actually my older pi model C from 2011, without the HiFiBerry DAC attached. The breadboard and chips are used to communicate with the remote control RF plug sockets. [This tutorial by Tim Leland](https://timleland.com/wireless-power-outlets/) provides the starting point. [WiringPi](http://wiringpi.com/) and [pinout](http://pinout.xyz/pinout/ground) are useful to get the right pinouts.

I bought 5 pairs of 433Mhz RF Transmitter module + receivers for £4.50 from amazon, the breadboard and cables were a pound each, and 10 remote control plug sockets from ebay for £35.

After connecting up the RF module and installing Tim's `RFSniffer` [module](https://github.com/timleland/rfoutlet), by using the remote control for the plugs we can sniff the 433Mhz codes it is sending to each plug and note them down. 

Once we've got the codes for each plug, we then use the `codesend` module from Tim's code to send out each individual on/off trigger.

You can see the codes as [home assistant command switches](https://home-assistant.io/components/switch.command_line/) in my home assistant [configuration file](https://gist.github.com/Rabscuttler/b4d7ecf0add7508fcb15278ff5080d52):

`oncmd: "/var/www/rfoutlet/codesend 29955`
`offcmd: "/var/www/rfoutlet/codesend 29964`

Controlling the music from home assistant is done in a rather inelegant way. [Mopidy](https://www.mopidy.com/) has an api - the many [front ends](http://mopidy.readthedocs.org/en/latest/ext/web/#ext-web) communicate with it usually using the javascript api. However, you can also post to it with JSON - the API details are [here](http://mopidy.readthedocs.org/en/latest/api/http/).

So, my morning music script can be seen in this [gist](https://gist.github.com/Rabscuttler/32b189b8fa58398a012b6652dba17fde). After the Home Assistant automation script turns on the uplighter, fairy lights and amplifier, what it is doing is:

1. Clearing the mopidy tracklist
2. Adding playlist using the Spotify identifier - to find, right click on a song or playlist and select 'copy Spotify URI'*
3. Set to random
4. Begin playing

# The future

I'd like to implement more scenes and automation rules, as well as setting up [Owntracks](http://owntracks.org/) for location tracking. At present we see if people's phones are connected to the network to check if they are home, which is not that effective a solution.