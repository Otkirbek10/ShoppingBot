import sqlite3


class Database:
    def __init__(self, path_to_db="db.sqlite3"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

#     def create_table_users(self):
#         sql = """
#         CREATE TABLE Users (
#             id int NOT NULL,
#             Name varchar(255) NOT NULL,
#             email varchar(255),
#             language varchar(3),
#             PRIMARY KEY (id)
#             );
# """
#         self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self,tg_id: int, name: str,user_name = str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO mod_user(tg_id, name,user_name) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(tg_id, name,user_name), commit=True)

    def add_category(self,name: str):

        sql = """
        INSERT INTO mod_category(name) VALUES(?)
        """
        self.execute(sql, parameters=(name,), commit=True)

    def add_product(self,name: str,description:str,photo: str,price: int,category_id: int):

        sql = """
        INSERT INTO mod_product( name,description,photo,price,category_id) VALUES(?, ?, ?,?,?)
        """
        self.execute(sql, parameters=(name,description,photo,price,category_id), commit=True)

    def add_to_cart(self,tg_id: int,product:id,quantity:int):

        sql = """
        INSERT INTO mod_cart(tg_id,product,quantity) VALUES(?,?,?)
        """
        self.execute(sql, parameters=(tg_id,product,quantity), commit=True)

    def add_to_order(self,tg_id:int,name:str,phone:int,product:str):

        sql = """
        INSERT INTO mod_orders(tg_id,name,phone,product) VALUES(?,?,?,?)
        """
        self.execute(sql,parameters=(tg_id,name,phone,product),commit=True)

    def update_cart(self, tg_id: int, product: int, quantity: int):
        sql = "UPDATE mod_cart SET quantity=? WHERE tg_id=? AND product=?"
        return self.execute(sql, (quantity, tg_id, product), commit=True)

    def delete_product(self,id:int):
        sql = 'DELETE FROM mod_product WHERE id=?'
        return self.execute(sql, (id,), commit=True)

    def delete_product_for_category(self,category_id:int):
        sql = 'DELETE FROM mod_product WHERE category_id=?'
        return self.execute(sql, (category_id,), commit=True)

    def delete_from_cart(self,product:int):
        sql = 'DELETE FROM mod_cart WHERE product=? '
        return self.execute(sql, (product,), commit=True)

    def delete_from_cart_foruser(self,tg_id:int,product:int):
        sql = 'DELETE FROM mod_cart WHERE tg_id=? AND product=? '
        return self.execute(sql, (tg_id,product), commit=True)
    
    
    def delete_confirm_cart(self,**kwargs):
        sql = 'DELETE FROM mod_cart WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, commit=True)

    




    def select_product(self, **kwargs):    
        sql = "SELECT * FROM mod_product WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_cart_product(self, **kwargs):
        sql = "SELECT product FROM mod_cart WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_for_cart(self, **kwargs):
        sql = "SELECT * FROM mod_product WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_products(self):
        sql = """
        SELECT * FROM mod_product
        """
        return self.execute(sql, fetchall=True)


    def select_all_users(self):
        sql = """
        SELECT * FROM mod_user
        """
        return self.execute(sql, fetchall=True)

    def select_all_categories(self):
        sql = """
        SELECT * FROM mod_category
        """
        return self.execute(sql, fetchall=True)
    
    def select_orders(self):
        sql = """
        SELECT * FROM mod_orders
        """
        return self.execute(sql, fetchall=True)

    def select_cart(self, **kwargs):
        sql = "SELECT * FROM mod_cart WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def delete_category(self,id:int):
        sql = "DELETE FROM mod_category WHERE id=? "
        return self.execute(sql, (id,), commit=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM mod_user WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM mod_user;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    

def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")

