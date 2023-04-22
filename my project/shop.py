#Hosein Farzam
import tkinter
import sqlite3
import time 


# ----------------- create users table -------------
cnt=sqlite3.Connection("myshop.db")
print("connect to database...")

# query="""create table users
#   (id integer primary key,
#     user char(20) not null,
#     pass char(20) not null,
#     addr char(50) not null,
#     bought text not null,
#     JoiningDate char(50) not null) """

# cnt.execute(query)
# cnt.close()

t=time.strftime("%Y-%m-%d-%H:%M:%S")

# ----------------- init users table -------------
# query="""INSERT INTO users (user,pass,addr,bought,JoiningDate)
#       VALUES ('mahsa','123456789','teh',0,?) """
# cnt.execute(query,(t,))
# cnt.commit()
# cnt.close()

# ------------------- create product table ---------------
# query="""CREATE TABLE products
#   ( ID INTEGER PRIMARY KEY,
#   name CHAR(20) NOT NULL,
#   price int NOT NULL,
#   qnt int CHAR(50) NOT NULL,
#   comment TEXT)"""
 
# cnt.execute(query)
# cnt.close()



# query="""INSERT INTO products (name,price,qnt)
#       VALUES ('T-shirt','120','50') """
# cnt.execute(query)
# cnt.commit()
# cnt.close()     


# ----------------- create sale products -----------------
# query="""create table SaleProducts
#   (id integer primary key,
#     name char(20) not null,
#     TotalNumberOfSold text not null
#     ) """

# cnt.execute(query)
# cnt.close()


# ------------------------ insert sale products ---------------
# query="""INSERT INTO products (name,price,qnt,TotalNumberOfSold,comment)
#       VALUES ('infinity stones','99999999999999','0',0,'maybe one day...') """
# cnt.execute(query)
# cnt.commit()
# cnt.close()      

# ---------------------- create sale products time table ---------------
# query="""create table SaleProductsTime
#   (id integer primary key,
#     product char(20) not null,
#     NumberOfSold text not null,
#     customer char(20) not null,
#     time text not null
#     ) """

# cnt.execute(query)
# cnt.close()






# ----------------- functions ----------------
def login():
    global user_login
    user_login=user_txt.get()
    pas=pas_txt.get()
    
    if user_login=="" or pas=="":  # if len(user)==0 or len(pas)==0
        msg_lbl.configure(text="please fill the blanks!",fg="red")
        return
    
    query='''SELECT * from users WHERE user=? AND pass=?'''
    result=cnt.execute(query,(user_login,pas))
    rows=result.fetchall()
    if len(rows)==0:
        msg_lbl.configure(text="wrong username or pass",fg="red")
        return
    else:
        msg_lbl.configure(text="welcome to your account",fg="green")
        user_txt.delete(0,"end")
        pas_txt.delete(0,"end")
        login_btn.configure(state="disabled")
        logout_btn.configure(state="active")
        shop_btn.configure(state="active")
    if (user_login=="admin"):
        admin_btn.configure(state="active")


def logout():
    login_btn.configure(state="active")
    logout_btn.configure(state="disabled")
    shop_btn.configure(state="disabled")
    admin_btn.configure(state="disabled")
    msg_lbl.configure(text="you are logged out!",fg="green")


def final_submit():
    user=user1_txt.get()
    pas=pas1_txt.get()
    addr=addr1_txt.get()
    
    # -------------------- validation -----------------
    
    if user=="" or pas=="" or addr=="" :
        msg1_lbl.configure(text="fill all the blanks!",fg="red")
        return
    
    if len(pas)<8:
        msg1_lbl.configure(text="pass length error!",fg="red")
        return
    
    query="""select * from users where user=?"""
    
    result=cnt.execute(query,(user,))
    rows=result.fetchall()
    
    if len(rows)!=0:
        msg1_lbl.configure(text="username already exist!",fg="red")
        return
    
    query="""insert into users (user,pass,addr,bought,JoiningDate)
    values(?,?,?,?,?)"""
    cnt.execute(query,(user,pas,addr,0,t))
    cnt.commit()
    msg1_lbl.configure(text="submit done successfully!",fg="green")
    user1_txt.delete(0,"end")
    pas1_txt.delete(0,"end")
    addr1_txt.delete(0,"end")


