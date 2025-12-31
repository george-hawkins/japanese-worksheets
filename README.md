Japanese worksheets
===================

Create Japanese worksheet PDFs.

Install
-------

```
$ git clone git@github.com:george-hawkins/japanese-worksheets.git
$ cd japanese-worksheets
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install reportlab requests lxml svglib
```

Run
---

```
(venv) $ python worksheet.py --filename=kanji_practice.pdf --characters='一二三四五六七八九十'
```
