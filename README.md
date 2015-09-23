minesweeper README

Set up Pyramid project
----------------------

>- mkvirtualenv minesweeper

>- pip install pyramid

>- pcreate -s starter minesweeper

>- Run following commands for test and development
```
python setup.py test -q to test
python setup.py develop
```
>- pserve development.ini --reload


Add Bootstrap Angular support
-----------------------------
>- Add bootstrap support
```
     <app>/static/css
     <app>/static/font
     <app>/static/js
```
>- Add angular.js
```
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.0.7/angular.min.js"></script>
```