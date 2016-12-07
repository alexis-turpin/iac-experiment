import tornado.web
import initialization_handler


class SingleBanana(initialization_handler.InitializationHandler):
    """Single Banana handler

    Implement the GET/PATCH/PUT/DELETE methods for a single banana
    """
    def get(
            self,
            banana_id=None
    ):
        """Get a single banana

        Get a single banana identified by the mandatory banana_id param
        Handle common errors such as banana_id arg missing, not
        existing or DB errors.

        Args:
            INT banana_id: mandatory to identify which banana to return

        Returns:
            A dict describing all data (id, color, size, price) related
            to the chosen banana.
            Example (banana_id = 1):
                {
                    "id": 1,
                    "color": "yellow",
                    "size": 10.5,
                    "price": 4.99,
                }

            if banana_id arg is missing, doesn't exist in the DB, or
            there is an issue to query it from the DB, it will return a
            dict describing an error instead.
            Example (doesn't exist in the DB):
                {
                    "error": "This banana doesn't exist",
                    "errorCode": 404
                }
        """
        if not banana_id:  # Should I just return an empty dict in that case ?
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
        """Patch a single banana

        Get a single banana identified by the mandatory banana_id param
        Then update this banana's color, size AND/OR price according to
        the related args. Then returns the updated banana.
        Handle common errors such as banana_id arg missing, not
        existing or DB errors.

        Args:
            INT banana_id: mandatory to identify which banana to update
            STR color: optional new chosen color
            FLOAT size: optional new chosen size
            FLOAT price: optional new chosen price

        Returns:
            A dict describing all data (id, color, size, price) related
            to the updated banana.
            Example (banana_id = 1, price = 1.49):
                {
                    "id": 1,
                    "color": "yellow",
                    "size": 10.5,
                    "price": 1.49,
                }

            if banana_id arg is missing, doesn't exist in the DB, or
            there is an issue to query it from the DB, it will return a
            dict describing an error instead.
            Example (missing banana_id arg):
                {
                    "error": "Missing argument:   id",
                    "errorCode": 400,
                }
        """
        # TODO: Must find a better way to patch than SELECT then UPDATE
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
        """Put a single banana

        Update color, size AND price of a banana chosen by the
        mandatory banana_id arg. All args are mandatory.
        Then returns the updated banana
        Handle common errors such as args missing, banana not existing
        or DB errors.

        Args:
            INT banana_id: mandatory to identify which banana to update
            STR color: mandatory new chosen color
            FLOAT size: mandatory new chosen size
            FLOAT price: mandatory new chosen price

        Returns:
            A dict describing all data (id, color, size, price) related
            to the updated banana.
            Example (banana_id = 1, color = "green", size = 8.2,
                price = 4.99):
                {
                    "id": 1,
                    "color": "green",
                    "size": 8.2,
                    "price": 4.99,
                }

            if one or multiple arg(s) is(are) missing, banana doesn't
            exist, or there is an issue to query it from the DB,
            it will return a dict describing an error instead.
            Example (missing banana_id and color arg):
                {
                    "error": "Missing argument: id, color, , ",
                    "errorCode": 400,
                }
        """
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
        """Delete a single banana

        Delete a single banana chosen by the mandatory banana_id arg.
        Handle common errors such as banana_id arg missing, banana not
        existing or DB errors.

        Args:
            INT banana_id: mandatory to identify which banana to delete

        Returns:
            A dict describing how many bananas have been deleted.
            (should be one, since id is unique)
            Example (banana_id = 1):
                {
                    "banana_deleted": 1
                }

            if banana_id is missing, banana doesn't exist, or there is
            an issue to delete it from the DB, it will return a dict
            describing an error instead.
            Example (banana doesn't exist):
                {
                    "error": "This banana doesn't exist",
                    "errorCode": 404
                }
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
