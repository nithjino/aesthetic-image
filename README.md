# Aesthetic Image Creator

## Requirements
* Python 3
* [wxPython](https://www.wxpython.org/)
* [numpy](http://www.numpy.org/)
* [Pillow](https://pillow.readthedocs.io)
* [jpglitch](https://github.com/Kareeeeem/jpglitch) (I provide it in this repo since I modified it a little bit)

## Instructions
You can load the image through either the File menu or by pressing the button.

You shift the RGB channels by either inputting the shift with the keyboard or by using the +/- button

You can save by either using the `File->Save Image` or `File->Save Image As`. `Save Image` will overwrite the image that you chose to load.
The `Save Image` button acts like `File->Save Image as`.

The Glitch effect will do as it says. It will cause a glitch effect in the image. There are tool tips that will explain what each field does

The Reset Image button will just reload the chosen image from disk

The image preview box is only 600x800. The program will scale the image up or down as far as it can while still keeping the aspect ratio. The saved image will keep the same dimensions as the source image. There can be some delay for bigger images as it has to do pixel by pixel manipulation. I've tested a 2000x2000 image and each shift can take up to 1 second.

## Screenshots
![alt text](https://media.discordapp.net/attachments/224644073795878913/433104295705968640/unknown.png)

![alt text](https://media.discordapp.net/attachments/224644073795878913/433104583506657280/unknown.png)

![alt text](https://media.discordapp.net/attachments/224644073795878913/433104668944629760/unknown.png)

## Bugs
If you shift a channel in one direction for some time, it seems to get stuck in that direction for a little while. By that, I mean if you want to shift the channel in the other direction, you have to shift it more than usual. For example, if I hold down `+` for the red shift on the X axis for some time and then press `-` on the red shift on the X axis, it will continue to shift in the positive direction for a little bit longer and then start shifting in the negative direction. I really need to figure out why.

## Features I want to implement if I find the time to do so
- [ ] Add a scanline effect
- [x] Add a glitching effect
