# importing modules
import mysql.connector as m
# The 's' variable will store user details after successful login/sign-in.
# NOTE: The variable 's' is now only managed in the main application logic,
# and is passed as an argument to functions where needed.

def login():
    """Handles user login."""
    print('-------------------------------------------------')
    user_id = int(input("Enter your user ID:"))
    user_name = input("Enter user name:")
    password = int(input("Enter your password:"))
    
    # Connect to the database (hardcoded credentials as per the project)
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    
    # Check credentials
    co.execute("select * from users")
    user_records = co.fetchall()
    jl = 5
    s_result = [] # Initialize s_result
    
    for record in user_records:
        # Check if Name (record[1]), Password (record[2]), and ID (record[0]) match the input
        if user_name == record[1] and str(password) == str(record[2]) and user_id == record[0]:
            jl = 6
            print("login successful.")
            co.execute('select * from users where UserID={} and UserName="{}" and Password={}'.format(user_id, user_name, password))
            s_result = co.fetchall()
            break
            
    if jl == 5:
        print("wrong details given")
        
    mydb.commit()
    print('-------------------------------------------------')
    return s_result # Return the user details

def room_booking(user_details):
    """Handles room booking process. Takes user_details (s) as argument."""
    print('-------------------------------------------------')
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    co.execute('select * from roombooking ')
    booking_records = co.fetchall()
    
    room_num_input = int(input("Enter your selected Room Number: "))
    
    # Logic to generate next Booking ID
    booking_id = booking_records[-1][1] + 1 if booking_records else 1001
    print("Your Booking ID is", booking_id)
    
    u_id = user_details[0][0] # user's id
    u_name = user_details[0][1] # user's name
    address = input("Enter Address: ")
    phone_num = int(input("Enter Phone number:"))
    check_in_date = input('Enter check in date (YYYY-MM-DD):')
    check_out_date = input('Enter check out date (YYYY-MM-DD):')
    gender = input('Enter your gender: ')
    
    co.execute('select RoomNum, Status from rooms')
    room_statuses = co.fetchall()
    valid_room_numbers = [room_record[0] for room_record in room_statuses]
    booked = False
    
    for room_record in room_statuses:
        room_num_db = room_record[0]
        status = room_record[1].strip().capitalize()
        
        if room_num_db == room_num_input:
            if status == 'Vacant':
                # Insert into roombooking (Room_Num, Booking_ID, User_ID, User_Name, Address, Phone_Num, CheckIn, Cheak Out, Gender)
                co.execute("insert into roombooking values({},{},{},'{}','{}',{},'{}','{}','{}')".format(room_num_input, booking_id, u_id, u_name, address, phone_num, check_in_date, check_out_date, gender))
                # Update room status to Occupied
                co.execute("update rooms set Status='{}' where RoomNum={}".format('Occupied', room_num_input))
                print('Room booked.')
                booked = True
                break
            elif status == 'Occupied':
                print('''Room chosen is already booked by someone.
Please choose another room. ''')
                booked = True
                break
    
    if room_num_input not in valid_room_numbers and not booked:
        print('Entered room number does not exist.')
        
    mydb.commit()
    print('-------------------------------------------------')

def room_details():
    """Displays all room details from the 'rooms' table."""
    print('-------------------------------------------------')
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    co.execute('select * from rooms')
    room_records = co.fetchall()
    for record in room_records:
        print(record)
    mydb.commit()
    print('-------------------------------------------------')

def menu():
    """Displays the restaurant menu."""
    print('-------------------------------------------------')
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    print("*****MENU*****")
    print('item_number, item_name, price, category, availability')
    co.execute('select * from menu')
    menu_records = co.fetchall()
    for record in menu_records:
        print(record)
    mydb.commit()
    print('-------------------------------------------------')

