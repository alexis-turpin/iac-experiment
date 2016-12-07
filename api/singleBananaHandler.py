import tornado.web
import initialization_handler


class SingleBanana(initialization_handler.InitializationHandler):
    def get(
            self,
            banana_id=None
    ):
        """
        :param INT banana_id: default to None
        :return: write a single banana in JSON format
        """
        if not banana_id:
            self.write(
                {
                    "error": "Missing argument:   id",
                    "errorCode": 400,
                }
            )
        else:
            conn = self.connect_db()
            try:
                with conn.cursor() as cursor:
                    sql = 'SELECT * FROM `bananas` WHERE `id` = %s'
                    qty = cursor.execute(sql, banana_id)
                    query = cursor.fetchone()
                if not qty:
                    raise tornado.web.HTTPError(404)
            except tornado.web.HTTPError:
                self.write(
                    {
                        "error": "This banana doesn't exist",
                        "errorCode": 404
                    }
                )
            except Exception as e:
                self.write(
                    {
                        "error": "Couldn't query Bananas:  " + str(e),
                        "errorCode": 500
                    }
                )
            else:
                self.write(
                    {
                        "id": query[0],
                        "color": query[1],
                        "size": query[2],
                        "price": query[3],
                    }
                )
            finally:
                conn.close()

    def patch(
            self,
            banana_id=None
    ):
        """

        :param banana_id:
        :return:
        """
        # TODO doc
        if not banana_id:
            self.write(
                {
                    "error": "Missing argument:   id",
                    "errorCode": 400,
                }
            )
        else:
            conn = self.connect_db()
            try:
                with conn.cursor() as cursor:
                    sql = 'SELECT * FROM `bananas` WHERE `id` = %s'
                    qty = cursor.execute(sql, banana_id)
                    current = cursor.fetchone()
                if not qty:
                    raise tornado.web.HTTPError(404)
            except tornado.web.HTTPError:
                self.write(
                    {
                        "error": "This banana doesn't exist",
                        "errorCode": 404
                    }
                )
            except Exception as e:
                self.write(
                    {
                        "error": "Couldn't query Bananas:  " + str(e),
                        "errorCode": 500
                    }
                )
            else:
                try:
                    color = self.get_argument("color", current[1])
                    size = self.get_argument("size", current[2])
                    price = self.get_argument("price", current[3])
                    with conn.cursor() as cursor:
                        sql = ('UPDATE `bananas` '
                               'SET `color` = %s, `size` = %s, `price` = %s '
                               'WHERE `id` = %s')
                        cursor.execute(sql, (color, size, price, banana_id))
                except Exception as e:
                    self.write(
                        {
                            "error": "Couldn't UPDATE banana:    " + str(e),
                            "errorCode": 500
                        }
                    )
                else:
                    conn.commit()
                    self.write(
                        {
                            "id": banana_id,
                            "color": color,
                            "size": size,
                            "price": price,
                        }
                    )
            finally:
                conn.close()

    def put(
            self,
            banana_id=None
    ):
        """
        :return:
        """
        # TODO doc
        color = self.get_argument("color", None)
        size = self.get_argument("size", None)
        price = self.get_argument("price", None)
        if not all([banana_id, color, size, price]):
            self.write(
                {
                    "error": "Missing argument: " + ", ".join(
                        [
                            (not bool(banana_id)) * "id",
                            (not bool(color)) * "color",
                            (not bool(size)) * "size",
                            (not bool(price)) * "price",
                        ]
                    ),
                    "errorCode": 400,
                }
            )
        else:
            conn = self.connect_db()
            try:
                with conn.cursor() as cursor:
                    sql = ('UPDATE `bananas` '
                           'SET `color` = %s, `size` = %s, `price` = %s '
                           'WHERE `id` = %s')
                    qty = cursor.execute(sql, (color, size, price, banana_id))
                if not qty:  # Number of line changed == 0
                    raise tornado.web.HTTPError(404)
            except tornado.web.HTTPError:
                self.write(
                    {
                        "error": "This banana doesn't exist",
                        "errorCode": 404
                    }
                )
            except Exception as e:
                self.write(
                    {
                        "error": "Couldn't UPDATE banana:    " + str(e),
                        "errorCode": 500
                    }
                )
            else:
                conn.commit()
                self.write(
                    {
                        "id": banana_id,
                        "color": color,
                        "size": size,
                        "price": price,
                    }
                )
            finally:
                conn.close()

    def delete(
            self,
            banana_id=None
    ):
        if not banana_id:
            self.write(
                {
                    "error": "Missing argument:   id",
                    "errorCode": 400,
                }
            )
        else:
            conn = self.connect_db()
            try:
                with conn.cursor() as cursor:
                    sql = 'DELETE FROM `bananas` WHERE `id`=%s'
                    qty = cursor.execute(sql, banana_id)
                if qty == "0":
                    raise tornado.web.HTTPError(404)
            except tornado.web.HTTPError:
                self.write(
                    {
                        "error": "This banana doesn't exist",
                        "errorCode": 404
                    }
                )
            except Exception as e:
                self.write(
                    {
                        "error": "Couldn't DELETE banana:    " + str(e),
                        "errorCode": 500
                    }
                )
            else:
                conn.commit()
                self.write(
                    {
                        "banana_deleted": qty
                    }
                )
            finally:
                conn.close()
