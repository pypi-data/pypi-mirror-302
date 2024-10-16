# emr_password_manager.py

import random
import string

def generate_password(length=8, use_letters=True, use_digits=True, use_symbols=True, exclude_chars=""):
    """
    Generates a random password based on specified criteria.
    
    Parameters:
    - length (int): The length of the password. Default is 8.
    - use_letters (bool): Whether to include letters. Default is True.
    - use_digits (bool): Whether to include digits. Default is True.
    - use_symbols (bool): Whether to include symbols. Default is True.
    - exclude_chars (str): Characters to exclude from the password.
    
    Returns:
    - str: The generated password.
    """
    character_pool = ""
    
    if use_letters:
        character_pool += string.ascii_letters
    
    if use_digits:
        character_pool += string.digits
    
    if use_symbols:
        character_pool += string.punctuation
    
    character_pool = ''.join([ch for ch in character_pool if ch not in exclude_chars])
    
    if not character_pool:
        raise ValueError("No characters available to generate a password. Check your criteria.")
    
    password = ''.join(random.choice(character_pool) for _ in range(length))
    return password

def password_strength(password):
    """
    Evaluates the strength of a given password and returns a score out of 10.
    
    Parameters:
    - password (str): The password to evaluate.
    
    Returns:
    - int: A score between 0 and 10 based on the password strength.
    """
    score = 0

    if len(password) >= 8:
        score += 2
    if len(password) >= 12:
        score += 2
    
    if any(char in string.ascii_lowercase for char in password):
        score += 1
    if any(char in string.ascii_uppercase for char in password):
        score += 1
    if any(char in string.digits for char in password):
        score += 1
    if any(char in string.punctuation for char in password):
        score += 2
    
    if len(set(password)) == len(password):
        score += 1
    
    return str(score) + " / 10"