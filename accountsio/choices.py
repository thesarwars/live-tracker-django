from django.db import models

class UserTypeChoices(models.TextChoices):
    CUSTOMER = 'customer', 'Customer'
    RIDER = 'rider', 'Rider'
    ADMIN = 'admin', 'Admin'
    
class GenderChoices(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"