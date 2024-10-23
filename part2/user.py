#!/usr/bin/python3

import uuid
from datetime import datetime
import re
import smtplib
from email.mime.text import MIMEText
import bcrypt

class user:
    def __init__(self, id, first_name, last_name, email, password):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.place = [] # Each user can have several location
        self.review = [] # Each user can leave several reviews


    # Generate the unique token
    def generer_token():
        return str(uuid.uuid4())


    # Check first_name validity
    def validate_first_name(first_name):
        # Length check (between 3 an 30 characters)
        if len(first_name) < 3 or len(first_name) > 30:
            return False
        
        # Character verification: letters, spaces, apostrophes and hyphens are allowed
        # Regex: ^ = start, $ = end, [a-zA-ZÀ-ÿ] = letters with accents
        # Apostrophes and hyphens are accepted between letters.
        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", first_name):
            return False
        
        return True


    # Check Last_name validity
    def validate_last_name(last_name):
        # Length check (between 3 an 30 characters)
        if len(last_name) < 3 or len(last_name) > 30:
            return False
        
        # Character verification: letters, spaces, apostrophes and hyphens are allowed
        # Regex: ^ = start, $ = end, [a-zA-ZÀ-ÿ] = letters with accents
        # Apostrophes and hyphens are accepted between letters.
        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", last_name):
            return False
        
        return True


    # Check email validity
    def validate_email(email):
        if "@" and "." in email:
            return True
        else:
            return False
        
    # Check if the email is alrady present in the datebase
    def verifier_unicite_email(email, db):
        user = db.find_user_by_email(email)
        return user is None  # Returns True if the e-mail is unique
    
    # Send a verification email
    def send_email_verification(email_destinataire, token):
        subject = "Verify your email address"
        message = f"Click on this link to verify your mail : (http/your_mail.com/verify-email) token={token}"

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = "no-reply@yoursite.com"
        msg['To'] = email_destinataire

        try:
            with smtplib.SMTP("smtp.yoursite.com", 587) as server:
                server.starttls()
                server.login("your_email@yoursite.com", "your_password")
                server.sendmail(msg["From"], msg["To"], msg.as_tring())
            print("E-mail sent successfully.")
        except Exception as e:
            print(f"Error sending e-mail: {e}")

    # Confirm email verification
    def verifier_token(token, db):
        user = db.find_user_by_token(token)
        if user:
            user.email_verify = True
            db.save(user)
            return True
        return False


    # Function to check password complexity
    def validate_password(password):
        # Check minimum password length
        if len(password) < 8:
            return False

        # Check for capital letters
        if not re.search(r"[A-Z]", password):
            return False

        # Check for lower-case letters
        if not re.search(r"[a-z]", password):
            return False

        # Check the presence of a digit
        if not re.search(r"\d", password):
            return False

        # Check for the presence of a special character
        if not re.search(r"[!@#$%^&*()_+=-]", password):
            return False
        
        return True

    # Function to confirm password
    def confirm_password(password, confirm_password):
        if password != confirm_password:
            return False
        return None

    # Password hash function
    def hasher_password(password):
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return password_hash

    # Execute validation
    password = input("Enter your password: ")
    confirm_password = input("Confirm your password: ")

    # Check security criteria
    message_error = validate_password(password)
    if message_error:
        print(f"Error : {message_error}")
    else:
    # Confirmation check
        confirm_message = confirm_password(password, confirm_password)
    if confirm_message:
        print(f"Error : {confirm_message}")
    else:
        # Hash password
        password_hash = hasher_password(password)
        print(f"Password validated and hashed: {password_hash.decode("utf-8")}")

    # Define each location as a user
    def add_place(self, place):
        self.place.append(place)
        place.user = user

    # Define eache reviews as a user
    def add_review(self, review):
        self.review.append(review)


    # Validaty datetime
    def save(self):
        """Update the update_at timestamp whenever the object is modified"""
        self.created_at = datetime.now()
        self.update_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.item():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save() # Update the update_at timestamp