def order(user_details):
    """Handles the food ordering process. Takes user_details (s) as argument."""
    if not user_details:
        print("Please log in or sign up first.")
        return

    print('-------------------------------------------------')
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    u_id = user_details[0][0] # user id
    
    # Determine the table number (Logic updated to check booking or ask)
    co.execute('select TableNum from table_booking where UserID = {} ORDER BY Date DESC, Time DESC LIMIT 1'.format(u_id))
    table_result = co.fetchone()
    
    if table_result:
        table_num = table_result[0]
        print("Your Table Number is", table_num)
    else:
        table_num = int(input("Enter your Table Number (must be already booked/assigned): "))

    co.execute('select * from order_info')
    order_info_records = co.fetchall()
    
    # Generate next Order Number
    order_num = len(order_info_records) + 1 
    
    co.execute('select * from menu')
    menu_dishes = co.fetchall() # all dishes
    
    distinct_items_count = int(input("Enter no. of distinct items to be ordered: "))
    total_amount = 0 # Total amount
    
    for i in range(distinct_items_count):
        item_num_input = int(input("Enter the item number to be ordered: "))
        quantity = int(input("Enter the quantity of above item to be ordered: "))
        
        item_found = False
        for dish in menu_dishes:
            if item_num_input == dish[0]: # ItemNum matches
                price = dish[2] # price of a dish
                subtotal = price * quantity # subtotal
                
                # Insert into order_details (OrderNum, ItemNum, Quantity, Subtotal)
                co.execute('insert into order_details values({},{},{},{})'.format(order_num, item_num_input, quantity, subtotal))
                total_amount = total_amount + subtotal
                item_found = True
                break
        
        if not item_found:
            print(f"Item number {item_num_input} not found in menu. Skipping.")
            
    # Insert into order_info (OrderNum, User_ID, Table_Num, Total_Amount)
    co.execute('insert into order_info values({},{},{},{})'.format(order_num, u_id, table_num, total_amount))
    
    mydb.commit()
    print('Your order has been placed. Total Amount: {}'.format(total_amount))
    print('-------------------------------------------------')

def table_booking(user_details):
    """Handles restaurant table booking. Takes user_details (s) as argument."""
    if not user_details:
        print("Please log in or sign up first.")
        return

    print('-------------------------------------------------')
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    
    table_num = int(input('Enter Table number:'))
    u_id = user_details[0][0] # user id
    date_booked = input('Enter date booked (YYYY-MM-DD): ')
    time_booked = input('Enter time booked (HH:MM:SS): ')
    
    # Insert into table_booking (TableNum, User_ID, Date, Time)
    co.execute('insert into table_booking values({},{},"{}","{}")'.format(table_num, u_id, date_booked, time_booked))
    print('Table booked.')
    mydb.commit()
    print('-------------------------------------------------')

def feedback(user_details):
    """Handles the user feedback submission. Takes user_details (s) as argument."""
    if not user_details:
        print("Please log in or sign up first.")
        return

    print('-------------------------------------------------')
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    
    user_id = user_details[0][0] 
    user_name = user_details[0][1]
    
    # Get next Feedback ID
    co.execute('SELECT FeedbackID FROM feedback ORDER BY FeedbackID DESC LIMIT 1')
    last_id = co.fetchone()
    feedback_id = last_id[0] + 1 if last_id else 1 
    
    print("Your Feedback ID is", feedback_id)
    
    comment_text = input("Enter your feedback/comment: ")
    rating_score = int(input("Enter a rating (1-5, 5 being best): "))
    
    if not 1 <= rating_score <= 5:
        print("Rating must be between 1 and 5. Please try again.")
        return

    # Insert into feedback (FeedbackID, UserID, UserName, Comment, Rating)
    # Note: You need a 'feedback' table in your database for this to work.
    co.execute("insert into feedback values({},{},'{}','{}',{})".format(feedback_id, user_id, user_name, comment_text, rating_score))
    
    mydb.commit()
    print('Thank you! Your feedback has been recorded.')
    print('-------------------------------------------------')
    
# --- Staff Management Functions ---

