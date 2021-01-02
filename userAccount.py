import psycopg2


def connectToDatabase():
    DB_NAME = "ebblwauk"
    DB_USER = "ebblwauk"
    DB_PASS = "bnaS-Dso9WocygKY887Ow_hNdFM_wng8"
    DB_HOST = "hattie.db.elephantsql.com"
    DB_PORT = "5432"

    connection = psycopg2.connect(
        database=DB_NAME, user=DB_USER,
        password=DB_PASS, host=DB_HOST, port=DB_PORT)
    print("Database connected successfully")
    return connection


class userAccount:
    def __init__(self, connection):
        self.user_id = None
        self.connection = connection

    def LogIn(self, t_email, t_password):
        with self.connection.cursor() as curs:
            query = "SELECT customer_id FROM customer WHERE email = %s AND c_password = crypt(%s, c_password)"
            curs.execute(query, [t_email, t_password])
            rows = curs.fetchall()
            print(rows)
            if rows:
                self.user_id = int(rows[0][0])

    def Create(self, t_email, t_password):
        with self.connection.cursor() as curs:
            query = "INSERT INTO customer(email, c_password) VALUES(%s, crypt(%s, gen_salt('bf')))"
            curs.execute(query, [t_email, t_password])
            self.connection.commit()

    def isLoginSuccessfull(self):
        return self.user_id is not None


# ac = userAccount()
# print(ac.LogIn('nick.addington@asia-links.com', 'andrea'))

# print(ac.LogIn('nick.addington@asia-links.com', 'andrea1'))
# ac.disconnect()

# con = connectToDatabase()
# u = userAccount(con)
# u.Create("120@mail.ru", "12142k22nn2")
# u.close()
