from datetime import datetime

from config.db_config import TABLE_LOCATIONS


class Location:
    def __init__(self):
        self.__user_id = None
        self.__name = None
        self.__photo_url = None
        self.__latitude = None
        self.__longtitude = None
        self.__date = datetime.now()

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_photo_url(self):
        return self.__photo_url

    def set_photo_url(self, photo_url):
        self.__photo_url = photo_url

    def get_latitude(self):
        return self.__latitude

    def set_latitude(self, latitude):
        self.__latitude = latitude

    def get_longtitude(self):
        return self.__longtitude

    def set_longtitude(self, longtitude):
        self.__longtitude = longtitude

    def get_date(self):
        return self.__date

    def get_insert_query(self):
        latitude = self.get_latitude()
        if latitude is None:
            latitude = 0

        longtitude = self.get_longtitude()
        if longtitude is None:
            longtitude = 0
        return "INSERT INTO `{}` VALUES ({}, '{}', '{}', {}, {}, '{}')".format(
            TABLE_LOCATIONS,
            self.get_user_id(),
            self.get_name(),
            self.get_photo_url(),
            latitude,
            longtitude,
            self.get_date().isoformat(' ')
        )

    @staticmethod
    def get_find_by_user_id_query(user_id):
        return "SELECT * FROM {} WHERE `user_id` = {} ORDER BY `created_at` DESC".format(TABLE_LOCATIONS, user_id)

    @staticmethod
    def get_delete_by_user_id_query(user_id):
        return "DELETE FROM {} WHERE `user_id` = {}".format(TABLE_LOCATIONS, user_id)
