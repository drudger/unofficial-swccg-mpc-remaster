# unofficial-swccg-mpc-remaster

Resources for automating card creation of SWCCG in GIMP.

## To Use
1. Download Resources.
2. Put the plug-ins into GIMP's plug-ins folder.
3. Open template to use in GIMP.
4. The plug-in should be able to be accessed through a menu at the top "SWCCG" -> "Automate card creation."
5. Choose the card's json data from swccg-card-json-separate-cards folder and the image you wish to use.

You will need to clean up the Lore text and possibly adjust spacing in the Game text. 

### Limitations
Currently, this only works for Characters: Alien, Battle-Droid, Droid, Imperial, Rebel.

### Tested on 
* Windows 10 
  * GIMP 2.10.18 
  * Python 2.7.17

* Ubuntu/Linux 20.04.2 LTS 
  * GIMP 2.10.18 
  * Python 2.7.18

## Credits
* [Templates](https://www.reddit.com/r/starwarsccgalters/comments/n6q9cd/600_dpi_templates_im_proud_of_getting_these/) by [Bardez](https://www.reddit.com/user/Bardez), modified and reorganized layers.
* [Card Data](https://github.com/swccgpc/swccg-card-json) by [SWCCGPC](https://www.starwarsccg.org/), modified to separate individual cards.
* [Jackson Bates](https://www.youtube.com/user/malgalin) for helping me understand the basics of GIMP's Python-Fu.
