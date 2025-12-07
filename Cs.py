# importing modules
import mysql.connector as m
# The 's' variable will store user details after successful login/sign-in.
s = [] 

def login():
    """Handles user login."""
    global s
    try:
        print('-------------------------------------------------')
        e = int(input("Enter your user ID:"))
        x = input("Enter user name:")
        y = int(input("Enter your password:"))
        
        # Connect to the database (hardcoded credentials as per the project)
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        
        # Check credentials
        co.execute("select * from users")
        xj = co.fetchall()
        jl = 5
        
        for i in xj:
            if x == i[1] and str(y) == str(i[2]) and e == i[0]:
                jl = 6
                print("login successful.")
                co.execute('select * from users where UserID={} and UserName="{}" and Password={}'.format(e, x, y))
                s_result = co.fetchall()
                s = s_result # Update the global 's'
                return s_result
                
        if jl == 5:
            print("wrong details given")
            return []
            
        mydb.commit()
        print('-------------------------------------------------')
        
    except ValueError:
        print('Invalid input given.')
    except TypeError:
        print("invalid data type")
    except m.Error as err:
        print(f"Database error: {err}")
    return []

def room_booking(s):
    """Handles room booking process."""
    try:
        print('-------------------------------------------------')
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        co.execute('select * from roombooking ')
        g = co.fetchall()
        
        a = int(input("Enter your selected Room Number: "))
        # Logic to generate next Booking ID
        x = g[-1][1] + 1 if g else 1001
        print("Your Booking ID is", x)
        
        k = s[0][0] # user's id
        y = s[0][1] # user's name
        z = input("Enter Address: ")
        p = int(input("Enter Phone number:"))
        e = input('Enter check in date (YYYY-MM-DD):')
        t = input('Enter check out date (YYYY-MM-DD):')
        w = input('Enter your gender: ')
        
        co.execute('select RoomNum, Status from rooms')
        qw = co.fetchall()
        wq = [ie[0] for ie in qw]
        booked = False
        
        for ie in qw:
            room_num = ie[0]
            status = ie[1].strip().capitalize()
            
            if room_num == a:
                if status == 'Vacant':
                    # Insert into roombooking (Room_Num, Booking_ID, User_ID, User_Name, Address, Phone_Num, CheckIn, Cheak Out, Gender)
                    co.execute("insert into roombooking values({},{},{},'{}','{}',{},'{}','{}','{}')".format(a, x, k, y, z, p, e, t, w))
                    # Update room status to Occupied
                    co.execute("update rooms set Status='{}' where RoomNum={}".format('Occupied', a))
                    print('Room booked.')
                    booked = True
                    break
                elif status == 'Occupied':
                    print('''Room chosen is already booked by someone.
Please choose another room. ''')
                    booked = True
                    break
        
        if a not in wq and not booked:
            print('Entered room number does not exist.')
            
        mydb.commit()
        
    except ValueError:
        print('Invalid input given.')
    except TypeError:
        print("Invalid type of data given.")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

    print('-------------------------------------------------')

def room_details():
    """Displays all room details from the 'rooms' table."""
    print('-------------------------------------------------')
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        co.execute('select * from rooms')
        q = co.fetchall()
        for j in q:
            print(j)
        mydb.commit()
    except Exception as e:
        print(f"Error fetching room details: {e}")
    print('-------------------------------------------------')

def menu():
    """Displays the restaurant menu."""
    print('-------------------------------------------------')
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        print("*****MENU*****")
        print('item_number, item_name, price, category, availability')
        co.execute('select * from menu')
        a = co.fetchall()
        for i in a:
            print(i)
        mydb.commit()
    except Exception as e:
        print(f"Error fetching menu: {e}")
    print('-------------------------------------------------')