def insert_sdetails(user_details):
    """Adds a new staff member's details to the 'staff' table. Takes user_details (s) as argument."""
    if not user_details:
        print("Please log in or sign up first.")
        return

    print("--------------------------------------------------")
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    
    u_id = user_details[0][0] # user id (from current session)
    u_name = user_details[0][1] # user name (from current session)
    department = input("Enter department:")
    phone_num = int(input("Enter phone number:"))
    doj = input("Enter date of joining (YYYY-MM-DD):")
    address = input("Enter address:")
    gender = input("Enter gender:")
    user_type = "STAFF"
    
    # Insert into staff (User_Id, User_name, dept, phone_number, DateOfJoining, address, Gender, User_type)
    co.execute("insert into staff values({},'{}','{}',{},'{}','{}','{}','{}')".format(u_id, u_name, department, phone_num, doj, address, gender, user_type))
    print("data successfully inserted")
    mydb.commit()
    print("--------------------------------------------------")

def remove_sdetails():
    """Removes a staff member's details by UserID."""
    print("_______________________________________")
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    staff_id_to_remove = int(input("Enter UserID of the staff member to remove: ")) 
    co.execute("delete from staff where UserID ={}".format(staff_id_to_remove))
    print("data successfully removed")
    mydb.commit()
    print("________________________________________________")
    
def staff_name_change(user_details):
    """Allows staff to change their name. Returns updated user_details."""
    if not user_details: return user_details
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    user_id = user_details[0][0] # user id
    new_name = input('Enter the new name:')
    co.execute('update users set UserName="{}" where UserID={}'.format(new_name, user_id))
    co.execute('update staff set UserName="{}" where UserID={}'.format(new_name, user_id))
    
    # Update session variable to be returned
    updated_details = list(user_details[0])
    updated_details[1] = new_name
    updated_s = [tuple(updated_details)]
    
    print('Name updated successfully.')
    mydb.commit()
    print("--------------------------------------------")
    return updated_s

def staff_department_change(user_details):
    """Allows staff to change their department."""
    if not user_details: return
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    user_id = user_details[0][0] # user id
    new_department = input('Enter the department name:')
    co.execute('update staff set dept="{}" where UserID={}'.format(new_department, user_id))
    print('Department updated successfully.')
    mydb.commit()
    print("--------------------------------------------")
    
def staff_phoneNum_change(user_details):
    """Allows staff to change their phone number."""
    if not user_details: return
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    user_id = user_details[0][0] # user id
    new_phone = input('Enter the new phone number:')
    co.execute('update staff set PhoneNum="{}" where UserID={}'.format(new_phone, user_id))
    print('Phone number updated successfully.')
    mydb.commit()
    print("--------------------------------------------")

def staff_address_change(user_details):
    """Allows staff to change their address."""
    if not user_details: return
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    user_id = user_details[0][0] # user id
    new_address = input('Enter the new address:')
    co.execute('update staff set Address="{}" where UserID={}'.format(new_address, user_id))
    print('Address updated successfully.')
    mydb.commit()
    print("--------------------------------------------")

def search_sname():
    """Searches staff by name."""
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    search_name = input('Enter the staff member name you want to search about:')
    co.execute('select * from staff where UserName like "%{}%"'.format(search_name))
    search_results = co.fetchall()
    if len(search_results) == 0:
        print('No person with this name was found')
    else:
        for record in search_results: print(record)

def search_staff():
    """Searches staff by UserID, Department, Phone No., or Date of Joining."""
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    print('Press 1- search through UserId')
    print('Press 2- search through department')
    print('Press 3- search through phone no.')
    print('Press 4- search through date of joining')
    ckl = int(input("enter your choice:"))
    
    if ckl == 1:
        user_id_search = int(input("enter userID:"))
        co.execute("select*from staff where UserID={}".format(user_id_search))
    elif ckl == 2:
        dept_search = input("enter department:")
        co.execute("select*from staff where Dept='{}'".format(dept_search))
    elif ckl == 3:
        phone_search = int(input("enter phone no."))
        co.execute("select*from staff where PhoneNum={}".format(phone_search))
    elif ckl == 4:
        doj_search = input("enter date of joining :")
        co.execute("select*from staff where DateOfJoining='{}'".format(doj_search))
    else:
        print('Invalid choice.')
        return

    result = co.fetchall()
    for record in result: print(record)

def roombooking_remove():
    """Removes a room booking record by Booking ID."""
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    print('To remove a record from room booking details')
    booking_id_to_remove = int(input("Enter the booking ID to be removed:"))
    # You would typically also update the 'rooms' status back to 'Vacant' here
    co.execute('delete from roombooking where BookingID={}'.format(booking_id_to_remove))
    print('Record of the room booking has been removed')
    mydb.commit()
        