def submit():
    global user1_txt,pas1_txt,addr1_txt,msg1_lbl
    win_submit=tkinter.Toplevel(win)
    win_submit.title("Submit")
    win_submit.geometry("200x200")
    
    # ---------------------- widgets ---------------------
    user1_lbl=tkinter.Label(win_submit,text="username: ")
    user1_lbl.pack()

    user1_txt=tkinter.Entry(win_submit,width=20)
    user1_txt.pack()

    pas1_lbl=tkinter.Label(win_submit,text="password: ")
    pas1_lbl.pack()

    pas1_txt=tkinter.Entry(win_submit,width=20)
    pas1_txt.pack()
    
    addr1_lbl=tkinter.Label(win_submit,text="address: ")
    addr1_lbl.pack()

    addr1_txt=tkinter.Entry(win_submit,width=20)
    addr1_txt.pack()

    msg1_lbl=tkinter.Label(win_submit,text="")
    msg1_lbl.pack()

    login1_btn=tkinter.Button(win_submit,text="submit now!",command=final_submit)
    login1_btn.pack()
    
    
    # -----------------------------------------
    win_submit.mainloop()



def send_info1():# it gets the time for another table...
    query_time="""INSERT INTO SaleProductsTime (product,NumberOfSold,customer,time)
            VALUES (?,?,?,?) """
    cnt.execute(query_time,(p_name,1,user_login,t))
    cnt.commit()
    

def buy():
    global p_name
    global desired
    desired=select_txt.get()
        
    query='''select * from products where id=?'''
    result=cnt.execute(query,(desired,))
    rows=result.fetchall()
    
    if desired=="":
        msgSH_lbl.configure(text="fill the blank!",fg="red")
        return
    
    if len(rows)==0:
        msgSH_lbl.configure(text="product doesn't exist!",fg="red")
        select_txt.delete(0,"end")
        return
    
    query2='''select qnt from products where id=?'''
    result=cnt.execute(query2,(desired,))
    rows2=result.fetchall()

    for count in rows2:
        qnt=count
    if 0 in qnt:
        msgSH_lbl.configure(text="the product is unavailable!",fg="red")
        select_txt.delete(0,"end")
        return
    
    
    
    query3='''UPDATE products SET qnt=qnt-1 WHERE ID=?'''
    cnt.execute(query3,(desired,))
    cnt.commit()
    
    query4='''UPDATE products SET TotalNumberOfSold=TotalNumberOfSold+1 WHERE ID=?'''
    cnt.execute(query4,(desired,))
    cnt.commit()
    
    query5='''UPDATE users SET bought=bought+1 WHERE user=?'''
    cnt.execute(query5,(user_login,))
    cnt.commit()
    
    msgSH_lbl.configure(text="bought successfully!",fg="green")
    select_txt.delete(0,"end")
    
    # ----------- for sending the info ----------------
    query_send='''select * from products where id=?'''
    result=cnt.execute(query_send,(desired,))
    rows_send=result.fetchall()
    for item_send in rows_send:
        p_name=item_send[1]
    
    # query_send2='''select * from users where id=?'''
    # result=cnt.execute(query_send2,(desired,))
    # rows_send2=result.fetchall()
    # for item_send in rows_send2:
    #     c_name=item_send[3]
    send_info1()


