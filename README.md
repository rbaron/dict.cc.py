dict.cc.py
=========

![dict.cc.py usage](http://i.imgur.com/83XCU53.gif)

Simple unofficial command line interface for ![dict.cc](http://dict.cc) written in Python 2. It supports translations between the most common languages available on the website.

Installation
------------

dict.cc.py works with python2 and python3 and is available at pypi. All you have to do to install it is:

```bash
pip install dict.cc.py
```

Usage
-----

It's super easy! Here's a quick example of using it to translate the word `beer` between english (`en`) and swedish (`sv`):

```bash
$ dict.cc.py en sv beer
Showing 3 of 3 result(s)

  English                                                     Swedish
  =======                                                     =======
  beer........................................................öl
  beer glass..................................................ölglas
  wheat beer..................................................veteöl
```

You can also search for phrases by using quotation marks:

```bash
$ dict.cc.py en sv "free beer"
Showing 10 of 50 result(s)

  English                                                     German
  =======                                                     =======
  free beer...................................................Freibier
  alcohol-free beer...........................................alkoholfreies Bier
  free as in beer.............................................frei wie in Freibier
  Beer-Lambert law............................................Lambert-Beer-Gesetz
  free agent..................................................Free Agent
  lead-free labels............................................Bleifrei-Aufkleber
  Free Birds..................................................Free Birds – Esst uns an einem anderen Tag
  beer........................................................Bier
  beer........................................................Gerstenkaltschale
  beer........................................................Gerstenlimonade
  beer........................................................Gerstensaft
```

Available languages include: `en`, `de`, `sv`, `pt`, `it`, `fr`, `ro`.

License
-------

Public domain.