def room_booking_details():
    """Shows room booking details for a given UserID."""
    print('-------------------------------------------------')
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    search_user_id = input("enter userid to view booking details:")
    co.execute("select * from roombooking where UserID={} ".format(search_user_id))
    results = co.fetchall()
    for record in results: print(record)
    print("details shown")
    mydb.commit()
    print('-------------------------------------------------')

def add_dish():
    """Adds a new dish to the menu."""
    print("__________________________________________")
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    item_num = int(input("enter item number:"))
    item_name = input("enter item Name:")
    price = int(input("enter price:"))
    category = input("enter category:")
    veg_nonveg = input("enter veg or non-veg:")
    co.execute("insert into menu values({},'{}',{},'{}','{}')".format(item_num, item_name, price, category, veg_nonveg))
    print("dish successfully added ")
    mydb.commit()
    print("--------------------------------------------")

def remove_dish():
    """Removes a dish from the menu by Item Number."""
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    item_num_to_remove = int(input("Enter item number:"))
    co.execute("delete from menu where ItemNum ={}".format(item_num_to_remove))
    print("dish successfully removed")
    mydb.commit()
    print("--------------------------------------------")

def change_price_dish():
    """Updates the price of a dish."""
    print("--------------------------------------------------")
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    item_num = int(input("Enter item number to be updated:"))
    new_price = int(input("Enter new price of the dish:"))
    co.execute("update menu set Price={} where ItemNum={}".format(new_price, item_num))
    mydb.commit()
    print("--------------------------------------------------")

def change_name_dish():
    """Updates the name of a dish."""
    print("--------------------------------------------------")
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    item_num = int(input("Enter item number to be updated:"))
    new_name = input("Enter new name of the dish:")
    co.execute("update menu set ItemName='{}' where ItemNum={}".format(new_name, item_num))
    mydb.commit()
    print("--------------------------------------------------")
    
def order_details():
    """Displays all order information."""
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    co.execute("select * from order_info ")
    results = co.fetchall()
    for record in results: print(record)
    print("details shown")
    mydb.commit()
    print("--------------------------------------------")

def cancel_booking(user_details):
    """Cancels the current user's table booking."""
    if not user_details: return
    print("--------------------------------------------------")
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    u_id = user_details[0][0] # user's id
    co.execute("delete from table_booking where UserID ={}".format(u_id))
    print("Booking cancelled.")
    mydb.commit()
    print("--------------------------------------------")

def book_table(user_details):
    """Books a table for the current user."""
    if not user_details: return
    print("--------------------------------------------------")
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    u_id = user_details[0][0] # user's id
    table_num = int(input("Enter table number to be booked:"))
    date_booked = input("Enter date for which you want to book table (YYYY-MM-DD):")
    time_booked = input("Enter time (HH:MM:SS):")
    co.execute("insert into table_booking values({},{},'{}','{}')".format(table_num, u_id, date_booked, time_booked))
    print("Table booked.")
    mydb.commit()
    print("--------------------------------------------")
    
# --- Guest Management Functions (used by Staff) ---
def guest_details():
    """Displays all guest details."""
    print('-------------------------------------------------')
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    co.execute("select * from guests")
    results = co.fetchall()
    for record in results: print(record)
    print("details shown")
    mydb.commit()
    print('-------------------------------------------------')

def insert_gdetails(user_details):
    """Adds a new guest member's details to the 'guests' table. Takes user_details (s) as argument."""
    if not user_details: return
    print("--------------------------------------------------")
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    u_id = user_details[0][0] # user id
    u_name = user_details[0][1] # user name
    phone_num = int(input("Enter phone number:"))
    address = input("Enter address:")
    gender = input("Enter gender:")
    user_type = "GUEST"
    co.execute("insert into guests values({},'{}',{},'{}','{}','{}')".format(u_id, u_name, phone_num, address, gender, user_type))
    print("data successfully added to database")
    mydb.commit()
    print("--------------------------------------------------")
    
