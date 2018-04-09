# Aesthetic Image Creator
Main repo here: https://gitlab.com/bunu/aesthetic-image

This repo is just a copy of my gitlab repo. There is no guarantee that this repo will be up-to-date

Check out my gitlab if you want that.

## Requirements
* Python 3
* [wxPython](https://www.wxpython.org/)
* [numpy](http://www.numpy.org/)
* [Pillow](https://pillow.readthedocs.io)

## Instructions
You can load the image through either the File menu or by pressing the button.

You shift the RGB channels by either inputting the shift with the keyboard or by using the +/- button

You can save by either using the `File->Save Image` or `File->Save Image As`. `Save Image` will overwrite the image that you chose to load.
The `Save Image` button acts like `File->Save Image as`.

The Reset Image button will just reload the chosen image from disk

The image preview box is only 600x800. The program will scale the image up or down as far as it can while still keeping the aspect ratio. The saved image will keep the same dimensions as the source image. There can be some delay for bigger images as it has to do pixel by pixel manipulation. I've tested a 2000x2000 image and each shift can take up to 1 second.

## Screenshots
![alt text](https://media.discordapp.net/attachments/224644073795878913/432738576392912897/unknown.png)

![alt text](https://media.discordapp.net/attachments/224644073795878913/432738821629804564/unknown.png)

## Bugs
If you shift a channel in one direction for some time, it seems to get stuck in that direction for a little while. By that, I mean if you want to shift the channel in the other direction, you have to shift it more than usual. For example, if I hold down `+` for the red shift on the X axis for some time and then press `-` on the red shift on the X axis, it will continue to shift in the positive direction for a little bit longer and then start shifting in the negative direction. I really need to figure out why.

## Features I want to implement if I find the time to do so
- [ ] Add a scanline effect
- [ ] Add a glitching effect
