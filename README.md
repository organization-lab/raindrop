# raindrop

An open-source macOS menu bar timer for human-being.

## How to use

1. you should have python 3 installed (tested with Python 3.7 and macOS 10.15.5)
2. install `rumps` (`$pip install rumps`)
3. clone or download `raindrop.py`
4. `$python raindrop.py`
5. find the app icon in your menu bar (top right of your screen) and choose time for your `raindrop`
6. click `Start Timer`. a window should pop up for inputting `What will this raindrop for?`, then click `OK` (or press Enter)
7. you should see a counting down number in menu bar
8. when the raindrop finished, another window should pop up for your feedback
    - how many percent time you actually used for your purpose (feel free to wondering some time in your raindrop, that's human-being)
    - a general feedback with 1-5 stars (click will also close the window)
9. all logs is stored at `test.log` in your `raindrop` folder. you may also like to store rumps debug output to a file by redirecting stdout

## Features (some are not implemented yet)

- [x] simple digital countdown timer with notification at your macOS menu bar.
- [x] attach notes of projects to each timer
- [x] attach feedback after timer runs out
    - [x] a general feedback with 1-5 stars
    - [x] how many percent time you actually used
    - [ ] how is your efficiency
- [ ] some random quotes of principles to enhance experience and get more concentrated
- [ ] report analyzer for long-term monitoring and feedback analysis of your `raindrops`

## Miscellaneous

### Why this App called `raindrop`?

- raindrop is a metaphor of everyday time. The model is to collect time as raindrops - raindrops will finally form a river, moving unstoppable to its destination - the ocean.

### Why there is some quotes?

We believe that proper recall of quotes may help people live happier and more meaningful (that's `for human-being` means).

### Minor points

- license: MIT (i.e. feel free to reuse and make your own version)
- raindrop is inspired partly by [Timebox](https://github.com/visini/timebox).
- for principles, Ray Dalio's [Principles](https://principles.com/) is highly recommended by us.

---

(c) Trevize Inc. Organization laboratory. 2020