def remove_gdetails():
    """Removes a guest member's details by UserID."""
    print("--------------------------------------------")
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    guest_id_to_remove = int(input("Enter UserID of the guest to remove: "))
    co.execute("delete from guests where UserID ={}".format(guest_id_to_remove))
    print("data successfully deleted")
    mydb.commit()
    print("--------------------------------------------")

def guest_name_change(user_details):
    """Allows guest to change their name. Returns updated user_details."""
    if not user_details: return user_details
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    user_id = user_details[0][0] # user id
    new_name = input('Enter the new name:')
    co.execute('update users set UserName="{}" where UserID={}'.format(new_name, user_id))
    co.execute('update guests set UserName="{}" where UserID={}'.format(new_name, user_id))
    
    # Update session variable to be returned
    updated_details = list(user_details[0])
    updated_details[1] = new_name
    updated_s = [tuple(updated_details)]
    
    print('Name updated successfully.')
    mydb.commit()
    print("--------------------------------------------")
    return updated_s

def guest_phoneNum_change(user_details):
    """Allows guest to change their phone number."""
    if not user_details: return
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    user_id = user_details[0][0] # user id
    new_phone = input('Enter the new phone number:')
    co.execute('update guests set PhoneNum="{}" where UserID={}'.format(new_phone, user_id))
    print('Phone number updated successfully.')
    mydb.commit()
    print("--------------------------------------------")

def guest_address_change(user_details):
    """Allows guest to change their address."""
    if not user_details: return
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    user_id = user_details[0][0] # user id
    new_address = input('Enter the new address:')
    co.execute('update guests set Address="{}" where UserID={}'.format(new_address, user_id))
    print('Address updated successfully.')
    mydb.commit()
    print("--------------------------------------------")

def search_gname():
    """Searches guests by name."""
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    search_name = input('Enter the guest name you want to search about:')
    co.execute('select * from guests where UserName like "%{}%"'.format(search_name))
    results = co.fetchall()
    for record in results: print(record)

