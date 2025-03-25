from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import cv2
import numpy as np
import json
from .models import QRCode, User
import ast

def scanner_view(request):
    """View to display the QR code scanner interface"""
    return render(request, 'core/scanner.html')

@csrf_exempt
def verify_qr(request):
    """API endpoint to verify QR code data"""
    if request.method == 'POST':
        try:
            # Get the image data from the request
            image_data = request.FILES.get('image')
            if not image_data:
                return JsonResponse({'error': 'No image data received'}, status=400)

            # Convert image to numpy array
            nparr = np.frombuffer(image_data.read(), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Create QR Code detector
            qr_detector = cv2.QRCodeDetector()
            
            # Detect and decode QR code
            retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(img)
            
            if not retval or not decoded_info:
                return JsonResponse({'error': 'No QR code found'}, status=400)

            # Get the first QR code data (we'll use the first one found)
            qr_data = decoded_info[0]
            
            # Convert string representation of dictionary to actual dictionary
            try:
                qr_data = ast.literal_eval(qr_data)
            except:
                return JsonResponse({'error': 'Invalid QR code data'}, status=400)

            # Verify user exists
            try:
                user = User.objects.get(id=qr_data['user_id'])
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            # Get latest QR code for user
            qr_code = QRCode.objects.filter(user=user).latest('created_at')

            if not qr_code.is_valid:
                return JsonResponse({'error': 'QR code is invalid'}, status=400)

            # Update last used time
            qr_code.last_used = timezone.now()
            qr_code.save()

            return JsonResponse({
                'success': True,
                'message': 'Access granted',
                'user': {
                    'username': user.username,
                    'role': user.role
                }
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
