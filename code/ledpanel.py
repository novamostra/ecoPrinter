#!/usr/bin/env python
#WS2812B custom effects for ecoPrinter
#author: novamostra.com
from time import sleep
import threading
import board
import neopixel

class WS2812B(object):

    def __init__(self, pin, total_leds):
        self.total_leds = total_leds
        self.pixels = neopixel.NeoPixel(pin, total_leds)        
        self.running = False

    def brightness(self,brightness):
        self.pixels.brightness = brightness

    def fill(self,color):
        self.pixels.fill(color)

    def off(self):
        self.pixels.fill((0,0,0))

    def wheel(self,pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b)      

    def looping_ball(self,color,delay):
        self.delay = delay
        self.color = color
        self.running = True
        self.thread = threading.Thread(target=self.__loop)
        self.thread.start()
        
    def loop(self,color,delay,loops):
        self.off()
        self.delay = delay
        self.color = color
        self.running = True
        for r in range (0,loops):
            for x in range (0,self.total_leds):
                if (self.running):
                    self.pixels[x-3]=((0,0,0))                
                    self.pixels[x-2]=(int(self.color[0]/8),int(self.color[1]/8),int(self.color[2]/8))
                    self.pixels[x-2]=(int(self.color[0]/4),int(self.color[1]/4),int(self.color[2]/4))
                    self.pixels[x-1]=(int(self.color[0]/2),int(self.color[1]/2),int(self.color[2]/2))
                    self.pixels[x]=self.color
                    sleep(self.delay)
                else :
                    break
                self.off()

    def change_color(self,color):
        self.color = color                
            
    def __loop(self):
        while self.running:
            for x in range (0,self.total_leds):
                self.pixels[x-3]=((0,0,0))                
                self.pixels[x-2]=(int(self.color[0]/8),int(self.color[1]/8),int(self.color[2]/8))
                self.pixels[x-2]=(int(self.color[0]/4),int(self.color[1]/4),int(self.color[2]/4))
                self.pixels[x-1]=(int(self.color[0]/2),int(self.color[1]/2),int(self.color[2]/2))
                self.pixels[x]=self.color
                sleep(self.delay)

    def stop(self):
        if(self.running):
            self.running = False
            self.thread.join()
            self.off()
    
    def reset(self):
        self.off()
