# Use a cursor to to interact with the database
import pymysql.cursors

# Create a class and object to connect to the database
class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'root',
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        # Establishes a connection to the database
        self.connection = connection
    # Queary the database
    def query_db(self, query, data = None):
        with self.connection.cursor() as cursor:
            try:
                # query = cursor.mogrify(query, data)
                # print("Running Query:", query)

                # executable = cursor.execute(query, data)
                # print("Running Query:", query)

                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong", e)
                return False
            # finally: 
            #     # closes the connection
            #     self.connection.close()
def connectToMySQL(db):
    return MySQLConnection(db)
    