def search_guest():
    """Searches guests by UserID, Address, Phone No., or Gender."""
    mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    print('Press 1- search through UserId')
    print('Press 2- search through Address')
    print('Press 3- search through phone no.')
    print('Press 4- search through gender')
    ckl = int(input("enter your choice:"))
    
    if ckl == 1:
        user_id_search = int(input("Enter userID:"))
        co.execute("select * from guests where UserID={}".format(user_id_search))
    elif ckl == 2:
        address_search = input("Enter Address:")
        co.execute("select * from guests where Address='{}'".format(address_search))
    elif ckl == 3:
        phone_search = int(input("Enter phone no."))
        co.execute("select * from guests where PhoneNum={}".format(phone_search))
    elif ckl == 4:
        gender_search = input("Enter Gender:")
        co.execute("select * from guests where Gender='{}'".format(gender_search))
    else:
        print('Invalid choice.')
        return

    result = co.fetchall()
    for record in result: print(record)

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
    
    s = [] # User details variable, locally maintained

    # 1. Login/Sign-in Loop
    while True:
        print('-------------------------------------------------')
        print('Press 1- Login')
        print('Press 2- Sign in')
        print('Press 3- About hotel')
        print('-------------------------------------------------')
        
        choose = int(input("Enter your choice: "))
            
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
            mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
            co = mydb.cursor()

            print('''Don't have any account. Please create an account.''')
            co.execute('select * from users')
            user_records = co.fetchall()
            # Determine next User ID (assuming sequential)
            new_user_id = user_records[-1][0] + 1 if user_records else 1 
            print('Your user id is', new_user_id)
            
            new_user_name = input("Enter user name:")
            new_password = int(input("New password:"))
            confirm_password = int(input("Confirm password:"))
            
            if new_password != confirm_password:
                print('wrong password has been given for confirmation')
                print("Enter correct password")
                confirm_password = int(input("Confirm password:"))
                
            user_identity = input('Enter your identity (Guest/Staff): ')
            
            # Insert into users (UserID, UserName, Password, UserType)
            co.execute("insert into users values({},'{}',{},'{}')".format(new_user_id, new_user_name, confirm_password, user_identity.lower()))
            
            address = input("Enter address:")
            phone_num = int(input("Enter Phone number:"))
            gender = input("Enter your gender:")
            user_type_upper = user_identity.strip().upper()
            
            if user_type_upper == 'GUEST':
                # Insert into guests (User_ID, User_name, phone_number, address, Gender, User_Type)
                co.execute("insert into guests values({},'{}',{},'{}','{}','{}')".format(new_user_id, new_user_name, phone_num, address, gender, 'Guest'))
            elif user_type_upper == 'STAFF':
                department = input("Enter your department:")
                doj = input("Enter date of joining (YYYY-MM-DD):")
                # Insert into staff (User_Id, User_name, dept, phone_number, DateOfJoining, address, Gender, User_type)
                co.execute("insert into staff values({},'{}','{}',{},'{}','{}','{}','{}')".format(new_user_id, new_user_name, department, phone_num, doj, address, gender, 'Staff'))
                
            mydb.commit()
            
            print('Your account was created')
            s = [(new_user_id, new_user_name, confirm_password, user_type_upper)]
            print("login successful.")
            print('You have logged in through the account created now')
            print("--------------------------------------------------")
            break

        else:
            print('Invalid choice. Please enter 1, 2, or 3.')
                

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
                            feedback(s)
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
                            order(s)
                        elif ci == 3:
                            table_booking(s)
                        elif ci == 4:
                            break
                        else:
                            print('Give required input')
                            
                        print('-------------------------------------------------')
                        print("Press 1- Feedback")
                        print('Press 2- Skip')
                        kk = int(input("Enter your choice: "))
                        if kk == 1:
                            feedback(s)
                            break
                        elif kk == 2:
                            pass
                        print('-------------------------------------------------')
                        break # Exit the inner Restaurant menu loop
                        
                elif c == 3:
                    break
                else:
                    print('Give required input')
                        
        elif 'STAFF' in hy:
            while True:
                print("--------------------------------------------")
                print("press 1 for Staff details")
                print("press 2 for Guest details")
                print("press 3 for Lodging room details")
                print("press 4 for Restaurant management")
                print("press 5 to Exit")
                print("--------------------------------------------")
                
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
                            mydb = m.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
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
                                    insert_sdetails(s)
                                elif zl == 2:
                                    remove_sdetails()
                                elif zl == 3: # Change details
                                    while True:
                                        print("--------------------------------------------")
                                        print("press 1 to change staff member name")
                                        print("press 2 to change department")
                                        print("press 3 to change phone no.")
                                        print("press 4 to change address")
                                        print("press 5 to exit")
                                        print("--------------------------------------------")
                                        
                                        oj = int(input("Enter your choice:"))
                                        
                                        if oj == 1: 
                                            s = staff_name_change(s) # Update s with new details
                                        elif oj == 2: staff_department_change(s)
                                        elif oj == 3: staff_phoneNum_change(s)
                                        elif oj == 4: staff_address_change(s)
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
                                
                                if zl == 1: insert_gdetails(s)
                                elif zl == 2: remove_gdetails()
                                elif zl == 3: # Change details
                                    while True:
                                        print("--------------------------------------------")
                                        print("print 1 to change guest name")
                                        print("print 2 to change phone no.")
                                        print("print 3 to change address")
                                        print("press 4 to exit")
                                        print("--------------------------------------------")
                                        
                                        oj = int(input("Enter your choice:"))
                                        
                                        if oj == 1: 
                                            s = guest_name_change(s) # Update s with new details
                                        elif oj == 2: guest_phoneNum_change(s)
                                        elif oj == 3: guest_address_change(s)
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
                            if kl == 1: cancel_booking(s)
                            elif kl == 2: book_table(s)
                            elif kl == 3: break
                            else: print('Give required input')

                        elif vv == 4: break
                        else: print('Give required input')
                        
                elif ap == 5:
                    break
                
                else:
                    print('Give required input')
                    
                break

    # Final closing message
    print('successfully visited')
    print('''
+++++++++++++++++++++++++++++++++++++++++++
  
*****************THANKS FOR VISITING********************
  
+++++++++++++++++++++++++++++++++++++++++++
 
''')
