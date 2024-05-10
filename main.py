import pyodbc

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

class Customer:
    def display_customer(self):
        cursor.execute("Select * from Customer")
        #movies = cursor.fetchall()
        for customer in cursor:
            print(customer)

    def create_customer(self,customer_id,customer_name,customer_email,customer_password):
        cursor.execute(
            "INSERT INTO customer (customer_id, name, email, password) VALUES (?, ?, ?, ?)",
            (customer_id,customer_name,customer_email,customer_password)
        )
        conn.commit()   # Permanent storing | If no commit then no data | Before commiting we can change the values and redo

    def delete_customer(self,id):
        cursor.execute(
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
            (id)
        )
        conn.commit()

    def getOrdersByCustomer(self,cust_id):
        cursor.execute(
            """
        select oi.product_id,p.name,oi.quantity from orders o inner join
        Order_items oi on o.order_id=oi.order_id inner join
        Product p on p.product_id=oi.product_id
        where o.customer_id= ? """,
            (cust_id)
        )
        for customer in cursor:
            print(customer)



    

  
#############################################################################################

# CART TABLE

class Cart:
    def display_cart(self):
        cursor.execute("Select * from Cart_items")
        #movies = cursor.fetchall()
        for customer in cursor:
            print(customer)

    def add_cart(slef,cart_item_id,cust_id,prod_id,quantity):
        cursor.execute(
            """
            declare @a int = (select cart_id from Cart
					    where customer_id= ?);

            insert into Cart_items (cart_item_id,cart_id,product_id,quantity)
            values ( ?,@a , ? , ?)
            """,
            (cust_id,cart_item_id,prod_id,quantity)
        )
        conn.commit()

    def remove_cart(self,cust_id,prod_id):
        cursor.execute(
            """
            declare @a int = (select cart_id from Cart
					where customer_id= ?);

            delete from Cart_items
            where cart_id= @a and product_id = ?
           
            """,
            (cust_id,prod_id)
        )
        conn.commit()

    def getAllFromCart(self,cust_id):
        cursor.execute(
            """
        select c.customer_id,p.product_id,(p.name) as Product_name,ci.quantity from Cart c inner join
        Cart_items ci on c.cart_id=ci.cart_id
        join Product p on ci.product_id=p.product_id
        where c.customer_id= ?  """,
            (cust_id)
        )
        for customer in cursor:
            print(customer)

    







cart_item=Cart()


# cart_item_id=int(input("Enter cart_item id:"))
# cust_id=int(input("Enter id:"))
# prod_id=int(input("Enter product id:"))
# quantity=int(input("Enter quantity:"))

# cart_item.add_cart(cart_item_id,cust_id,prod_id,quantity)
#cart_item.remove_cart(cust_id,prod_id)

cust_id=int(input("Enter id:"))

cart_item.getAllFromCart(cust_id)




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


cursor.close()
conn.close()