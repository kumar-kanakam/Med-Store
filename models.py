from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    cause = models.CharField(max_length=100, null=True, blank=True)
    batch_no = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    expiry_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()


    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)


    def __str__(self):
        return self.name


class Sale(models.Model):
    medicine = models.CharField( max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)