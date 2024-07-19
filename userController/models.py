from django.db import models
from django.core.validators import MinLengthValidator

class User(models.Model): 
    ROLE_CHOISES = [
        ('Admin', 'Admin'),
        ('Super Admin', 'Super Admin'),
        ('QAPersonal', 'QAPersonal'),
        ('Sales', 'Sales'),
        ('Shelving Manager', 'Shelving Manager'),
    ]
    
    _id: models.AutoField(primary_key=True)
    name: models.CharField(max_length=40, validators=[MinLengthValidator(3, 'Name Invalid')])
    email: models.EmailField(max_length=45, validators=[MinLengthValidator(8, 'Email Invalid')])
    password: models.CharField(max_length=50, validators=[MinLengthValidator(8, 'Password Invalid')])
    role: models.CharField(max_length=20, validators=[MinLengthValidator(4, 'Role Invalid')], choices=ROLE_CHOISES)
    registrationDate: models.CharField(max_length=30, validators=[MinLengthValidator(8,'Registration date invalid')])
    userActive: models.BooleanField()
    
    # constructor input all info
    def __init__(self, name, email, password, role, registrationDate, userActive ) -> None:
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.registrationDate = registrationDate
        self.userActive = userActive
        
    # return inventory sku
    def __str__(self) -> str:
        return str(self.email)