import sqlite3

def do(query, *args):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(query, *args)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

class DBWrapper:
    __conn : sqlite3.Connection
    __name : str

    def __init__(self,name : str) -> None:
        self.__name = name
    def connect(self) -> None:
        self.__conn = sqlite3.connect(self.__name)

    def get(self,query, *args):
        cursor = self.__conn.cursor()
        data = cursor.execute(query,*args).fetchall()
        cursor.close()
        return data
        
    def disconnect(self) -> None:
        self.__conn.close()

    


if __name__ == '__main__':
    print(do('''SELECT * FROM intellect'''))