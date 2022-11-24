# Art Gallery

## Overview

An online web application that allows user to perform certain operations on the art gallery database.

### Prerequisites

#### softwares

* python
  * Pakages
    * flask_mysqldb

      ```python
      pip install flask_mysqldb
      ```
  
    * flask
      * [Installation](https://flask.palletsprojects.com/en/2.1.x/installation/)

* mysql
  * [Installation](<https://www.apachefriends.org/index.html>)

### Run the app

* Go to the drive of source code. i.e the path that has both src and venv folders

* set up the virtual environment using the command 

  ```cmd
  venv\Scripts\activate
  ```

* set the environment for flask app

    ```powershell
    $env:FLASK_APP = "app"
    ```

* navigate to the src folder

  ```cmd
  cd .\src\

  ```

* Run the app

    ```python
    flask run
    ```
