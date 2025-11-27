from django.db import models

class BaseLocation(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image_url = models.URLField(blank=True, help_text="URL to an image of the location")
    description = models.TextField(blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Pandit(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.URLField(blank=True, help_text="URL to an image of the pandit")
    description = models.TextField(blank=True)
    years_of_experience = models.IntegerField(default=5)
    specialization = models.CharField(max_length=100, blank=True, help_text="e.g., Vedic Rituals, Katha")

    class Meta:
        verbose_name = "Pandit"
        verbose_name_plural = "Pandits"

    def __str__(self):
        return self.name

class Temple(BaseLocation):
    deity = models.CharField(max_length=100, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Temple"
        verbose_name_plural = "Temples"

class LunchSpot(BaseLocation):
    cuisine = models.CharField(max_length=100, default="Vegetarian")
    price_range = models.CharField(max_length=50, choices=[('$', '$'), ('$$', '$$'), ('$$$', '$$$')], default='$$')

    class Meta:
        verbose_name = "Lunch Spot"
        verbose_name_plural = "Lunch Spots"

class Booking(models.Model):
    pandit = models.ForeignKey(Pandit, on_delete=models.CASCADE, related_name='bookings')
    user_name = models.CharField(max_length=200)
    booking_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pandit', 'booking_date')
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"Booking for {self.pandit.name} on {self.booking_date} by {self.user_name}"
