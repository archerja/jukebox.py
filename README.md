# jukebox.py

This python script will create an html page that plays your local music.

The web page will mimic a classic jukebox look, or can mimic a modern "CD" jukebox style.
You can play the local music using the browser. It will open a new tab, and play an mp3 with the default player application.

Modern and Various styles will look for a "folder.jpg" album cover in the same directory as the mp3.


**Classic Style**

![classic](/images/classic.png)


**Modern/Various Style**

![modern](/images/modern.png)


## Installation

This script requires [mutagen](https://github.com/quodlibet/mutagen) to pull the mp3 tags out of your files.


## Usage example

```
$ ./jukebox.py 
Usage: jukebox.py [PATH] [TYPE] [OPTION]
Try 'jukebox.py --help' for more information.
```

**Simple Help**
```
$ ./jukebox.py --help

./jukebox.py , version  0.0.3

Usage:  ./jukebox.py  [PATH] [TYPE] [OPTION]

                    PATH     [path to your mp3 folder]

                    TYPE     [classic|modern|various]
                                (choose 1 of 3 styles)

                    OPTION   [number of columns]
                                (optional: defaults to 4)
```

**Create web page with classic look**
```
$ ./jukebox.py /media/music/artists/ classic
```

## Release History

* 0.0.3
    * Bugs (spelling mistakes)
* 0.0.2
    * The first proper release
    * Added various artist type
    * Added ability to change number of columns
    * Added simple help
* 0.0.1
    * Work in progress


## Author

Joseph Archer (C) 2018


## License

The code is covered by the MIT.