def order():
    """Handles the food ordering process."""
    global s
    if not s:
        print("Please log in or sign up first.")
        return

    print('-------------------------------------------------')
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        r = s[0][0] # user id
        
        # Determine the table number (Logic updated to check booking or ask)
        co.execute('select TableNum from table_booking where UserID = {} ORDER BY Date DESC, Time DESC LIMIT 1'.format(r))
        table_result = co.fetchone()
        
        if table_result:
            rq = table_result[0]
            print("Your Table Number is", rq)
        else:
            rq = int(input("Enter your Table Number (must be already booked/assigned): "))

        co.execute('select * from order_info')
        ret_new = co.fetchall()
        
        # Generate next Order Number
        b = len(ret_new) + 1 
        
        co.execute('select * from menu')
        me = co.fetchall() # all dishes
        
        srt = int(input("Enter no. of distinct items to be ordered: "))
        ta = 0 # Total amount
        
        for i in range(srt):
            k = int(input("Enter the item number to be ordered: "))
            e = int(input("Enter the quantity of above item to be ordered: "))
            
            item_found = False
            for p in me:
                if k == p[0]: # ItemNum matches
                    pri = p[2] # price of a dish
                    st = pri * e # subtotal
                    
                    # Insert into order_details (OrderNum, ItemNum, Quantity, Subtotal)
                    co.execute('insert into order_details values({},{},{},{})'.format(b, k, e, st))
                    ta = ta + st
                    item_found = True
                    break
            
            if not item_found:
                print(f"Item number {k} not found in menu. Skipping.")
                
        # Insert into order_info (OrderNum, User_ID, Table_Num, Total_Amount)
        co.execute('insert into order_info values({},{},{},{})'.format(b, r, rq, ta))
        
        mydb.commit()
        print('Your order has been placed. Total Amount: {}'.format(ta))
        
    except ValueError:
        print('Invalid input given (expected a number).')
    except Exception as e:
        print(f"An error occurred during order placement: {e}")

    print('-------------------------------------------------')

def table_booking():
    """Handles restaurant table booking."""
    global s
    if not s:
        print("Please log in or sign up first.")
        return

    print('-------------------------------------------------')
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        
        tn = int(input('Enter Table number:'))
        uid = s[0][0] # user id
        date = input('Enter date booked (YYYY-MM-DD): ')
        time = input('Enter time booked (HH:MM:SS): ')
        
        # Insert into table_booking (TableNum, User_ID, Date, Time)
        co.execute('insert into table_booking values({},{},"{}","{}")'.format(tn, uid, date, time))
        print('Table booked.')
        mydb.commit()
        
    except ValueError:
        print('Invalid input given (expected a number for Table number).')
    except Exception as e:
        print(f"An error occurred during table booking: {e}")
        
    print('-------------------------------------------------')
    
# --- Staff Management Functions ---

def insert_sdetails():
    """Adds a new staff member's details to the 'staff' table."""
    global s
    if not s:
        print("Please log in or sign up first.")
        return

    print("--------------------------------------------------")
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        
        p = s[0][0] # user id (from current session)
        k = s[0][1] # user name (from current session)
        m = input("Enter department:")
        h = int(input("Enter phone number:"))
        i = input("Enter date of joining (YYYY-MM-DD):")
        l = input("Enter address:")
        s_gender = input("Enter gender:")
        w = "STAFF"
        
        # Insert into staff (User_Id, User_name, dept, phone_number, DateOfJoining, address, Gender, User_type)
        co.execute("insert into staff values({},'{}','{}',{},'{}','{}','{}','{}')".format(p, k, m, h, i, l, s_gender, w))
        print("data successfully inserted")
        mydb.commit()
        
    except ValueError:
        print('Invalid input given (expected a number for phone number).')
    except Exception as e:
        print(f"An error occurred during staff detail insertion: {e}")

    print("--------------------------------------------------")

def remove_sdetails():
    """Removes a staff member's details by UserID."""
    print("_______________________________________")
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        c = int(input("Enter UserID of the staff member to remove: ")) 
        co.execute("delete from staff where UserID ={}".format(c))
        print("data successfully removed")
        mydb.commit()
    except ValueError:
        print('Invalid input given (expected a number).')
    except Exception as e:
        print(f"An error occurred during staff detail removal: {e}")
    print("________________________________________________")
    
def staff_name_change():
    """Allows staff to change their name."""
    global s
    if not s: return
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        pu = s[0][0] # user id
        x = input('Enter the new name:')
        co.execute('update users set UserName="{}" where UserID={}'.format(x, pu))
        co.execute('update staff set UserName="{}" where UserID={}'.format(x, pu))
        s[0] = (s[0][0], x, s[0][2], s[0][3]) # Update session variable
        print('Name updated successfully.')
        mydb.commit()
    except:
        print('Enter a valid value')
    print("--------------------------------------------")

