import json
import initialization_handler


class AllBananas(initialization_handler.InitializationHandler):
    def get(self):
        """
        Get all bananas and write them in a JSON format
        Takes no parameters
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
        """
        Add a banana and write its id.
        Takes 3 argument :
         - color STRING
         - size REAL
         - price REAL
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
