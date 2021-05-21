import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


def dict_factory(cursor,row):
    d={}
    for idx,col in enumerate(cursor.description):
        d[col[0]]=row[idx]
    return d


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS Items (id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT,price  TEXT, brand TEXT, picture BLOB, stock INT)')
    print(" Item Table created successfully")
    #conn.execute('CREATE TABLE IF NOT EXISTS ADMIN (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT,password TEXT)')
    #print("ADMIN Table created successfully")
    conn.close()


init_sqlite_db()


def add_admin():
    # if request.method == "POST":
    msg = None
    try:

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO ADMIN (username,password) VALUES ('admin', 'admin')", )
            con.commit()
            msg = " admin was successfully added to the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred in insert operation: " + str(e)
    finally:
        con.close()
        print(msg)


app = Flask(__name__)
CORS(app)


@app.route('/')
def land():
    land=""
    return ("<p>Add /show-records/ to url to view json records</p><p>\n Netlify link :https://admiring-minsky-04b5fe.netlify.app/index.html</p>")



@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    if request.method == "POST":

        msg = None
        try:
            post_data = request.get_json()
            product_name = post_data['product_name']
            price = post_data['price']
            brand = post_data['brand']
            picture = post_data['picture']
            stock = post_data['stock']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Items (product_name, price, brand, picture,stock) VALUES (?, ?, ?, ?,?)", (product_name, price, brand, picture, stock))
                con.commit()
                msg = product_name + " was successfully added to the database."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            con.close()
            return jsonify(msg)


@app.route('/login/',methods=['POST'])
def login():
    msg=None
    try:
        post_data = request.get_json()
        username=post_data['username']
        password=post_data['password']
        with sqlite3.connect('database.db') as con:
            cur=con.cursor()
            sql=("SELECT * FROM Admin WHERE username = ? and password = ?")
            cur.execute(sql,[username,password])
            records=cur.fetchall()

    except Exception as e:
        con.rollback()
        msg=("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
        return jsonify(msg)

'''-------------------------------------------------------------------------------------------'''
@app.route('/show-records/', methods=["GET"])
def show_records():
    records = []
    try:

        with sqlite3.connect('database.db') as con:
            con.row_factory=dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM Items")
            records = cur.fetchall()
        ''' for row in records:
                print(row)

            for i in row:
                print(i)
            print((records))'''
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
        return jsonify(records)


@app.route('/show-admin/', methods=["GET"])
def show_admin():
    records = []
    try:

        with sqlite3.connect('database.db') as con:
            con.row_factory=dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM ADMIN")
            records = cur.fetchall()
        ''' for row in records:
                print(row)

            for i in row:
                print(i)
            print((records))'''
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
        return jsonify(records)



@app.route('/edit-item/<int:product_id>/',methods=['PUT'])
def edit_product(product_id):
    post_data = request.get_json()
    records = {'id':product_id,
               'product_name' : post_data['product_name'],
               'price' :post_data['price'],
                'brand' : post_data['brand'],
               'picture' : post_data['picture'],
               'stock': post_data['stock']}
    #Database
    con =sqlite3.connect('database.db')
    #cursor
    cur = con.cursor()
    sql= ("UPDATE Items SET product_name = ?, price = ?, brand = ?, picture = ?, stock = ?  WHERE id= ?")
    cur.execute(sql,(records['product_name'],records['price'],records['brand'],records['picture'],records['stock'],records['id']))

    con.commit()


    return jsonify(records)


@app.route('/delete-item/<int:product_id>/', methods=["DELETE"])
def delete_product(product_id):

    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Items WHERE id=" + str(product_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return (msg)

# @app.route('/search/show-records/',methods=['POST'])
# def searchItem():
#     if request.method == "POST":
#
#         try:
#             post_data = request.get_json()
#             product_name=post_data['search']
#             with sqlite3.connect('database.db') as con:
#                 con.row_factory=dict_factory
#                 #Database
#                 cur =con.cursor()
#                 #cursor
#                 cur.execute("SELECT * FROM Items WHERE product_name= ?",
#                         (product_name))
#                 data=cur.fetchall()
#
#         except Exception as e:
#             print("sum not right",str(e))
#
#         finally:
#             con.close()
#             return jsonify(data)
#


if __name__=="__main__":
    app.run(debug=True)