def staff_department_change():
    """Allows staff to change their department."""
    global s
    if not s: return
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        pu = s[0][0] # user id
        x = input('Enter the department name:')
        co.execute('update staff set dept="{}" where UserID={}'.format(x, pu))
        print('Department updated successfully.')
        mydb.commit()
    except:
        print('Enter a valid value')
    print("--------------------------------------------")
    
def staff_phoneNum_change():
    """Allows staff to change their phone number."""
    global s
    if not s: return
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        pu = s[0][0] # user id
        x = input('Enter the new phone number:')
        co.execute('update staff set PhoneNum="{}" where UserID={}'.format(x, pu))
        print('Phone number updated successfully.')
        mydb.commit()
    except:
        print('Enter a valid value')
    print("--------------------------------------------")

def staff_address_change():
    """Allows staff to change their address."""
    global s
    if not s: return
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        pu = s[0][0] # user id
        x = input('Enter the new address:')
        co.execute('update staff set Address="{}" where UserID={}'.format(x, pu))
        print('Address updated successfully.')
        mydb.commit()
    except:
        print('Enter a valid value')
    print("--------------------------------------------")

def search_sname():
    """Searches staff by name."""
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        x = input('Enter the staff member name you want to search about:')
        co.execute('select * from staff where UserName like "%{}%"'.format(x))
        a = co.fetchall()
        if len(a) == 0:
            print('No person with this name was found')
        else:
            for i in a: print(i)
    except:
        print('Some error occured')

def search_staff():
    """Searches staff by UserID, Department, Phone No., or Date of Joining."""
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        print('Press 1- search through UserId')
        print('Press 2- search through department')
        print('Press 3- search through phone no.')
        print('Press 4- search through date of joining')
        ckl = int(input("enter your choice:"))
        
        if ckl == 1:
            kkk = int(input("enter userID:"))
            co.execute("select*from staff where UserID={}".format(kkk))
        elif ckl == 2:
            klc = input("enter department:")
            co.execute("select*from staff where Dept='{}'".format(klc))
        elif ckl == 3:
            lll = int(input("enter phone no."))
            co.execute("select*from staff where PhoneNum={}".format(lll))
        elif ckl == 4:
            opo = input("enter date of joining :")
            co.execute("select*from staff where DateOfJoining='{}'".format(opo))
        else:
            print('Invalid choice.')
            return

        result = co.fetchall()
        for i in result: print(i)

    except ValueError:
        print('Invalid input given (expected a number).')
    except:
        print('Enter a valid value')

def roombooking_remove():
    """Removes a room booking record by Booking ID."""
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        print('To remove a record from room booking details')
        ckl = int(input("Enter the booking ID to be removed:"))
        # You would typically also update the 'rooms' status back to 'Vacant' here
        co.execute('delete from roombooking where BookingID={}'.format(ckl))
        print('Record of the room booking has been removed')
        mydb.commit()
    except:
        print('Some error occured')
        
def room_booking_details():
    """Shows room booking details for a given UserID."""
    print('-------------------------------------------------')
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        v = input("enter userid to view booking details:")
        co.execute("select * from roombooking where UserID={} ".format(v))
        a = co.fetchall()
        for i in a: print(i)
        print("details shown")
        mydb.commit()
    except Exception as e:
        print(f"Error fetching room booking details: {e}")
    print('-------------------------------------------------')

def add_dish():
    """Adds a new dish to the menu."""
    print("__________________________________________")
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        p = int(input("enter item number:"))
        k = input("enter item Name:")
        m = int(input("enter price:"))
        h = input("enter category:")
        l = input("enter veg or non-veg:")
        co.execute("insert into menu values({},'{}',{},'{}','{}')".format(p, k, m, h, l))
        print("dish successfully added ")
        mydb.commit()
    except ValueError:
        print('Invalid input given (expected a number for item number/price).')
    except Exception as e:
        print(f"An error occurred while adding dish: {e}")
    print("--------------------------------------------")

