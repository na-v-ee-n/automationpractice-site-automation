import random
import string
from datetime import datetime

class TestDataGenerator:
    
    @staticmethod
    def generate_random_email():
        """Generate random email in format userxxxxmmm@gmail.com"""
        random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        random_numbers = ''.join(random.choices(string.digits, k=3))
        return f"user{random_chars}{random_numbers}@gmail.com"
    
    @staticmethod
    def generate_strong_password():
        """Generate a strong password"""
        return "Str0ngP@ss123!"
    
    @staticmethod
    def generate_weak_password():
        """Generate a weak password for negative testing"""
        return "123"
    
    @staticmethod
    def generate_invalid_email():
        """Generate invalid email format"""
        return "invalid-email"
    
    @staticmethod
    def generate_long_email():
        """Generate maximum length email"""
        return 'a' * 60 + '@gmail.com'
    
    @staticmethod
    def generate_special_char_email():
        """Generate email with special characters"""
        return 'test+user_123@mail.com'