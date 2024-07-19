from django.db import models

class InvitationCode(models.Model): 
    code = models.CharField(max_length=100)
    exp = models.CharField(max_length=25)
    
    # constructor input all info
    def __init__(self, code, exp) -> None:
        self.code = code
        self.exp = exp
        
    # return inventory sku
    def __str__(self) -> str:
        return str(self.code)
    
    
class RetailRecord(models.Model):
    MARKETPLACE_CHOISES = [
        ('Hibid', 'Hibid'),
        ('Retail', 'Retail'),
        ('eBay', 'eBay'),
        ('Wholesale', 'Wholesale'),
        ('Other', 'Other')
    ]
    
    PAYMENTMETHOD_CHOISES = [
        ('Cash', 'Cash'),
        ('E-transfer', 'E-transfer'),
        ('Check', 'Check'),
        ('Online', 'Online'),
        ('Store Credit', 'Store Credit'),
    ]
    
    sku = models.IntegerField()
    time = models.CharField(max_length=20)
    amount = models.IntegerField()
    quantity = models.IntegerField()
    marketplace = models.CharField(max_length=15, choices=MARKETPLACE_CHOISES)
    paymentMethod = models.CharField(max_length=15, choices=PAYMENTMETHOD_CHOISES)
    buyerName = models.CharField(max_length=30)
    adminName = models.CharField(max_length=30)
    adminId = models.CharField(max_length=40, blank=True)
    invoiceNumber = models.CharField(max_length=30, blank=True)
    
    def __init__(self, sku, time, amount, quantity, marketplace, paymentMethod, buyerName, adminName, adminId) -> None:
        self.sku = sku
        self.time = time
        self.amount = amount
        self.quantity=quantity
        self.marketplace = marketplace
        self.paymentMethod = paymentMethod
        self.buyerName = buyerName
        self.adminName = adminName
        self.adminId = adminId
        
    def __str__(self) -> str:
        return str(self.sku)
    
class ReturnRecord(models.Model):
    PAYMENTMETHOD_CHOISES = [
        ('Cash', 'Cash'),
        ('E-transfer', 'E-transfer'),
        ('Check', 'Check'),
        ('Online', 'Online'),
        ('Store Credit', 'Store Credit'),
    ]
    
    # plus a RetailRecord models object
    returnTime: models.CharField(max_length=30)
    returnQuantity: models.CharField(max_length=4)
    returnAmount: models.CharField(max_length=7)
    refundMethod: models.CharField(max_length=30, choices=PAYMENTMETHOD_CHOISES)
    reason: models.CharField(max_length=100, blank=True)
    adminName: models.CharField(max_length=30)
    adminId: models.CharField(max_length=40, blank=True)
    
    def __init__(self, returnTime, refundMethod, reason, adminName, adminId) -> None:
        self.returnTime = returnTime
        self.refundMethod = refundMethod
        self.reason = reason
        self.adminName = adminName
        self.adminId = adminId
        
    def __str__(self) -> str:
        return str(self.returnTime)