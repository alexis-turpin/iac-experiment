import json
import initialization_handler


class AllBananas(initialization_handler.InitializationHandler):
    """All Bananas handler

    Implement the GET and POST methods for all bananas
    """
    def get(self):
        """Get all bananas

        Get every single bananas from the database and returns them in a
        ordered JSON format.
        Handle database errors.

        Takes no parameters

        Returns:
            JSON ordered data containing all bananas in the DB.
            Example (with 2 bananas):
                [
                    {
                        "id": 1,
                        "price": 5.5,
                        "color": "yellow",
                        "size": 10.5
                    },
                    {
                        "id": 2,
                        "price": 7,
                        "color": "green",
                        "size": 8.3
                    },
                ]

            In case of database error, it will return a dict describing
            the encountered error.
            Example:
            {
                "error": "Couldn't query all Bananas:[ERROR_MESSAGE],"
                "errorCode": 500
            }
        """
        conn = self.connect_db()
        try:
            with conn.cursor() as cursor:
                qty = cursor.execute('SELECT * FROM `bananas`')
                query = cursor.fetchall()
        except Exception as e:
            self.write(
                {
                    "error": "Couldn't query all Bananas:    " + str(e),
                    "errorCode": 500
                }
            )
        else:
            self.write(json.dumps(
                [
                    {
                        "id": q[0],
                        "color": q[1],
                        "size": q[2],
                        "price": q[3],
                    }
                    for q in query
                    ],
                # indent=4
            ))
        finally:
            conn.close()

    def post(self):
        """Post a new banana.

        Create a new banana in the database using mandatory color, size
        and price arguments. Catch misuse of the method with a banana_id
        argument.
        Handle common errors such as missing args,
        forbidden banana_id arg or DB errors.

        Args:
            STR color: mandatory chosen color of the banana to create
            FLOAT size: mandatory chosen size of the banana to create
            FLOAT price: mandatory chosen price of the banana to create

        Returns:
             A dict containing a last_row_id : the banana_id of the
             created banana_id.
             Example:
                 {"last_row_id": 3}

             If arguments are missing, a banana_id arg is provided or it
             encounters a DB error, it will return a dict describing an
             error instead.
             Example (banana_id argument provided):
                {
                    "error": ("POST method cannot have id argument,"
                              "consider using singleBanana PUT method"),
                    "errorCode": 400,
                }
        """
        banana_id = self.get_argument("id", None)
        color = self.get_argument("color", "yellow")
        size = self.get_argument("size", None)
        price = self.get_argument("price", None)
        if color and size and price and not banana_id:
            conn = self.connect_db()
            try:
                with conn.cursor() as cursor:
                    sql = ('INSERT INTO `bananas` (`color`, `size`, `price`)'
                           'VALUES (%s, %s, %s)')
                    cursor.execute(
                        sql,
                        (color, size, price)
                    )
                    last_row_id = cursor.lastrowid
            except Exception as e:
                self.write(
                    {
                        "error": "Couldn't INSERT banana:    " + str(e),
                        "errorCode": 500
                    }
                )
            else:
                conn.commit()
                self.write({"last_row_id": last_row_id})
            finally:
                conn.close()
        elif banana_id:
            self.write(
                {
                    "error": ("POST method cannot have id argument,"
                              "consider using singleBanana PUT method"),
                    "errorCode": 400,
                }
            )
        else:
            self.write(
                {
                    "error": "Missing argument: " + ", ".join(
                        [
                            bool(color) * "color",
                            bool(size) * "size",
                            bool(price) * "price"
                        ]
                    ),
                    "errorCode": 400,
                }
            )