def remove_dish():
    """Removes a dish from the menu by Item Number."""
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        o = int(input("Enter item number:"))
        co.execute("delete from menu where ItemNum ={}".format(o))
        print("dish successfully removed")
        mydb.commit()
    except ValueError:
        print('Invalid input given (expected a number for item number).')
    except Exception as e:
        print(f"An error occurred while removing dish: {e}")
    print("--------------------------------------------")

def change_price_dish():
    """Updates the price of a dish."""
    try:
        print("--------------------------------------------------")
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        h = int(input("Enter item number to be updated:"))
        sh = int(input("Enter new price of the dish:"))
        co.execute("update menu set Price={} where ItemNum={}".format(sh, h))
        mydb.commit()
    except ValueError:
        print('Invalid input given (expected a number).')
    except:
        print('Enter a valid value')
    print("--------------------------------------------------")

def change_name_dish():
    """Updates the name of a dish."""
    try:
        print("--------------------------------------------------")
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        h = int(input("Enter item number to be updated:"))
        sh = input("Enter new name of the dish:")
        co.execute("update menu set ItemName='{}' where ItemNum={}".format(sh, h))
        mydb.commit()
    except ValueError:
        print('Invalid input given (expected a number for item number).')
    except:
        print('Enter a valid value')
    print("--------------------------------------------------")
    
def order_details():
    """Displays all order information."""
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        co.execute("select * from order_info ")
        a = co.fetchall()
        for i in a: print(i)
        print("details shown")
        mydb.commit()
    except Exception as e:
        print(f"Error fetching order details: {e}")
    print("--------------------------------------------")

def cancel_booking():
    """Cancels the current user's table booking."""
    global s
    if not s: return
    try:
        print("--------------------------------------------------")
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        pu = s[0][0] # user's id
        co.execute("delete from table_booking where UserID ={}".format(pu))
        print("Booking cancelled.")
        mydb.commit()
    except:
        print('Enter a valid value')
    print("--------------------------------------------")

def book_table():
    """Books a table for the current user."""
    global s
    if not s: return
    try:
        print("--------------------------------------------------")
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        pu = s[0][0] # user's id
        o = int(input("Enter table number to be booked:"))
        p = input("Enter date for which you want to book table (YYYY-MM-DD):")
        l = input("Enter time (HH:MM:SS):")
        co.execute("insert into table_booking values({},{},'{}','{}')".format(o, pu, p, l))
        print("Table booked.")
        mydb.commit()
    except ValueError:
        print('Invalid input given (expected a number for table number).')
    except:
        print('Enter a valid value')
    print("--------------------------------------------")
    
# --- Guest Management Functions (used by Staff) ---
def guest_details():
    """Displays all guest details."""
    print('-------------------------------------------------')
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        co.execute("select * from guests")
        a = co.fetchall()
        for i in a: print(i)
        print("details shown")
        mydb.commit()
    except Exception as e:
        print(f"Error fetching guest details: {e}")
    print('-------------------------------------------------')

def insert_gdetails():
    """Adds a new guest member's details to the 'guests' table."""
    global s
    if not s: return
    try:
        print("--------------------------------------------------")
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        p = s[0][0] # user id
        k = s[0][1] # user name
        h = int(input("Enter phone number:"))
        l = input("Enter address:")
        s_gender = input("Enter gender:")
        w = "GUEST"
        co.execute("insert into guests values({},'{}',{},'{}','{}','{}')".format(p, k, h, l, s_gender, w))
        print("data successfully added to database")
        mydb.commit()
    except ValueError:
        print('Invalid input given (expected a number for phone number).')
    except:
        print('Enter a valid value')
    print("--------------------------------------------------")
    
def remove_gdetails():
    """Removes a guest member's details by UserID."""
    try:
        print("--------------------------------------------")
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        c = int(input("Enter UserID of the guest to remove: "))
        co.execute("delete from guests where UserID ={}".format(c))
        print("data successfully deleted")
        mydb.commit()
    except:
        print('Enter a valid value')
    print("--------------------------------------------")

