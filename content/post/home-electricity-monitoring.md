+++
title = "Home Electricity Monitoring with EmonPi"
date = "2018-07-28T08:46:44+01:00"
description = "Rebooting home electricity monitoring with EmonPi"
tags = [
  "electricity, energy, home, monitoring, raspberry pi, emonpi"
]
+++

After a long hiatus I've rebooted the home electricity monitoring system: an [EmonTx](https://wiki.openenergymonitor.org/index.php/EmonTx_V3.4) unit with a sensor round the live cable out of our main electricity meter, sending data to a raspberry pi hat on a pi running [EmonCMS](https://wiki.openenergymonitor.org/index.php/EmonPi).

This gives a data reading every 10 seconds (in theory - mine is dropping some at present), so you can get a lovely dashboard like this:

{{< figure src="/img/Emonpi 2018-07-28.png" title="The EmonCMS home electricity use dashboard" >}}


