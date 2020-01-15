dict.cc.py
=========

![dict.cc.py usage](https://i.imgur.com/83XCU53.gif)

Simple unofficial command line interface for ![dict.cc](https://www.dict.cc) written in Python. It supports translations between the most common languages available on the website.

Installation
------------

dict.cc.py works with Python 2 and Python 3 and is available on PyPi. All you have to do to install it is:

```bash
pip install dict.cc.py
```

Usage
-----

It's super easy! Here's a quick example of using it to translate the word `beer` between english (`en`) and swedish (`sv`):

```bash
$ dict.cc.py en sv beer
Showing 2 of 2 result(s)

English                                                     Swedish
========                                                    =======
beer ...................................................... öl
beer glass ................................................ ölglas
```

You can also search for phrases by using quotation marks:

```bash
% dict.cc.py en de body
Showing 10 of 49 result(s)

Englisch                                                    Deutsch
=========                                                   =======
body ...................................................... Körper-
a'body [Scot.] [allbody] .................................. jedermann
body [also wine] .......................................... Körper [auch bei Wein]
body ...................................................... Leib
body [dead body ] ......................................... Leiche
body ...................................................... Karosserie
body [trunk] .............................................. Rumpf
body [main part] .......................................... Hauptteil
body ...................................................... Gehäuse
body ...................................................... Körperschaft
body [society, organisation for sth.] ..................... Gesellschaft [Organisation]

```

Available languages include: `en`, `de`, `sv`, `pt`, `it`, `fr`, `ro`, `nl`.

Usage as Code
------------

```
>>> from dictcc import Dict
>>> translator = Dict()
>>> result = translator.translate("hello", from_language="en", to_language="de")
>>> result.translation_tuples[:2]
[('Hello !', 'Hallo!'), ('Hello !', 'Servus! [bayer.] [österr.]')]
```

License
-------

Public domain.
