"""
User service layer for handling user-related business logic
"""
from typing import Dict, Any, Optional, Tuple
from django.db import transaction
from django.contrib.auth import get_user_model
from django.apps import apps
from apps.rbac.models import Group, UserGroup
from apps.accounts.models import User
from apps.accounts.validators import validate_login_data
import logging

logger = logging.getLogger(__name__)


class UserService:
    """
    Service class for user-related operations
    """
    
    def __init__(self):
        self.User = get_user_model()
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User UUID
            
        Returns:
            User instance or None if not found
        """
        try:
            return self.User.objects.get(id=user_id)
        except self.User.DoesNotExist:
            return None
    
    def get_all_users(self) -> list:
        """
        Get all users ordered by username
        
        Returns:
            List of User instances
        """
        return list(self.User.objects.all().order_by("username"))
    
    def check_username_exists(self, username: str, exclude_user_id: Optional[str] = None) -> bool:
        """
        Check if username already exists
        
        Args:
            username: Username to check
            exclude_user_id: User ID to exclude from check (for updates)
            
        Returns:
            True if username exists, False otherwise
        """
        queryset = self.User.objects.filter(username=username)
        if exclude_user_id:
            queryset = queryset.exclude(id=exclude_user_id)
        return queryset.exists()
    
    def check_email_exists(self, email: str, exclude_user_id: Optional[str] = None) -> bool:
        """
        Check if email already exists
        
        Args:
            email: Email to check
            exclude_user_id: User ID to exclude from check (for updates)
            
        Returns:
            True if email exists, False otherwise
        """
        if not email:
            return False
        queryset = self.User.objects.filter(email=email)
        if exclude_user_id:
            queryset = queryset.exclude(id=exclude_user_id)
        return queryset.exists()
    
    def get_group_by_name(self, group_name: str) -> Optional[Group]:
        """
        Get group by name (case insensitive)
        
        Args:
            group_name: Group name to find
            
        Returns:
            Group instance or None if not found
        """
        try:
            return Group.objects.get(name__iexact=group_name)
        except Group.DoesNotExist:
            return None
    
    def assign_user_to_group(self, user: User, group: Group) -> bool:
        """
        Assign user to a group
        
        Args:
            user: User instance
            group: Group instance
            
        Returns:
            True if successful, False otherwise
        """
        try:
            UserGroup.objects.get_or_create(user_id=user.id, group_id=group.id)
            return True
        except Exception as e:
            logger.error(f"Failed to assign user {user.id} to group {group.id}: {e}")
            return False
    
    def remove_user_from_all_groups(self, user: User) -> bool:
        """
        Remove user from all groups
        
        Args:
            user: User instance
            
        Returns:
            True if successful, False otherwise
        """
        try:
            UserGroup.objects.filter(user_id=user.id).delete()
            return True
        except Exception as e:
            logger.error(f"Failed to remove user {user.id} from groups: {e}")
            return False
    
    @transaction.atomic
    def create_user(self, user_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """
        Create a new user
        
        Args:
            user_data: Dictionary containing user data
            
        Returns:
            Tuple of (success, result)
        """
        try:
            # Extract and validate data
            username = (user_data.get("username") or "").strip()
            email = (user_data.get("email") or "").strip()
            password = user_data.get("password") or ""
            first_name = (user_data.get("first_name") or "").strip()
            last_name = (user_data.get("last_name") or "").strip()
            group_name = (user_data.get("group") or "").strip()
            
            # Validate required fields
            if not username or not password:
                return False, {"error": "username and password are required"}
            
            # Check for existing username
            if self.check_username_exists(username):
                return False, {"error": "username already exists"}
            
            # Check for existing email
            if email and self.check_email_exists(email):
                return False, {"error": "email already exists"}
            
            # Validate group if provided
            group = None
            if group_name:
                group = self.get_group_by_name(group_name)
                if not group:
                    return False, {"error": f"Group '{group_name}' does not exist"}
            
            # Create user
            user = self.User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            
            # Assign to group if provided
            if group:
                if not self.assign_user_to_group(user, group):
                    logger.warning(f"Failed to assign user {user.id} to group {group.id}")
            
            logger.info(f"User created successfully: {user.username}")
            return True, {"user": user}
            
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            return False, {"error": "Failed to create user"}
    
    @transaction.atomic
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """
        Update an existing user
        
        Args:
            user_id: User UUID
            update_data: Dictionary containing update data
            
        Returns:
            Tuple of (success, result)
        """
        try:
            # Get user
            user = self.get_user_by_id(user_id)
            if not user:
                return False, {"error": "User not found"}
            
            # Extract data
            username = (update_data.get("username") or "").strip() or None
            email = (update_data.get("email") or "").strip() or None
            first_name = (update_data.get("first_name") or "").strip() if "first_name" in update_data else None
            last_name = (update_data.get("last_name") or "").strip() if "last_name" in update_data else None
            password = update_data.get("password") or None
            group_name = (update_data.get("group") or "").strip() if "group" in update_data else None
            
            # Check uniqueness for provided fields
            if username and self.check_username_exists(username, exclude_user_id=user_id):
                return False, {"error": "username already exists"}
            
            if email and self.check_email_exists(email, exclude_user_id=user_id):
                return False, {"error": "email already exists"}
            
            # Validate group if provided
            target_group = None
            if group_name is not None and group_name != "":
                target_group = self.get_group_by_name(group_name)
                if not target_group:
                    return False, {"error": f"Group '{group_name}' does not exist"}
            
            # Update user fields
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            if username is not None:
                user.username = username
            if email is not None:
                user.email = email
            if password:
                user.set_password(password)
            
            # Save user
            user.save()
            
            # Handle group assignment
            if group_name is not None:
                # Remove from all groups first
                self.remove_user_from_all_groups(user)
                # Add to new group if specified
                if target_group:
                    if not self.assign_user_to_group(user, target_group):
                        logger.warning(f"Failed to assign user {user.id} to group {target_group.id}")
            
            logger.info(f"User updated successfully: {user.username}")
            return True, {"user": user}
            
        except Exception as e:
            logger.error(f"Failed to update user {user_id}: {e}")
            return False, {"error": "Failed to update user"}
    
    def delete_user(self, user_id: str) -> Tuple[bool, Any]:
        """
        Delete a user
        
        Args:
            user_id: User UUID
            
        Returns:
            Tuple of (success, result)
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False, {"error": "User not found"}
            
            username = user.username
            user.delete()
            
            logger.info(f"User deleted successfully: {username}")
            return True, {"message": "User deleted successfully"}
            
        except Exception as e:
            logger.error(f"Failed to delete user {user_id}: {e}")
            return False, {"error": "Failed to delete user"}
    
    def validate_user_data(self, user_data: Dict[str, Any], is_update: bool = False) -> Tuple[bool, Any]:
        """
        Validate user data
        
        Args:
            user_data: User data to validate
            is_update: Whether this is for an update operation
            
        Returns:
            Tuple of (is_valid, validation_result)
        """
        errors = []
        warnings = []
        
        # Check required fields for creation
        if not is_update:
            if not user_data.get("username"):
                errors.append("Username is required")
            if not user_data.get("password"):
                errors.append("Password is required")
        
        # Validate username format if provided
        username = user_data.get("username", "").strip()
        if username:
            if len(username) < 3:
                errors.append("Username must be at least 3 characters long")
            if len(username) > 150:
                errors.append("Username must be no more than 150 characters long")
        
        # Validate email format if provided
        email = user_data.get("email", "").strip()
        if email:
            import re
            email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not email_regex.match(email):
                errors.append("Invalid email format")
        
        # Validate password strength if provided
        password = user_data.get("password", "")
        if password:
            if len(password) < 8:
                errors.append("Password must be at least 8 characters long")
            if len(password) > 128:
                errors.append("Password must be no more than 128 characters long")
        
        if errors:
            return False, {"errors": errors, "warnings": warnings}
        
        return True, {"warnings": warnings}


# Service instance
user_service = UserService()
