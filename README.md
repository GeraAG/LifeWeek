Your life in weeks.

Website to show and your life in weeks and write notes for each week.
The idea is from waitbutwhy.com by Tim Urban.

Project is still in development phase.

![image](https://github.com/GeraAG/LifeWeeks/assets/13507709/74c4143c-b24e-4bb0-bf44-d33646d23cc5)

Required dependencies:

```
pip install flask
pip install psycopg2
```

Also required to have postgreSQL server.

To run:
```
python app.py
```

What has been done:
1. Connection to database
2. Initializing and populating tables
3. Basic front-end
4. Get notes from server and display them in a floating window
5. Write or edit note to save it to the server

TODO:
1. ~~Automatically change current weeks~~
2. ~~Change how to write notes to server. Right now it is possible to do sql injections~~
3. ~~Add authentication and user creation~~
4. ~~Add cookies~~
5. Pretty up front-end
6. ~~Remove edit button, can always change note but save changes when you press button save~~
7. After sign up automatically login
8. Add Home, logout, login, signup
9. Add logs