def shop():
    global select_txt
    global msgSH_lbl
    win_shop=tkinter.Toplevel(win)
    win_shop.title("Shop")
    win_shop.geometry("400x400")
    
    lstbox=tkinter.Listbox(win_shop,width=50)
    lstbox.pack()
    
    query=""" select * from products"""
    result=cnt.execute(query)
    rows=result.fetchall()
    
    for product in rows:
        #mystr=str(product[0])+" "product[1]+" "+str(product[2])
        mystr=f"id: {product[0]}   name: {product[1]}   price: {product[2]}   qnt={product[3]}"
        lstbox.insert(0, mystr)
    
    select_lbl=tkinter.Label(win_shop,text="select the product by id: ")
    select_lbl.pack()

    select_txt=tkinter.Entry(win_shop,width=20)
    select_txt.pack()
    
    msgSH_lbl=tkinter.Label(win_shop,text="")
    msgSH_lbl.pack()
    
    buy_btn=tkinter.Button(win_shop,text="buy it!",command=buy)
    buy_btn.pack()
    
    
    
    
    
    
    
    
    
    
    win_shop.mainloop()

# ----------------------------- all about admin ------------------------------------------------
def registered_users():
    win_registered=tkinter.Toplevel(win_admin)
    win_registered.title("registered users list")
    win_registered.geometry("400x200")
    
    lstbox=tkinter.Listbox(win_registered,width=50)
    lstbox.pack()
    
    query=""" select * from users"""
    result=cnt.execute(query)
    rows=result.fetchall()
    
    for user in rows:
        mystr=user[1]
        time=user[5]
        lstbox.insert(0, mystr+" ---> "+"joining date: "+time)
        
    win_registered.mainloop()

def available_products():
    win_available=tkinter.Toplevel(win_admin)
    win_available.title("available products list")
    win_available.geometry("200x200")
    
    lstbox=tkinter.Listbox(win_available,width=20)
    lstbox.pack()
    
    query=""" select * from products"""
    result=cnt.execute(query)
    rows=result.fetchall()
    
    for product in rows:
        mystr=product[1]
        qnt=product[3]
        if int(qnt)!=0:
            lstbox.insert(0, mystr)
    
    win_available.mainloop()

def unavailable_products():
    win_unavailable=tkinter.Toplevel(win_admin)
    win_unavailable.title("unavailable products list")
    win_unavailable.geometry("200x200")
    
    lstbox=tkinter.Listbox(win_unavailable,width=20)
    lstbox.pack()
    
    query=""" select * from products"""
    result=cnt.execute(query)
    rows=result.fetchall()
    
    for product in rows:
        mystr=product[1]
        qnt=product[3]
        if int(qnt)==0:
            lstbox.insert(0, mystr)
    
    win_unavailable.mainloop()

def best_selling():
    win_best_selling=tkinter.Toplevel(win_admin)
    win_best_selling.title("best selling products list")
    win_best_selling.geometry("400x200")
    
    lstbox=tkinter.Listbox(win_best_selling,width=50)
    lstbox.pack()
    
    query='''select * from products where TotalNumberOfSold!=0'''   
    result=cnt.execute(query)
    rows=result.fetchall()
    
    for product in rows:
        mystr=product[1]
        tsold=product[4]
        lstbox.insert(0,mystr+" ---> "+"total number of sold: "+tsold)
    
    win_best_selling.mainloop()

def lowest_selling():
    win_lowest_selling=tkinter.Toplevel(win_admin)
    win_lowest_selling.title("best selling products list")
    win_lowest_selling.geometry("500x200")
    
    lstbox=tkinter.Listbox(win_lowest_selling,width=50)
    lstbox.pack()
    
    query='''select * from products where TotalNumberOfSold=0'''   
    result=cnt.execute(query)
    rows=result.fetchall()
    
    for product in rows:
        mystr=product[1]
        tsold=product[4]
        lstbox.insert(0,mystr+" ---> "+"total number of sold: "+tsold)
    
    win_lowest_selling.mainloop()


