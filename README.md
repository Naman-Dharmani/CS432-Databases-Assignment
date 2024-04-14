# CS432-Databases-Assignment
A full stack web application (Svelte + Flask) designed as a buy-and-sell portal, developed as a course project to showcase real-world applications of database management principles


## Installation Guide

1. Clone the repository:
    ```sh
        git clone https://github.com/Naman-Dharmani/CS432-Databases-Assignment.git
    ```

2. Navigate to the project directory: 
    ```sh
        cd CS432-Databases-Assignment
    ```

3. Create a virtual environment and make sure to activate it:
    ```
        python -m venv .venv
        source .venv/bin/activate # Linux
        .\.venv\Scripts\activate  # Windows CMD
        .\.venv\Scripts\Activate.ps1  # Windows PowerShell
    ```

4. Install the server dependencies in virtual environment:
    ```sh
        pip install -r server/requirements.txt
        # pip3 in Linux
    ```

5. Install [Nodejs v18](https://nodejs.org/en/download):


6. Now, open the terminal/MySQL workbench and create a mysql database:
    ```
        CREATE DATABASE buy_sell;
    ```

7. Change the config.yaml file inside _server_ directory:
    ```
        mysql_host: "localhost"
        mysql_user: <mysql_username>
        mysql_password: <user_password>
        mysql_db: "buy_sell"
    ```
    
8. Install the client dependencies:
    ```sh
        cd client
        npm install
    ```

9. Go to the project dir and start the server, and wait until it starts
    ```sh
        cd ..
        python server/run.py
    ```

10. In a new terminal, start the client:
    ```sh 
        cd client
        npm run dev
    ```


11. Now, visit the url shown in the terminal.


__NOTE:__ The frontend is not available for some of the routes. For this we have created a _api_test.rest_ file inside server directory that covers all the methods used in the routes file. Therefore, to test it out install a VSCode extension named [_REST Client_](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) by Huachao Mao. Inorder to test it use the send request option that appears before each of the routes in the api_test.rest file itself.
