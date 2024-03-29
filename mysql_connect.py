from mysql.connector import MySQLConnection, Error
from collections import OrderedDict
from config import read_db_config


class MysqlPython(object):
    """
        Python Class for connecting  with MySQL server and accelerate development project using MySQL
        Extremely easy to learn and use, friendly construction.
    """

    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None
    __cursor = None
    __connection = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance or not cls.__database:
            cls.__instance = super(MysqlPython, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    # End def __new__

    # def __init__():

    def __open(self):
        try:
            db_config = read_db_config()
            cnx = MySQLConnection(**db_config)
            self.__connection = cnx
            self.__cursor = cnx.cursor()
        except Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

    # End def __open

    def __close(self):
        self.__cursor.close()
        self.__connection.close()

    # End def __close

    def get_connection(self):
        try:
            db_config = read_db_config()
            self.__connection = MySQLConnection(**db_config)
        except Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
        return  self.__connection

    def select(self, table, where=None, *args, **kwargs):

        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","
        # End for keys

        query += ' FROM %s' % table

        if where:
            query += " WHERE %s" % where
        # End if where

        self.__open()

        self.__cursor.execute(query, values)
        items = self.__cursor.fetchall()

        self.__close()

        return items

    # End def select

    def update(self, table, where=None, *args, **kwargs):
        query = "UPDATE %s SET " % table
        keys = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "` = %s"
            if i < l:
                query += ","
            # End if i less than 1
        # End for keys
        query += " WHERE %s" % where

        self.__open()
        self.__cursor.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        update_rows = self.__cursor.rowcount
        self.__close()

        return update_rows

    # End function update

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(
                ["%s"] * len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"] * len(values)) + ")"

        self.__open()
        self.__cursor.execute(query, values)
        self.__connection.commit()
        self.__close()
        return self.__cursor.lastrowid

    # End def insert

    def delete(self, table, where=None, *args):
        query = "DELETE FROM %s" % table
        if where:
            query += ' WHERE %s' % where

        values = tuple(args)

        self.__open()
        self.__cursor.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        delete_rows = self.__cursor.rowcount
        self.__close()

        return delete_rows

    # End def delete

    def select_advanced(self, sql, *args):
        od = OrderedDict(args)
        query = sql
        values = tuple(od.values())
        self.__open()
        self.__cursor.execute(query, values)
        items = self.__cursor.fetchall()
        number_rows = self.__cursor.rowcount
        number_columns = len(self.__cursor.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in items]
        else:
            result = [item[0] for item in items]

        self.__close()
        return result

    # End def select_advanced


# End class