def guest_name_change():
    """Allows guest to change their name."""
    global s
    if not s: return
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        pu = s[0][0] # user id
        x = input('Enter the new name:')
        co.execute('update users set UserName="{}" where UserID={}'.format(x, pu))
        co.execute('update guests set UserName="{}" where UserID={}'.format(x, pu))
        s[0] = (s[0][0], x, s[0][2], s[0][3]) # Update session variable
        print('Name updated successfully.')
        mydb.commit()
    except:
        print('Enter a valid value')
    print("--------------------------------------------")

def guest_phoneNum_change():
    """Allows guest to change their phone number."""
    global s
    if not s: return
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        pu = s[0][0] # user id
        x = input('Enter the new phone number:')
        co.execute('update guests set PhoneNum="{}" where UserID={}'.format(x, pu))
        print('Phone number updated successfully.')
        mydb.commit()
    except:
        print('Enter a valid value')
    print("--------------------------------------------")

def guest_address_change():
    """Allows guest to change their address."""
    global s
    if not s: return
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        pu = s[0][0] # user id
        x = input('Enter the new address:')
        co.execute('update guests set Address="{}" where UserID={}'.format(x, pu))
        print('Address updated successfully.')
        mydb.commit()
    except:
        print('Enter a valid value')
    print("--------------------------------------------")

def search_gname():
    """Searches guests by name."""
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        x = input('Enter the guest name you want to search about:')
        co.execute('select * from guests where UserName like "%{}%"'.format(x))
        a = co.fetchall()
        for i in a: print(i)
    except:
        print('Some error occured')

def search_guest():
    """Searches guests by UserID, Address, Phone No., or Gender."""
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        print('Press 1- search through UserId')
        print('Press 2- search through Address')
        print('Press 3- search through phone no.')
        print('Press 4- search through gender')
        ckl = int(input("enter your choice:"))
        
        if ckl == 1:
            kkk = int(input("Enter userID:"))
            co.execute("select * from guests where UserID={}".format(kkk))
        elif ckl == 2:
            klc = input("Enter Address:")
            co.execute("select * from guests where Address='{}'".format(klc))
        elif ckl == 3:
            lll = int(input("Enter phone no."))
            co.execute("select * from guests where PhoneNum={}".format(lll))
        elif ckl == 4:
            opo = input("Enter Gender:")
            co.execute("select * from guests where Gender='{}'".format(opo))
        else:
            print('Invalid choice.')
            return

        result = co.fetchall()
        for i in result: print(i)

    except ValueError:
        print('Invalid input given (expected a number).')
    except:
        print('Enter a valid value')

# --- About Hotel Text ---
xk = ''' Welcome to TAJ HOTEL, where nature meets luxury in perfect harmony.
Nestled in a serene and picturesque location, TAJ HOTEL offers an unforgettable escape surrounded by breathtaking landscapes and tranquil surroundings.
Whether you’re here to unwind, explore, or indulge in world-class amenities, our hotel provides the ideal setting for relaxation and rejuvenation.
Step outside and be embraced by the beauty of nature — lush gardens, panoramic views, and the soothing sounds of nature create a peaceful oasis right at your doorstep.
Our expertly landscaped grounds are perfect for a leisurely stroll, while nearby hiking trails and scenic spots allow you to connect with the great outdoors.
Inside, our modern, yet cozy accommodations provide a warm and inviting atmosphere, designed to complement the natural beauty that surrounds us.
Large windows offer stunning views of the landscape, bringing the outside in and filling every room with light and fresh air.
From sunrise to sunset, TAJ HOTEL offers a serene escape that blends the comfort of luxury with the peace of nature.
Come experience an environment that nurtures your soul and rejuvenates your spirit.
Whether you’re visiting for a weekend get away or a longer stay, we promise that every moment spent here will be a tranquil retreat from the everyday hustle.
'''

# --- Main Application Logic ---

