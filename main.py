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

    def create_customer(self,customer_name,customer_email,customer_password):
        cursor.execute(
            """INSERT INTO customer (name, email, password) VALUES ( ?, ?, ?)
            declare @a int = (select max(customer_id) from customer)
            insert into cart (customer_id)
            values (@a)   """,
            (customer_name,customer_email,customer_password)
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
            """,
            (customer_id)
        ).rowcount
        conn.commit()
        try: 
            if rows_deleted == 0:
                raise CustomerNotFoundException(customer_id)
        except CustomerNotFoundException as e:
            print(e)





# PRODUCT TABLE
class Product:
    def display_product(self):
        cursor.execute("Select * from Product")
        product = cursor.fetchall() # Get all data
        headers = [column [0] for column in cursor.description]
        print(tabulate (product, headers=headers, tablefmt="psql"))

    def createProduct(self,name,price,description,stock_quantity):
        cursor.execute( "insert into Product ( name, price, description, stock_quantity) values(?,?,?,?)",
                       (name,price,description,stock_quantity))
        conn.commit()

    def delete_product(self,product_id):
        rows_deleted = cursor.execute("""
        delete from Order_items where product_id=?
        delete from Cart_items where product_id=?
        delete from Product where product_id=?
        """,
        (product_id,product_id,product_id)
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
        cart = cursor.fetchall() # Get all data
        headers = [column [0] for column in cursor.description]
        print(tabulate (cart, headers=headers, tablefmt="psql"))
        

    def add_to_cart(self,customer_id,prod_id,quantity):
        cursor.execute(
            """
            declare @a int = (select cart_id from Cart
					    where customer_id= ?);

            insert into Cart_items (cart_id,product_id,quantity)
            values ( @a , ? , ?)
            """,
            (customer_id,prod_id,quantity)
        )
        conn.commit()

 
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
        cart = cursor.fetchall() # Get all data
        headers = [column [0] for column in cursor.description]
        print(tabulate (cart, headers=headers, tablefmt="psql"))

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
        print("Your order has been placed")


    def getOrdersByCustomer(self,customer_id):
        cursor.execute(
            """
        select oi.product_id,p.name,oi.quantity from orders o inner join
        Order_items oi on o.order_id=oi.order_id inner join
        Product p on p.product_id=oi.product_id
        where o.customer_id= ? """,
            (customer_id)
        )
        order = cursor.fetchall() # Get all data
        headers = [column [0] for column in cursor.description]
        print(tabulate (order, headers=headers, tablefmt="psql"))
        




if __name__=='__main__':
   
    customer_access=Customer()
    cart_access=Cart()
    order_access=Order()
    product_access=Product()

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
            customer_access.display_customer()

        elif choice==2:
            product_name=input("Enter product name:")
            price=int(input("Enter product price:"))
            description=input("Enter product description:")
            stock_quantity=int(input("Enter product quantity:"))
            product_access.createProduct(product_name,price,description,stock_quantity)

        elif choice==3:
            product_access.display_product()
            product_id=int(input("Enter product ID:"))
            product_access.delete_product(product_id)

        elif choice==4:
            customer_id=int(input("Enter customer ID:"))
            product_id=int(input("Enter product ID:"))
            quantity=int(input("Enter quantity:"))
            cart_access.add_to_cart(customer_id,product_id,quantity)

        elif choice==5:
            customer_id=int(input("Enter customer ID:"))
            cart_access.getAllFromCart(customer_id)

        elif choice==6:
            customer_id=int(input("Enter customer ID:"))
            pq = {}
            num_entries = int(input("Enter the number of products you want to add: "))
            for i in range(num_entries):
                product = input("Enter product ID: ")
                quantity = input("Enter quantity: ")
                pq.update({product: quantity})
            shipping_address=input("Enter shipping address:")
            order_access.placeOrder(customer_id,pq,shipping_address)

        elif choice==7:
            customer_id=int(input("Enter customer ID:"))
            order_access.getOrdersByCustomer(customer_id)

        elif choice==8:
            break
        else:
            print("Wrong choice ❌")








cursor.close()
conn.close()
