+++
date = "2017-02-02"
draft = false
title = """Pantry and Closet Light Automation"""
slug = "pantry-closet-light-automation"
description = ""
keywords = "smartthings,home automation"
tags = ['Home Automation', 'SmartThings']
+++

{{% toc %}} 

One of the most common home automations is lighting. You need it when you need it and you want to conserve when you don't. One of the main scenerios for my home is my pantry and closets. If you need something from them, it is helpful to have light.   

### The Problem

I started with a basic contact switch which works well if you always close the door. I don't know if you house is like mine, but that doesn't always happen. When the door opens, the light turns on, when it closes, the light turns off. You could also add an allowance to turn the light off after it has been on for a certian period of time. But what happens when you come back and the light is off? Open and close the door? Toggle the switch?  

### The Solution

Enter SmartThings multi-sensor. They also have an accelerometer. This means if we mount the base on the door, we can use the doors motion to trigger the light too.  So in the scenerio above, if the light is off and the door is open, a simple or most cases necassary movement of the door will turn the light back on!  

Ok, so now how to put this all together.  We want the light to:

1. Turn on when the door is open
3. Turn on when the door moves
4. Turn off when the door is closed
5. Turn off after n-minutes of inactivity

<img src="/img/AutomatePantryClosetFlow.png" alt="Automated Pantry and Closet Flow" class="boxshadow">

### Hardware

1. [SmartThings](https://www.amazon.com/gp/product/B010NZV0GE/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B010NZV0GE&linkCode=as2&tag=matwalstecand-20&linkId=f418d2a528302c5933143b9dcf651585) (obviously)
2. [SmartThings MultiSensor](https://www.amazon.com/gp/product/B0118RQW3W/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0118RQW3W&linkCode=as2&tag=matwalstecand-20&linkId=f93d0b890c3fe6c55d0206ac8781d58f)
3. Switch or Bulb.  I am using the [Cree Connected](https://www.amazon.com/gp/product/B01701DL7A/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01701DL7A&linkCode=as2&tag=matwalstecand-20&linkId=9367f338ac2e61c8fd29758c1f02c137) bulbs. They work well becuase this solution doesn't require a physical switch and the bulb can be always powered.

### SmartApp

There was no native solution that puts all this together.  So I wrote my own SmartApp.  The key is around handing the cron tasks for the allowance so they reset on activity.  

#### SmartApp configuration

<img src="/img/SmartThingsPantry.png" alt="SmartThings Pantry App" class="boxshadow">

#### SmartApp Code

Here is the code, also available on [GitHub](https://github.com/MrMatt57/SmartThings/blob/master/SmartApps/AutomatedCloset.groovy):

```Groovy
/**
 *  Closet Door
 *
 *  Copyright 2015 Matthew Walker
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 *
 */
definition(
    name: "Automated Closet",
    namespace: "",
    author: "Matthew Walker",
    description: "Automated Closet",
    category: "Convenience",
    iconUrl: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience.png",
    iconX2Url: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience@2x.png",
    iconX3Url: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience@2x.png")

preferences {
  section("When these sensor are activated...") {
    input name: "contactSensor", type: "capability.contactSensor", title: "Contact Sensor", multiple: true
    input name: "knockSensor", type: "capability.accelerationSensor", title: "Movement Sensor", required: false, multiple: true
  }
  
  section("Turn this on...") {
    input "switchDevice", "capability.switch", title: "Switch?", required: false, multiple: true
    input name: "turnOff", type: "bool", title: "Turn off when Closed?"
    input "allowance", "number", title: "Leave on for Minutes? (0 Forever)"
  }
}

def installed() {
  init()
}

def updated() {
  unsubscribe()
  init()
}

def init() {
    if(knockSensor) {
      subscribe(knockSensor, "acceleration.active", doorKnockHandler)
    }
	subscribe(contactSensor, "contact", sensorHandler)
}

def sensorHandler(evt){
  log.debug "$evt.value"
  if(evt.value == "open") {
    turnOnSwitch()
  }
  else if (evt.value == "closed" && turnOff) {
    turnOffSwitch()
  }
}

def doorKnockHandler(evt) {
  if(contactSensor.latestValue("contact") == "closed"){
    return // door is closed
  }
  turnOnSwitch()
}

def turnOnSwitch() {
	switchDevice?.on()
	if(allowance && allowance > 0) {
    	unschedule() // reset timers
		def delay = allowance * 60
		log.debug "Turning off in ${allowance} minutes (${delay}seconds)"
		runIn(delay, turnOffSwitch)
    }
}

def turnOffSwitch() {
	switchDevice?.off()
    unschedule() // reset timers
}
```