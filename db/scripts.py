import sqlite3

# def do(query, *args):
#     conn = sqlite3.connect('test.db')
#     cursor = conn.cursor()
#     data = cursor.execute(query, *args).fetchall()
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return data

class DBWrapper:
    __conn : sqlite3.Connection
    __name : str

    def __init__(self,name : str) -> None:
        self.__name = name

    def get(self,query, *args):
            self.__conn = sqlite3.connect(self.__name)
            cursor = self.__conn.cursor()
            data = cursor.execute(query,*args).fetchall()
            cursor.close()
            self.__conn.close()
            return data