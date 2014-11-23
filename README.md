dict.cc.py
=========

![dict.cc.py usage](http://i.imgur.com/83XCU53.gif)

Simple unofficial command line interface for ![dict.cc](http://dict.cc). It supports translations between the most common languages available on the website.

Installation
------------

dict.cc.py is available at pypi. All you have to do to install it is:

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

Available languages include: `en`, `de`, `sv`, `pt`, `it`, `fr`, `ro`.

License
-------

Public domain.
