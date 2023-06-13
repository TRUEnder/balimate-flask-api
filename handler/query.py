import mysql.connector
from models.connection import pool


def query(queryStat):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()

        cursor.execute(queryStat)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        response = {
            "code": "success",
            "data": results
        }
        return response

    except mysql.connector.Error as err:

        response = {
            "code": "error",
            "error": {
                "code": str(err)
            }
        }
        return response


def queryWithColumnNames(queryStat):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()

        cursor.execute(queryStat)
        column_names = cursor.column_names
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        response = {
            "code": "success",
            "data": {
                "column_names": column_names,
                "records": results
            }
        }
        return response

    except mysql.connector.Error as err:

        response = {
            "code": "error",
            "error": {
                "code": str(err)
            }
        }
        return response
