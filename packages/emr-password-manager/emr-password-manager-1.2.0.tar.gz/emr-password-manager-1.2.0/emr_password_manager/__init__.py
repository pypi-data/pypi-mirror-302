# __init__.py

from .emr_password_manager import generate_password , password_strength
import sys
sys.path.insert(0, '.')

__all__ = [
    "generate_password",
    "password_strength",
]