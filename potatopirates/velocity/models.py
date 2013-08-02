from django.db import models

# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=20, decimal_places=3)
    store_id = models.ForeignKey("Store")

    def __unicode__(self):
        return self.name

class CustomerProfile(models.Model):
    rfid = models.CharField(max_length=20)

    def __unicode__(self):
        return self.rfid

class Receipt(models.Model):
    customer_id = models.ForeignKey("CustomerProfile")
    time = models.DateTimeField()

    def __unicode__(self):
        return "%s (%s)" % (self.id ,self.customer_id)

class Purchase(models.Model):
    receipt_id = models.ForeignKey("Receipt")
    product_id = models.ForeignKey("Product")
    price = models.DecimalField(max_digits=20, decimal_places=3)

    def __unicode__(self):
        return "%s: %s (%s)" % (self.id, self.product_id, self.receipt_id)


