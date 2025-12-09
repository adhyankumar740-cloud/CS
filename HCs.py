import mysql.connector as sqltr

def login():
    print('-------------------------------------------------')
    user_id = int(input("Enter your user ID:"))
    user_name = input("Enter user name:")
    password = int(input("Enter your password:"))
    
    mydb = sqltr.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    
    co.execute("select * from users")
    user_records = co.fetchall()
  
    s_result = [] 
    
    for record in user_records:
        if user_name == record[1] and str(password) == str(record[2]) and user_id == record[0]:
            print("login successful.")
            co.execute('select * from users where UserID={} and UserName="{}" and Password={}'.format(user_id, user_name, password))
            s_result = co.fetchall()
            break
            
    if not s_result: 
        print("wrong details given")
        
    mydb.commit()
    print('-------------------------------------------------')
    return s_result 

def room_booking(user_details):
    print('-------------------------------------------------')
    mydb = sqltr.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    co.execute('select * from roombooking ')
    booking_records = co.fetchall()
    
    room_num_input = int(input("Enter your selected Room Number: "))
    
    booking_id = len(booking_records) + 1 
    print("Your Booking ID is", booking_id)
    
    user_id = user_details[0][0] 
    user_name = user_details[0][1] 
    address = input("Enter Address: ")
    phone_num = int(input("Enter Phone number:"))
    check_in_date = input('Enter check in date (YYYY-MM-DD):')
    check_out_date = input('Enter check out date (YYYY-MM-DD):')
    gender = input('Enter your gender: ')
    
    co.execute('select RoomNum, Status from rooms')
    room_statuses = co.fetchall()
    
    room_found = False 
    
    for room_record in room_statuses:
        room_num_db = room_record[0]
        status = room_record[1].upper() 
        
        if room_num_db == room_num_input:
            room_found = True 
            
            if status == 'VACANT': 
                co.execute("insert into roombooking values({},{},{},'{}','{}',{},'{}','{}','{}')".format(room_num_input, booking_id, user_id, user_name, address, phone_num, check_in_date, check_out_date, gender))
                co.execute("update rooms set Status='{}' where RoomNum={}".format('Occupied', room_num_input))
                print('Room booked.')
                break
            elif status == 'OCCUPIED': 
                print('''Room chosen is already booked by someone.
Please choose another room. ''')
                break
    
    if not room_found:
        print('Entered room number does not exist.')
        
    mydb.commit()
    print('-------------------------------------------------')

def room_details():
    print('-------------------------------------------------')
    mydb = sqltr.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    co.execute('select * from rooms')
    room_records = co.fetchall()
    for record in room_records:
        print(record)
    mydb.commit()
    print('-------------------------------------------------')

def menu():
    print('-------------------------------------------------')
    mydb = sqltr.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
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
    if not user_details:
        print("Please log in or sign up first.")
        return

    print('-------------------------------------------------')
    mydb = sqltr.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
    co = mydb.cursor()
    user_id = user_details[0][0] 
    
    table_num = int(input("Enter your Table Number: "))

    co.execute('select * from order_info')
    order_info_records = co.fetchall()
    
    order_num = len(order_info_records) + 1 
    
    co.execute('select * from menu')
    menu_dishes = co.fetchall() 
    
    distinct_items_count = int(input("Enter no. of distinct items to be ordered: "))
    total_amount = 0 
    
    for i in range(distinct_items_count):
        item_num_input = int(input("Enter the item number to be ordered: "))
        quantity = int(input("Enter the quantity of above item to be ordered: "))
        
        item_found = False
        for dish in menu_dishes:
            if item_num_input == dish[0]: 
                price = dish[2] 
                subtotal = price * quantity 
                
                co.execute('insert into order_details values({},{},{},{})'.format(order_num, item_num_input, quantity, subtotal))
                total_amount = total_amount + subtotal
                item_found = True
                break
        
        if not item_found:
            print(f"Item number {item_num_input} not found in menu. Skipping.")
            
    co.execute('insert into order_info values({},{},{},{})'.format(order_num, user_id, table_num, total_amount))
    
    mydb.commit()
    print('Your order has been placed. Total Amount: {}'.format(total_amount))
    print('-------------------------------------------------')
    
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

if __name__ == "__main__":
    
    s = [] 

    while True:
        print('-------------------------------------------------')
        print('Press 1- Login')
        print('Press 2- About hotel') 
        print('Press 3- Exit')
        print('-------------------------------------------------')
        
        
        choose = int(input("Enter your choice: "))
            
        if choose == 1:
            s_result = login() 
            if s_result:
                s = s_result
                if 'GUEST' in s[0][3].upper():
                    print('Login successful.')
                    break
                else:
                    print('Login successful, but only Guests are supported in this version.')
                    s = [] 
                    print('Please log in with a Guest account.')

            else:
                print('Login failed. Please try again.')
                
        elif choose == 2:
            print(xk)
        
        elif choose == 3: 
            break

        else:
            print('Invalid choice.
Please enter 1, 2, or 3.')
                
    if s and len(s) > 0:
        hy = s[0][3].upper() 
        
        if 'GUEST' in hy:
            while True:
            
                print('-------------------------------------------------')
                print('Press 1- Lodging Room')
                print('Press 2- Restaurant')
                print('Press 3- Exit')
                print('-------------------------------------------------')
                
                c = int(input("Enter your choice: "))
                    
                if c == 1: 
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
                            
                        break 

                elif c == 2: 
                    while True:
               
                        print('Welcome to our restaurant')
                        print('Press 1- Menu')
                        print('Press 2- Order')
                        print('Press 3- Exit') 
                        
                        ci = int(input('Enter your choice:'))
                        
       
                        if ci == 1:
                            menu()
                        elif ci == 2:
                            order(s)
                        elif ci == 3: 
               
                            break
                        else:
                            print('Give required input')
                            
                        break 
       
                  
                elif c == 3:
                    break
                else:
                    print('Give required input')
        
    print('successfully visited')
    print('''
+++++++++++++++++++++++++++++++++++++++++++
  
*****************THANKS FOR VISITING********************
  
+++++++++++++++++++++++++++++++++++++++++++
 
''')
