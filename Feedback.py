def feedback():
    """Handles the user feedback submission."""
    global s
    if not s:
        print("Please log in or sign up first.")
        return

    print('-------------------------------------------------')
    try:
        mydb = m.connect(host="localhost", user="root", password="admin", database="taj_hotel")
        co = mydb.cursor()
        
        user_id = s[0][0] 
        user_name = s[0][1]
        
        # Get next Feedback ID
        co.execute('SELECT FeedbackID FROM feedback ORDER BY FeedbackID DESC LIMIT 1')
        last_id = co.fetchone()
        feedback_id = last_id[0] + 1 if last_id else 1 
        
        print("Your Feedback ID is", feedback_id)
        
        comment = input("Enter your feedback/comment: ")
        rating = int(input("Enter a rating (1-5, 5 being best): "))
        
        if not 1 <= rating <= 5:
            print("Rating must be between 1 and 5. Please try again.")
            return

        # Insert into feedback (FeedbackID, UserID, UserName, Comment, Rating)
        # Note: You need a 'feedback' table in your database for this to work.
        co.execute("insert into feedback values({},{},'{}','{}',{})".format(feedback_id, user_id, user_name, comment, rating))
        
        mydb.commit()
        print('Thank you! Your feedback has been recorded.')
        
    except ValueError:
        print('Invalid input given (expected a number for rating).')
    except m.Error as err:
        print(f"Database error: {err}. Ensure the 'feedback' table exists.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print('-------------------------------------------------')
