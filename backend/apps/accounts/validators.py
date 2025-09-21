"""
Request validation for authentication endpoints
"""
import re
from typing import Dict, List, Optional, Tuple
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class LoginValidator:
    """
    Validator for login request data
    """
    
    # Constants for validation rules
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 150
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128
    
    # Username validation regex (alphanumeric, underscore, hyphen, dot)
    USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9._-]+$')
    
    # Email validation regex
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_login_request(self, data: Dict) -> Tuple[bool, Dict]:
        """
        Validate login request data
        
        Args:
            data: Dictionary containing login data
            
        Returns:
            Tuple of (is_valid, validated_data)
        """
        self.errors = []
        self.warnings = []
        
        # Extract and validate fields
        username = self._validate_username(data.get('username', ''))
        password = self._validate_password(data.get('password', ''))
        
        # Check for additional fields that shouldn't be present
        self._validate_no_extra_fields(data, ['username', 'password'])
        
        if self.errors:
            return False, {'errors': self.errors, 'warnings': self.warnings}
        
        return True, {
            'username': username,
            'password': password,
            'warnings': self.warnings
        }
    
    def _validate_username(self, username: str) -> Optional[str]:
        """
        Validate username field
        
        Args:
            username: Username to validate
            
        Returns:
            Validated username or None if invalid
        """
        if not username:
            self.errors.append("Username is required")
            return None
        
        # Convert to string and strip whitespace
        username = str(username).strip()
        
        if not username:
            self.errors.append("Username cannot be empty")
            return None
        
        # Check length
        if len(username) < self.MIN_USERNAME_LENGTH:
            self.errors.append(f"Username must be at least {self.MIN_USERNAME_LENGTH} characters long")
            return None
        
        if len(username) > self.MAX_USERNAME_LENGTH:
            self.errors.append(f"Username must be no more than {self.MAX_USERNAME_LENGTH} characters long")
            return None
        
        # Check format (alphanumeric, underscore, hyphen, dot)
        if not self.USERNAME_REGEX.match(username):
            self.errors.append("Username can only contain letters, numbers, underscores, hyphens, and dots")
            return None
        
        # Check if it looks like an email (optional warning)
        if '@' in username and self.EMAIL_REGEX.match(username):
            self.warnings.append("Username appears to be an email address. Please use your username instead.")
        
        return username
    
    def _validate_password(self, password: str) -> Optional[str]:
        """
        Validate password field
        
        Args:
            password: Password to validate
            
        Returns:
            Validated password or None if invalid
        """
        if not password:
            self.errors.append("Password is required")
            return None
        
        # Convert to string
        password = str(password)
        
        # Check length
        if len(password) < self.MIN_PASSWORD_LENGTH:
            self.errors.append(f"Password must be at least {self.MIN_PASSWORD_LENGTH} characters long")
            return None
        
        if len(password) > self.MAX_PASSWORD_LENGTH:
            self.errors.append(f"Password must be no more than {self.MAX_PASSWORD_LENGTH} characters long")
            return None
        
        # Check for common weak passwords
        weak_passwords = [
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey'
        ]
        
        if password.lower() in weak_passwords:
            self.warnings.append("Password appears to be commonly used. Consider using a stronger password.")
        
        # Check for basic complexity (optional warning)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        complexity_score = sum([has_upper, has_lower, has_digit, has_special])
        if complexity_score < 3:
            self.warnings.append("Password could be stronger. Consider using uppercase, lowercase, numbers, and special characters.")
        
        return password
    
    def _validate_no_extra_fields(self, data: Dict, allowed_fields: List[str]) -> None:
        """
        Check for unexpected fields in the request
        
        Args:
            data: Request data dictionary
            allowed_fields: List of allowed field names
        """
        extra_fields = [field for field in data.keys() if field not in allowed_fields]
        if extra_fields:
            self.warnings.append(f"Unexpected fields found: {', '.join(extra_fields)}. These will be ignored.")
    
    def validate_mobile_login_request(self, data: Dict) -> Tuple[bool, Dict]:
        """
        Validate mobile login request data (same as regular login for now)
        
        Args:
            data: Dictionary containing login data
            
        Returns:
            Tuple of (is_valid, validated_data)
        """
        return self.validate_login_request(data)


class SecurityValidator:
    """
    Security-focused validation for login attempts
    """
    
    def __init__(self):
        self.suspicious_patterns = [
            # SQL injection patterns
            r"('|(\\')|(;)|(--)|(/\*)|(\*/)|(\|)|(\*)|(%)|(\+)|(\-)|(\=)|(\<)|(\>)|(\!)|(\@)|(\#)|(\$)|(\^)|(\&)|(\()|(\))|(\[)|(\])|(\{)|(\})|(\|)|(\\)|(\~)|(\`)|(\;)|(\:)|(\")|(\')|(\?)|(\/)|(\\)|(\*)|(\+)|(\-)|(\=)|(\<)|(\>)|(\!)|(\@)|(\#)|(\$)|(\^)|(\&)|(\()|(\))|(\[)|(\])|(\{)|(\})|(\|)|(\\)|(\~)|(\`))",
            # XSS patterns
            r"<script|javascript:|onload=|onerror=|onclick=|onmouseover=",
            # Command injection patterns
            r"(\||\&|\;|\$\(|\`|\>\>|\<\<)",
        ]
    
    def validate_security(self, username: str, password: str) -> Tuple[bool, List[str]]:
        """
        Check for suspicious patterns in login data
        
        Args:
            username: Username to check
            password: Password to check
            
        Returns:
            Tuple of (is_safe, security_warnings)
        """
        warnings = []
        
        # Check username for suspicious patterns
        for pattern in self.suspicious_patterns:
            if re.search(pattern, username, re.IGNORECASE):
                warnings.append("Username contains potentially suspicious characters")
                break
        
        # Check password for suspicious patterns
        for pattern in self.suspicious_patterns:
            if re.search(pattern, password, re.IGNORECASE):
                warnings.append("Password contains potentially suspicious characters")
                break
        
        # Check for excessive length (potential buffer overflow attempt)
        if len(username) > 1000 or len(password) > 1000:
            warnings.append("Input length exceeds normal limits")
        
        return len(warnings) == 0, warnings


def validate_login_data(data: Dict, is_mobile: bool = False) -> Tuple[bool, Dict]:
    """
    Main validation function for login requests
    
    Args:
        data: Request data dictionary
        is_mobile: Whether this is a mobile login request
        
    Returns:
        Tuple of (is_valid, result_data)
    """
    # Initialize validators
    login_validator = LoginValidator()
    security_validator = SecurityValidator()
    
    # Validate login data
    if is_mobile:
        is_valid, validated_data = login_validator.validate_mobile_login_request(data)
    else:
        is_valid, validated_data = login_validator.validate_login_request(data)
    
    if not is_valid:
        return False, validated_data
    
    # Security validation
    username = validated_data.get('username')
    password = validated_data.get('password')
    
    if username and password:
        is_safe, security_warnings = security_validator.validate_security(username, password)
        if not is_safe:
            validated_data['warnings'] = validated_data.get('warnings', []) + security_warnings
    
    return True, validated_data
