from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
import logging

logger = logging.getLogger(__name__)

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=[
        ('admin', 'Admin'),
        ('user', 'User'),
    ], default='user')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'QR User'
        verbose_name_plural = 'QR Users'

    def __str__(self):
        return f"{self.username} ({self.role})"

class QRCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qr_codes')
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    is_valid = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        data = {
            'user_id': str(self.user.id),
            'username': self.user.username,
            'role': self.user.role,
        }
        
        qr.add_data(str(data))
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        filename = f'qr_code_{self.user.username}.png'
        
        self.qr_code.save(filename, File(buffer), save=False)

    def send_qr_code_email(self):
        if not self.qr_code:
            return

        subject = 'Your QR Code'
        message = f'''Hello {self.user.username},

Please find your QR code attached. You can use this QR code for access.

Best regards,
QR Code System'''
        
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.user.email]
        )
        
        with open(self.qr_code.path, 'rb') as f:
            email.attach(
                f'qr_code_{self.user.username}.png',
                f.read(),
                'image/png'
            )
        
        email.send(fail_silently=False)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)
        
        if is_new:
            self.send_qr_code_email()

    def __str__(self):
        return f"QR Code for {self.user.username}"
