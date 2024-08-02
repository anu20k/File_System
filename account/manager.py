from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, unique_id, password=None, **extra_fields):
        if not unique_id:
            raise ValueError("Unique id is required")
        
        # extra_fields['email'] = self.normalize_email(extra_fields['email'])
        user = self.model(unique_id=unique_id, **extra_fields)
        user.set_password(password)
        user.save(using= self.db)
        
        return user
         
        
    
    def create_superuser(self, unique_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(unique_id, password, **extra_fields)
        
        