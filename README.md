# ecoPrinter
ecoPrinter is an innovative device which can replace hard copies with **no interaction** file transferring, by implementing Android Beam and USB Printer Gadget functionality on a Raspberry PI Zero W.

Forget searching for Bluetooth devices or Wifi networks, enabling visibility, establishing a connection/pairing or setting up Wifi Direct, everything has become automated using (the unfortunately now deprecated) Android Beam. You just place your mobile device on the ecoPrinter while this is searching for a device (Red indication Light) and a few seconds later you can view the file on your mobile device as PDF. No matter if it is an image, document or a web-page, full backward compatibility is guaranteed because ecoPrinter appears as any other Printing device  on your computer.

The main idea for this device is to reduce the amount of paper we use and also help users organize and keep their receipts, invoices, documents with the minimum amount of effort.
<!--more-->
## How it works
1. The provider (owner of the device) connects the ecoPrinter and correlates the appropriate driver.
2. The provider of the ecoPrinter functionality simply selects the document to be printed and selects ecoPrinter as the preferable printer device.
3. The file is then send to the Raspberry Pi and is converted to PDF.
4. The WS2812B indicates to the user that it's time to place the mobile device to the ecoPrinter
5. With no other interaction the file is transferred to the mobile device as a PDF.

## Schematic
![ecoPrinter schematic](https://novamostra.com/wp-content/uploads/2020/02/ecoPrinterSchematic.png)

## Configuration/Setup
1. Clone the repository
2. Set execute permission to setup.sh
```bash
sudo chmod +x setup.sh
```
3. Run as sudo
```bash
sudo ./setup.sh
```
4. On your Windows computer setup the appropriate printer driver running the following command:
```
printui /if /b "ecoPrinter" /f %windir%\inf\ntprint.inf /m "Microsoft PS Class Driver" /r "USB001"
```
5. Your ecoPrinter is Ready!

The complete step by step guide on how to create your own ecoPrinter is available on [instructables](https://www.instructables.com/id/EcoPrinter/).

## 3d files are also available at Thingverse
[Download from Thingverse](https://www.thingiverse.com/thing:4164764)

[Find out more](https://novamostra.com/2020/02/15/ecoprinter/)
