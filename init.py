from DbConnection import DbConnection

connection = DbConnection()

c = connection.get_connection().cursor()
c.execute('''CREATE TABLE locations
             (user_id real, name text, image text, latitude real,  longtitude real, created_at date)
             '''
          )
connection.get_connection().commit()
connection.get_connection().close()