if __name__ == "__main__":
    
    # 1. Login/Sign-in Loop
    try:
        while True:
            print('-------------------------------------------------')
            print('Press 1- Login')
            print('Press 2- Sign in')
            print('Press 3- About hotel')
            print('-------------------------------------------------')
            
            try:
                choose = int(input("Enter your choice: "))
            except ValueError:
                print('Invalid input given (expected a number).')
                continue
                
            if choose == 1:
                s_result = login()
                if s_result:
                    s = s_result
                    print('Login successful.')
                    break
                else:
                    print('Login failed. Please try again.')
                    
            elif choose == 3:
                print(xk)
                
            elif choose == 2: # sign in
                print("--------------------------------------------------")
                try:
                    mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
                    co = mydb.cursor()
                except m.Error as err:
                    print(f"Database connection error: {err}")
                    continue

                print('''Don't have any account. Please create an account.''')
                co.execute('select * from users')
                f = co.fetchall()
                # Determine next User ID (assuming sequential)
                a = f[-1][0] + 1 if f else 1 
                print('Your user id is', a)
                
                x = input("Enter user name:")
                y = int(input("New password:"))
                z = int(input("Confirm password:"))
                
                if y != z:
                    print('wrong password has been given for confirmation')
                    print("Enter correct password")
                    z = int(input("Confirm password:"))
                    
                w = input('Enter your identity (Guest/Staff): ')
                
                # Insert into users (UserID, UserName, Password, UserType)
                co.execute("insert into users values({},'{}',{},'{}')".format(a, x, z, w.lower()))
                
                l = input("Enter address:")
                m_phone = int(input("Enter Phone number:"))
                n = input("Enter your gender:")
                k = w.strip().upper()
                
                if k == 'GUEST':
                    # Insert into guests (User_ID, User_name, phone_number, address, Gender, User_Type)
                    co.execute("insert into guests values({},'{}',{},'{}','{}','{}')".format(a, x, m_phone, l, n, 'Guest'))
                elif k == 'STAFF':
                    rt = input("Enter your department:")
                    ty = input("Enter date of joining (YYYY-MM-DD):")
                    # Insert into staff (User_Id, User_name, dept, phone_number, DateOfJoining, address, Gender, User_type)
                    co.execute("insert into staff values({},'{}','{}',{},'{}','{}','{}','{}')".format(a, x, rt, m_phone, ty, l, n, 'Staff'))
                    
                mydb.commit()
                
                print('Your account was created')
                s = [(a, x, z, k)]
                print("login successful.")
                print('You have logged in through the account created now')
                print("--------------------------------------------------")
                break

            else:
                print('Invalid choice. Please enter 1, 2, or 3.')
                
    except Exception as e:
        print(f"An error occurred in the main login loop: {e}")

    # 2. Main Menu Loop (Guest or Staff)
    if s and len(s) > 0:
        hy = s[0][3].upper().strip() # User_Type from 's' variable
        
        if 'GUEST' in hy:
            while True:
                print('-------------------------------------------------')
                print('Press 1- Lodging Room')
                print('Press 2- Restaurant')
                print('Press 3- Exit')
                print('-------------------------------------------------')
                
                try:
                    c = int(input("Enter your choice: "))
                    
                    if c == 1: # Lodging Room
                        # Lodging Room submenu
                        while True:
                            print('-------------------------------------------------')
                            print('Lodging room')
                            print("Press 1- Room details")
                            print('Press 2- Room booking')
                            print('Press 3- Exit')
                            print('-------------------------------------------------')
                            
                            ch = int(input("Enter your choice: "))
                            
                            if ch == 1:
                                room_details()
                                print("Press 1- Room booking")
                                print('Press 2- Skip')
                                cfr = int(input("Enter your choice: "))
                                if cfr == 1:
                                    room_booking(s)
                                elif cfr == 2:
                                    pass
                                
                            elif ch == 2:
                                room_booking(s)
                                
                            elif ch == 3:
                                break
                            else:
                                print('Give required input')
                                
                            print('-------------------------------------------------')
                            print("Press 1- Feedback")
                            print('Press 2- Skip')
                            kk = int(input("Enter your choice: "))
                            if kk == 1:
                                feedback()
                            elif kk == 2:
                                pass
                            print('-------------------------------------------------')
                            break # Exit the inner Lodging menu loop

                    elif c == 2: # Restaurant
                        # Restaurant submenu
                        while True:
                            print('Welcome to our restaurant')
                            print('Press 1- Menu')
                            print('Press 2- Order')
                            print('Press 3- Table booking')
                            print('Press 4- Exit')
                            
                            ci = int(input('Enter your choice:'))
                            
                            if ci == 1:
                                menu()
                            elif ci == 2:
                                order()
                            elif ci == 3:
                                table_booking()
                            elif ci == 4:
                                break
                            else:
                                print('Give required input')
                                
                            print('-------------------------------------------------')
                            print("Press 1- Feedback")
                            print('Press 2- Skip')
                            kk = int(input("Enter your choice: "))
                            if kk == 1:
                                feedback()
                                break
                            elif kk == 2:
                                pass
                            print('-------------------------------------------------')
                            break # Exit the inner Restaurant menu loop
                            
                    elif c == 3:
                        break
                    else:
                        print('Give required input')
                        
                except ValueError:
                    print('Invalid input given (expected a number).')

        elif 'STAFF' in hy:
            while True:
                print("--------------------------------------------")
                print("press 1 for Staff details")
                print("press 2 for Guest details")
                print("press 3 for Lodging room details")
                print("press 4 for Restaurant management")
                print("--------------------------------------------")
                
                try:
                    ap = int(input("Enter your choice:"))
                    
                    if ap == 1: # Staff details
                        while True:
                            print("--------------------------------------------")
                            print("****Staff details****")
                            print("press 1 to show staff details")
                            print("press 2 to update staff details")
                            print("press 3 to search staff details")
                            print("press 4 to exit")
                            print("--------------------------------------------")
                            
                            pp = int(input("Enter your choice:"))
                            
                            if pp == 1:
                                print("--------------------------------------------------")
                                mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
                                co = mydb.cursor()
                                co.execute('select * from staff')
                                x = co.fetchall()
                                for i in x: print(i)
                                mydb.commit()
                                print("--------------------------------------------------")
                                
                            elif pp == 2: # update staff details
                                while True:
                                    print("--------------------------------------------")
                                    print("press 1 to Add details of a new staff person")
                                    print("press 2 to Remove details of an old staff person")
                                    print("press 3 to change any of the following data:(staff person name, department, phone no., address)")
                                    print("press 4 to exit")
                                    print("--------------------------------------------")
                                    
                                    zl = int(input("Enter your choice:"))
                                    
                                    if zl == 1:
                                        insert_sdetails()
                                    elif zl == 2:
                                        remove_sdetails()
                                    elif zl == 3: # Change details
                                        print("--------------------------------------------")
                                        print("press 1 to change staff member name")
                                        print("press 2 to change department")
                                        print("press 3 to change phone no.")
                                        print("press 4 to change address")
                                        print("press 5 to exit")
                                        print("--------------------------------------------")
                                        
                                        oj = int(input("Enter your choice:"))
                                        
                                        if oj == 1: staff_name_change()
                                        elif oj == 2: staff_department_change()
                                        elif oj == 3: staff_phoneNum_change()
                                        elif oj == 4: staff_address_change()
                                        elif oj == 5: break
                                        else: print('Give required input')
                                            
                                    elif zl == 4: break
                                    else: print('Give required input')

                            elif pp == 3: # search staff details
                                while True:
                                    print("--------------------------------------------")
                                    print("****staff details****")
                                    print("press 1 to search staff names")
                                    print("press 2 to search details of a staff member by the description you will choose (user id, dept, phone, date_of_joining, address):")
                                    print("press 3 to exit")
                                    print("--------------------------------------------")
                                    
                                    hfg = int(input("Enter your choice:"))
                                    
                                    if hfg == 1: search_sname()
                                    elif hfg == 2: search_staff()
                                    elif hfg == 3: break
                                    else: print('Give required input')
                                
                            elif pp == 4: break
                            else: print('Give required input')
                            
                            break # Exit inner Staff details loop

                    elif ap == 2: # Guest details
                        while True:
                            print("--------------------------------------------")
                            print("****Guest details****")
                            print("press 1 to show guest details")
                            print("press 2 to update guest details")
                            print("press 3 to search guest details")
                            print("press 4 to exit")
                            print("--------------------------------------------")
                            
                            oo = int(input("Enter your choice:"))
                            
                            if oo == 1: guest_details()
                            
                            elif oo == 2: # update guest details
                                while True:
                                    print("--------------------------------------------")
                                    print("press 1 to Add details of a new guest")
                                    print("press 2 to Remove details of an old guest")
                                    print("press 3 to change any of the following data:(guest address, , phone no., user id)")
                                    print("press 4 to exit")
                                    print("--------------------------------------------")
                                    
                                    zl = int(input("Enter your choice:"))
                                    
                                    if zl == 1: insert_gdetails()
                                    elif zl == 2: remove_gdetails()
                                    elif zl == 3: # Change details
                                        print("--------------------------------------------")
                                        print("print 1 to change guest name")
                                        print("print 2 to change phone no.")
                                        print("print 3 to change address")
                                        print("press 4 to exit")
                                        print("--------------------------------------------")
                                        
                                        oj = int(input("Enter your choice:"))
                                        
                                        if oj == 1: guest_name_change()
                                        elif oj == 2: guest_phoneNum_change()
                                        elif oj == 3: guest_address_change()
                                        elif oj == 4: break
                                        else: print('Give required input')
                                            
                                    elif zl == 4: break
                                    else: print('Give required input')

                            elif oo == 3: # search guest details
                                while True:
                                    print("--------------------------------------------")
                                    print("press 1 to search guest names")
                                    print("press 2 to search details of a guest member by the description you will choose (user id, dept, phone, date_of_joining, address):")
                                    print("press 3 to exit")
                                    print("--------------------------------------------")
                                    
                                    hfg = int(input("Enter your choice:"))
                                    
                                    if hfg == 1: search_gname()
                                    elif hfg == 2: search_guest()
                                    elif hfg == 3: break
                                    else: print('Give required input')
                                    
                            elif oo == 4: break
                            else: print('Give required input')

                        break # Exit inner Guest details loop

                    elif ap == 3: # Lodging room details
                        while True:
                            print("--------------------------------------------")
                            print("------Lodging room details-------")
                            print("press 1 to show room booking details")
                            print("press 2 to remove details of a room booking")
                            print("press 3 to exit")
                            
                            op = int(input("Enter your choice:"))
                            if op == 1:
                                room_details()
                                room_booking_details()
                            elif op == 2:
                                roombooking_remove()
                            elif op == 3:
                                break
                            else:
                                print('Give required input')
                            break

                    elif ap == 4: # Restaurant management
                        while True:
                            print("--------------------------------------------")
                            print("------Restaurant management-------")
                            print("press 1 for modifications in menu")
                            print("press 2 for modifications in order")
                            print("press 3 for modifications in table booking")
                            print("press 4 to exit")
                            print("--------------------------------------------")
                            
                            vv = int(input("Enter your choice:"))
                            
                            if vv == 1: # modifications in menu
                                while True:
                                    menu()
                                    print("press 1 to add dish into menu")
                                    print("press 2 to remove dish from menu")
                                    print("press 3 to change price of any item")
                                    print("press 4 to change name of any item")
                                    print("press 5 for Exit")
                                    
                                    vqa = int(input("Enter your choice:"))
                                    
                                    if vqa == 1: add_dish()
                                    elif vqa == 2: remove_dish()
                                    elif vqa == 3: change_price_dish()
                                    elif vqa == 4: change_name_dish()
                                    elif vqa == 5: break
                                    else: print('Give required input')

                            elif vv == 2: # modifications in order
                                print("press 1 for order details")
                                print("press 2 for Exit")
                                om = int(input("Enter your choice:"))
                                if om == 1: order_details()
                                elif om == 2: break
                                else: print('Give required input')
                                    
                            elif vv == 3: # modifications in table booking
                                print("press 1 to cancel table booking")
                                print("press 2 to book a table")
                                print("press 3 for Exit")
                                kl = int(input("enter your choice"))
                                if kl == 1: cancel_booking()
                                elif kl == 2: book_table()
                                elif kl == 3: break
                                else: print('Give required input')

                            elif vv == 4: break
                            else: print('Give required input')
                            
                            break # Exit inner Restaurant management loop
                    
                    else:
                        print('Give required input')
                        
                except ValueError:
                    print('Invalid input given (expected a number).')
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    
                break

    # Final closing message
    print('successfully visited')
    print('''
+++++++++++++++++++++++++++++++++++++++++++
  
*****************THANKS FOR VISITING********************
  
+++++++++++++++++++++++++++++++++++++++++++
 
''')
