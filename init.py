from DbConnection import DbConnection
from config.db_config import TABLE_LOCATIONS

connection = DbConnection()

c = connection.get_connection().cursor()
c.execute('''CREATE TABLE {}
             (user_id real, name text, image text, latitude real,  longtitude real, created_at date)
             '''.format(TABLE_LOCATIONS)
          )
connection.get_connection().commit()
connection.get_connection().close()