def product_date():
    global win_date
    global show
    global lstbox2
    win_date=tkinter.Toplevel(win_admin)
    win_date.title("sold products / date list")
    win_date.geometry("400x400")
    
    lstbox=tkinter.Listbox(win_date,width=80)
    lstbox.pack()
    
    query=""" select * from SaleProductsTime"""
    result=cnt.execute(query)
    rows=result.fetchall()
    
    for opt in rows:
        product_t=opt[1]
        time=opt[4]
        customer_t=opt[3]
        lstbox.insert(0, "time: "+time+" ---> "+"product: "+product_t+" ---> "+"boght by: "+customer_t)
    
    
    win_date.mainloop()


def best_customers():
    win_customers=tkinter.Toplevel(win_admin)
    win_customers.title("best customers list")
    win_customers.geometry("300x200")
    
    lstbox=tkinter.Listbox(win_customers,width=50)
    lstbox.pack()
    
    query=""" select * from users where bought!=0"""
    result=cnt.execute(query)
    rows=result.fetchall()
    
    for user in rows:
        mystr=user[1]
        bought=user[4]
        if int(bought)==1:
            lstbox.insert(0, mystr+" ---> "+"bought from shop: "+bought+" time")
        else:
            lstbox.insert(0, mystr+" ---> "+"bought from shop: "+bought+" times")
    
    win_customers.mainloop()

def admin_panel():
    global win_admin
    win_admin=tkinter.Toplevel(win)
    win_admin.title("admin panel")
    win_admin.geometry("200x200")
    
    # ---------------------- widgets ---------------------
    user_btn=tkinter.Button(win_admin,text="registered users",command=registered_users)
    user_btn.pack()
    
    available_btn=tkinter.Button(win_admin,text="available products",command=available_products)
    available_btn.pack()
    
    unavailable_btn=tkinter.Button(win_admin,text="unavailable products",command=unavailable_products)
    unavailable_btn.pack()
    
    best_btn=tkinter.Button(win_admin,text="the best selling products",command=best_selling)
    best_btn.pack()
    
    lowest_btn=tkinter.Button(win_admin,text="the lowest selling products",command=lowest_selling)
    lowest_btn.pack()
    
    sold_btn=tkinter.Button(win_admin,text="sold products / date",command=product_date)
    sold_btn.pack()
    
    customer_btn=tkinter.Button(win_admin,text="the best customers",command=best_customers)
    customer_btn.pack()
    
    
    
    win_admin.mainloop()


def contact():
    message=tkinter.messagebox.showinfo("info","""thebestshop@gmail.com 
givemethehighestscore@gmail.com""")

def about_us():
    win_about=tkinter.Toplevel(win)
    win_about.title("info")
    win_about.geometry("500x500")
    about_lbl=tkinter.Label(win_about,text='''Here is an online retailer and web service provider.\n
      Our company provides products such as apparel, beauty and health products,
electronics, supernatural and rare items, grocery, games and tools.\n\nBetter buy from us ;)\n\nFounded: April 13, 2023\n\n''')
    about_lbl.pack()
    
    about__btn=tkinter.Button(win_about,text="contact us",command=contact)
    about__btn.pack()


#--------------------------------------

win=tkinter.Tk()
win.title("main")
win.geometry("300x300")


# ------------------ widgets------------

user_lbl=tkinter.Label(text="username: ")
user_lbl.pack()

user_txt=tkinter.Entry(width=20)
user_txt.pack()

pas_lbl=tkinter.Label(text="password: ")
pas_lbl.pack()

pas_txt=tkinter.Entry(width=20)
pas_txt.pack()

msg_lbl=tkinter.Label(text="")
msg_lbl.pack()

login_btn=tkinter.Button(text="login",command=login)
login_btn.pack()

logout_btn=tkinter.Button(text="logout",state="disabled" ,command=logout)
logout_btn.pack()

submit_btn=tkinter.Button(text="submit" ,command=submit)
submit_btn.pack()

shop_btn=tkinter.Button(text="shop" ,state="disabled",command=shop)
shop_btn.pack()

admin_btn=tkinter.Button(text="admin panel" ,state="disabled",command=admin_panel)
admin_btn.pack()

about_btn=tkinter.Button(text="about us",command=about_us)
about_btn.pack()







win.mainloop()
