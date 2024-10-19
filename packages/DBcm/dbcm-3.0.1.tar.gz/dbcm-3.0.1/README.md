
The DBcm.UseDatabase context manager for working with MySQL/MariaDB and SQLite3.

The 1.x release of this module was based on code created for the second edition 
of Head First Python. See chapters 7, 8, 9, and 11 of the that book for information
on how this module was created.  

To install the second edition release, please use: pip install DBcm=1.7.4

For the third edition of Head First Python, DBcm moved to release 2. The option to use 
SQLite3 is now supported in this new release.  Release 3 of DBcm removes the dependancy
on mysql.connector and replaces it with (the more up-to-date) mariadb library.

Simple example usage (for a MySQL/MariaDB backend):

    from DBcm import UseDatabase, SQLError

    config = { "host": "127.0.0.1",
               "user": "myUserid",
               "password": "myPassword",
               "database": "myDB" }

    with UseDatabase(config) as cursor:
        try:
            _SQL = "select * from log"
            cursor.execute(_SQL)
            data = cursor.fetchall()
        except SQLError as err:
            print("Your query caused an issue:", str(err))

If a filename (string) is used in place of a config dictionary when using 
DBcm.UseDataBase, the data is assumed to reside in a local SQLite file (which
gets created if it doesn't previously exist).
 
