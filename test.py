import pyodbc
from datetime import date

server_name = "TIGGER\\SQLEXPRESS"
database_name = "TEST2"


class ProductNotFoundException(Exception):
    def __init__(self, customer_id):
       print(f"Customer with ID {customer_id} not found")


conn_str = (
    f"Driver={{SQL Server}};"
    f"Server={server_name};"
    f"Database={database_name};"
    f"Trusted_Connection=yes;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

cursor.execute("Select 1")
print("Database connection is successful")

class customer:
    def delete_product(product_id):
        rows_deleted = cursor.execute(
            """
            DELETE FROM product
            WHERE product_id = ?
            """,
            (product_id,)
        ).rowcount
        conn.commit()
        try: 
            if rows_deleted == 0:
                raise ProductNotFoundException(product_id)
        except ProductNotFoundException as e:
            print(e)

customer.delete_customer(1002)


from tabulate import tabulate
class MovieService:
def read_movies(self):
cursor.execute("Select * from Movies")
movies = cursor.fetchall() # Get all data
headers = [column [0] for column in cursor.description]
print(tabulate (movies, headers=headers, tablefmt="psql"))