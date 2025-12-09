import mysql.connector as sqltr

HOTEL_ABOUT_INFO = ''' Welcome to TAJ HOTEL, where nature meets luxury in perfect harmony.
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

print('''
+++++++++++++++++++++++++++++++++++++++++++
  Welcome to TAJ HOTEL System
  
  -- Starting directly into the Main Menu --
+++++++++++++++++++++++++++++++++++++++++++
''')

print('-------------------------------------------------')
print('Press 1- Lodging Room')
print('Press 2- Restaurant')
print('Press 3- About Hotel') 
print('Press 4- Exit')
print('-------------------------------------------------')

main_choice = int(input("Enter your choice: "))
    
if main_choice == 1: 
    
    print('-------------------------------------------------')
    print('Lodging room')
    print("Press 1- Room details")
    print('Press 2- Room booking')
    print('Press 3- Exit')
    print('-------------------------------------------------')
    
    lodging_choice = int(input("Enter your choice: "))
    
    if lodging_choice == 1:
        
        # Room Details Logic
        print('-------------------------------------------------')
        mydb = sqltr.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
        co = mydb.cursor()
        co.execute('select * from rooms')
        room_records = co.fetchall()
        for record in room_records:
            print(record)
        mydb.commit()
        print('-------------------------------------------------')

        print("Press 1- Room booking")
        print('Press 2- Skip')
        room_details_choice = int(input("Enter your choice: "))
    
        if room_details_choice == 1:
            # Room Booking Logic (from Room Details Menu)
            print('-------------------------------------------------')
            mydb = sqltr.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
            co = mydb.cursor()
            co.execute('select * from roombooking ')
            booking_records = co.fetchall()
            
            user_name = input("Enter your User Name for booking: ")
            
            room_num_input = int(input("Enter your selected Room Number: "))
            
            booking_id = len(booking_records) + 1 
            print("Your Booking ID is", booking_id)
            
            address = input("Enter Address: ")
            phone_num = int(input("Enter Phone number:"))
            check_in_date = input('Enter check in date (YYYY-MM-DD):')
            check_out_date = input('Enter check out date (YYYY-MM-DD):')
            gender = input('Enter your gender: ')
            
            co.execute('select RoomNum, Status from rooms')
            room_statuses = co.fetchall()
            
            for room_record in room_statuses:
                
                if room_record[0] == room_num_input:
                    
                    if room_record[1].upper() == 'VACANT': 
                        co.execute("insert into roombooking values({},{},{},'{}','{}',{},'{}','{}','{}')".format(room_num_input, booking_id, 0, user_name, address, phone_num, check_in_date, check_out_date, gender))
                        co.execute("update rooms set Status='{}' where RoomNum={}".format('Occupied', room_num_input))
                        print('Room booked.')
                        break
                    elif room_record[1].upper() == 'OCCUPIED': 
                        print('''Room chosen is already booked by someone.
Please choose another room. ''')
                        break
            else:
                print('Entered room number does not exist.')
                
            mydb.commit()
            print('-------------------------------------------------')

    elif lodging_choice == 2:
        # Room Booking Logic (Direct Booking Menu)
        print('-------------------------------------------------')
        mydb = sqltr.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
        co = mydb.cursor()
        co.execute('select * from roombooking ')
        booking_records = co.fetchall()
        
        user_name = input("Enter your User Name for booking: ")
        
        room_num_input = int(input("Enter your selected Room Number: "))
        
        booking_id = len(booking_records) + 1 
        print("Your Booking ID is", booking_id)
        
        address = input("Enter Address: ")
        phone_num = int(input("Enter Phone number:"))
        check_in_date = input('Enter check in date (YYYY-MM-DD):')
        check_out_date = input('Enter check out date (YYYY-MM-DD):')
        gender = input('Enter your gender: ')
        
        co.execute('select RoomNum, Status from rooms')
        room_statuses = co.fetchall()
        
        for room_record in room_statuses:
            
            if room_record[0] == room_num_input:
                
                if room_record[1].upper() == 'VACANT': 
                    co.execute("insert into roombooking values({},{},{},'{}','{}',{},'{}','{}','{}')".format(room_num_input, booking_id, 0, user_name, address, phone_num, check_in_date, check_out_date, gender))
                    co.execute("update rooms set Status='{}' where RoomNum={}".format('Occupied', room_num_input))
                    print('Room booked.')
                    break
                elif room_record[1].upper() == 'OCCUPIED': 
                    print('''Room chosen is already booked by someone.
Please choose another room. ''')
                    break
        else:
            print('Entered room number does not exist.')
            
        mydb.commit()
        print('-------------------------------------------------')

elif main_choice == 2: 
    
    print('Welcome to our restaurant')
    print('Press 1- Menu')
    print('Press 2- Order')
    print('Press 3- Exit') 
    
    restaurant_choice = int(input('Enter your choice:'))

    if restaurant_choice == 1:
        # Menu Logic
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

    elif restaurant_choice == 2:
        # Order Logic
        print('-------------------------------------------------')
        mydb = sqltr.connect(host="localhost", user="root", password="gouravbhai@12", database="taj_hotel")
        co = mydb.cursor()

        table_num = int(input("Enter your Table Number: "))

        co.execute('select * from order_info')
        order_info_records = co.fetchall()
        order_num = len(order_info_records) + 1
        
        co.execute('select * from menu')
        menu_dishes = co.fetchall() 
        
        total_amount = 0 
        
        while True:
            item_num_input = int(input("Enter the item number (0 to finish order): "))
            if item_num_input == 0:
                break

            quantity = int(input("Enter the quantity: "))
            
            for dish in menu_dishes:
                if item_num_input == dish[0]: 
                    price = dish[2]
                    subtotal = price * quantity 
                    total_amount = total_amount + subtotal
                    break
                    
        co.execute('insert into order_info values({},{},{},{})'.format(order_num, 0, table_num, total_amount))
        
        mydb.commit()
        print('Your order has been placed. Total Amount: {}'.format(total_amount))
        print('-------------------------------------------------')

elif main_choice == 3:
    print(HOTEL_ABOUT_INFO)
    
elif main_choice == 4:
    pass

print('successfully visited')
print('''
+++++++++++++++++++++++++++++++++++++++++++

*****************THANKS FOR VISITING********************

+++++++++++++++++++++++++++++++++++++++++++

''')
