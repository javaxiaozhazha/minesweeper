minesweeper README

Run the game(python2.7 Pyramid1.5.7)
------------
>- cd into the project folder
>- mkvirtualenv develop
>- pip install pyramid
>- python setup.py develop
>- pserve development.ini --reload
>- [Warning] make sure all dependencies installed


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

Deploy to heroku
----------------
>**Pre-deploy**
>- pip  freeze > requirements.txt, delete the line include the github url

>- Add Procfile:  echo "web: ./run" > Procfile

>- Add run, chmod +x run
```
#!/bin/bash
set -e
python setup.py develop
python runapp.py
```

>- Add runapp.py
```
import os
from paste.deploy import loadapp
from waitress import serve
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = loadapp('config:production.ini', relative_to='.')
    serve(app, host='0.0.0.0', port=port)
```

>**Deploy:**

>- heroku create --stack cedar or set your own git remote url

>- git push heroku master

>- heroku scale web=1

>**Start, log**

>- heroku open

>- heroku ps

>- heroku logs -t