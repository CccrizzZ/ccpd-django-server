from django.db import models
from jsonfield import JSONField

class InventoryImage(models.Model): 
    _id: models.AutoField(primary_key=True)
    time: models.CharField(max_length=30)
    owner: models.CharField(max_length=32)
    images: JSONField()
    
    # constructor input all info
    def __init__(self, time, sku, owner, images) -> None:
        self.time = time
        self.sku = sku
        self.owner = owner
        self.images = images
        
    # return inventory sku
    def __str__(self) -> str:
        return str(self.sku)