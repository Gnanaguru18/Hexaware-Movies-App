import pyodbc
from datetime import date
from tabulate import tabulate

server_name = "TIGGER\\SQLEXPRESS"
database_name = "Ecom_application"
 
 
conn_str = (
    f"Driver={{SQL Server}};"
    f"Server={server_name};"
    f"Database={database_name};"
    f"Trusted_Connection=yes;"
)

print(conn_str)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

cursor.execute("Select 1")
print("Database connection is successful")

#############################################################################################

# CUSTOMER TABLE

class CustomerNotFoundException(Exception):
    def __init__(self, customer_id):
       print(f"Customer with ID {customer_id} not found")

class ProductNotFoundException(Exception):
    def __init__(self, customer_id):
       print(f"Customer with ID {customer_id} not found")

class Customer():
    def display_customer(self):
        cursor.execute("Select * from Customer")
        cust = cursor.fetchall() # Get all data
        headers = [column [0] for column in cursor.description]
        print(tabulate (cust, headers=headers, tablefmt="psql"))

    def create_customer(self,customer_id,customer_name,customer_email,customer_password):
        cursor.execute(
            """INSERT INTO customer (customer_id, name, email, password) VALUES (?, ?, ?, ?)
            insert into cart (customer_id)
            values (?)   """,
            (customer_id,customer_name,customer_email,customer_password,customer_id)
        )
        conn.commit()  

    def delete_customer(customer_id):
        
        rows_deleted = cursor.execute(
            """declare @a int = ?;
                    delete from Order_items
                    where order_id= (select order_id
                                    from orders
                                    where customer_id=@a)
                    delete from orders
                    where customer_id=@a

                    delete from Cart_items
                    where cart_id = (select cart_id
                                    from Cart
                                    where customer_id=@a)

                    delete from Cart
                    where customer_id=@a

                    delete from customer
                    where customer_id= @a
            """
            (customer_id,)
        ).rowcount
        conn.commit()
        try: 
            if rows_deleted == 0:
                raise CustomerNotFoundException(customer_id)
        except CustomerNotFoundException as e:
            print(e)

    def getOrdersByCustomer(self,customer_id):
        cursor.execute(
            """
        select oi.product_id,p.name,oi.quantity from orders o inner join
        Order_items oi on o.order_id=oi.order_id inner join
        Product p on p.product_id=oi.product_id
        where o.customer_id= ? """,
            (customer_id)
        )
        for customer in cursor:
            print(customer)



# PRODUCT TABLE
class Product:
    def delete_product(product_id):
        rows_deleted = cursor.execute("""
        select * from product
        """,
        (product_id,)
        ).rowcount
        conn.commit()
        try: 
            if rows_deleted == 0:
                raise ProductNotFoundException(product_id)
        except ProductNotFoundException as e:
            print(e)
    
  
#############################################################################################

# CART TABLE

class Cart:
    def display_cart(self):
        cursor.execute("Select * from Cart_items")
        #movies = cursor.fetchall()
        for customer in cursor:
            print(customer)

    def add_to_cart(self,cart_item_id,customer_id,prod_id,quantity):
        cursor.execute(
            """
            declare @a int = (select cart_id from Cart
					    where customer_id= ?);

            insert into Cart_items (cart_item_id,cart_id,product_id,quantity)
            values ( ?,@a , ? , ?)
            """,
            (customer_id,cart_item_id,prod_id,quantity)
        )
        conn.commit()

    # def create_cart(self,customer_id):
    #     cursor.execute(
    #     """
    #     insert into cart (customer_id)
    #     values (?)
    #     """,
    #     (customer_id)
    #     )
    #     conn.commit()


    def remove_from_cart(self,customer_id,prod_id):
        cursor.execute(
            """
            declare @a int = (select cart_id from Cart
					where customer_id= ?);

            delete from Cart_items
            where cart_id= @a and product_id = ?
           
            """,
            (customer_id,prod_id)
        )
        conn.commit()

    def getAllFromCart(self,customer_id):
        cursor.execute(
            """
        select c.customer_id,p.product_id,(p.name) as Product_name,ci.quantity from Cart c inner join
        Cart_items ci on c.cart_id=ci.cart_id
        join Product p on ci.product_id=p.product_id
        where c.customer_id= ?  """,
            (customer_id)
        )
        for customer in cursor:
            print(customer)

 ###########################################################################################

 # ORDER TABLE

class Order:
    def placeOrder(self,customer_id, pq_list, shippingAddress):
        today_date=str(date.today())
        cursor.execute(
        """
        insert into orders (customer_id,order_date,shipping_address)
        values (?,?,?)""",
        (customer_id,today_date,shippingAddress)
        
        )
        conn.commit()
    
        for i,j in pq_list.items():
            cursor.execute("""
            insert into Order_items (order_id,product_id,quantity)
            values ((select max(order_id) from orders), ?,?)""",
            (i,j)
            
            )
            conn.commit()

        cursor.execute("""
        update orders 
        set total_price=(select sum(price*quantity) from Product
        inner join Order_items on
        Product.product_id=Order_items.product_id 
        where order_id= (select max(order_id) from orders))
        where order_id=(select max(order_id) from orders)
        select * from orders    
            """        
        )
        conn.commit()
           




if __name__=='__main__':
   
    # order_access=Order()

    # customer_id=2
    # pq_list={4:5}
    # shipping_add="palaaani"
    # order_access.placeOrder(customer_id,pq_list,shipping_add)

    ####################################################3

    # Customer

    # customer_access = Customer()

    # customer_access.display_customer()

    # customer_id=int(input("Enter id:"))

    # customer_name=input("Enter name:")
    # customer_email=input("Enter mail")
    # customer_password=input("Enter password")
    # customer_access.create_customer(customer_id,customer_name,customer_email,customer_password)
    # customer_access.delete_customer(customer_id)
    # customer_access.display_customer()


    customer_access=Customer()

    while True:
        print("""
            Choose 
            1. Register Customer. 
            2. Create Product. 
            3. Delete Product. 
            4. Add to cart. 
            5. View cart. 
            6. Place order. 
            7. View Customer Order 
            8. Exit""")
        choice=int(input("Enter choice:"))
        if choice==1:
            customer_name=input("Enter Name:")
            customer_email=input("Enter Email:")
            customer_pass=input("Enter Password:")
            customer_access.create_customer(customer_name,customer_email,customer_pass)
        elif choice==2:
            pass
        elif choice==3:
            customer_access.display_customer()





cursor.close()
conn.close()
