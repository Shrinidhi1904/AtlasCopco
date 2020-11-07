from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings

import os
from datetime import datetime
from PIL import Image
from .forms import *
import cv2
import numpy as np
import pyzbar.pyzbar as pb


# Create your views here.
@login_required
def new_visitor(request):
	employees = Employee.objects.all()
	form = NewVisitorForm()
	if request.method == 'POST':
		form = NewVisitorForm(request.POST, request.FILES)
		print(form)
		if form.is_valid():
			visitor = form.save(commit=False)
			visitor.save()
			qrcodeimg = generateQR(visitor.id)
			visitor.qrcode = qrcodeimg
			send_qrcode_email(visitor.email, qrcodeimg) # email to send the qr code to the visitor
			visitor.save()
			messages.success(request, 'QR Code has been sent to the visitor\'s email-id')
			messages.success(request, f'The Visitor has been booked for entry')
			return redirect('/')
		else:
			messages.error(request, 'Error!')
	context = {'form': form, 'employees': employees}
	return render(request, 'entry/visitor_booking.html', context)


def generateQR(id):
	import qrcode
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=5,
		border=4
	)
	visitor = Visitor.objects.get(id=id)  # visitors id
	visitor.token = str(visitor.id) + str(visitor.name).upper()[:5] + str(visitor.email)[:5]
	qr.add_data(visitor.token)  # visitors id
	visitor.save()
	qr.make(fit=True)
	img = qr.make_image(fill_color="black", back_color="white")
	qrname = visitor.name + "_" + str(hash(visitor.name))
	img.save("./media/qrcodes/" + qrname + ".png")
	
	return "/media/qrcodes/" + qrname + ".png"
	
	# visitor.qrcode = "/media/qrcodes/" + qrname + ".png"
	# visitor.save()
@csrf_exempt
@login_required()
def scanQR(request, **kwargs):
	if kwargs.get('id'):
		visitor = Visitor.objects.get(id=kwargs.get('id'))
		print('id', visitor.id, cv2.__file__)
	cam = cv2.VideoCapture(0)
	while True:
		_, frame = cam.read()
		Read = pb.decode(frame)
		for ob in Read:
			readData = str(ob.data.rstrip().decode('utf-8'))
			print('readData',readData)
			if kwargs.get('qr') == 'userQR':
				visitor = Visitor.objects.filter(token=readData).order_by('-id').first()
				if visitor:
					print('/updatevisitor/'+str(visitor.id)+'/')
					cv2.destroyAllWindows()
					return redirect('/photoscan/'+str(visitor.id)+"/")
			elif visitor.visit_token:
				print(visitor.visit_token)
				if readData == visitor.visit_token:
					visitor.out_time = datetime.now()
					visitor.save()
					send_normal_email(visitor)
					messages.success(request, f'QR Code scanned successfully!')
					cv2.destroyAllWindows()
					return redirect(f'{reverse("home")}')
			else:
				visitor.visit_token = readData
				visitor.in_time = datetime.now()
				visitor.save()
				send_normal_email(visitor)
				messages.success(request, f'QR Code scanned with value: { readData }')
				cv2.destroyAllWindows()
				return redirect(reverse('home'))
		
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1)
		if key == 27:
			cv2.destroyAllWindows()
			return redirect(f'{reverse("home")}')
			break
		
		template_name = 'home/home.html'
		
def send_normal_email(Visitor):
	to_email = Visitor.user.user.email
	print(to_email)
	if Visitor.out_time:
		subject = Visitor.name + ' has left Atlas Copco Campus'
		message = 'Hello!\n\n\t' + Visitor.name + ' has left the Atlas Copco campus at ' + str(Visitor.out_time.date()) + ' ' + Visitor.out_time.strftime("%X") + '.'
	else:
		subject = Visitor.name + ' is visiting Atlas Copco'
		message = 'Hello!\n\n\t' + Visitor.name + ' is visiting the Atlas Copco campus at ' + str(Visitor.in_time.date()) + ' ' + Visitor.in_time.strftime("%X") + '.'
	email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to_email])
	email.content_subtype='html'
	email.send(fail_silently=False)

def send_qrcode_email(to_email, qrcodeimg):
	subject = 'QR Code for entry in Atlas Copco'
	message = '''Hello!\nYou have been granted the permission to visit Atlas Copco as a visitor!\n 
			PFA an attached QR Code which you will have to show when you leave our premises!'''
	email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to_email])
	email.content_subtype='html'
	
	with open(os.path.join(settings.BASE_DIR, '') + qrcodeimg, mode='rb') as file:
		email.attach(os.path.join(settings.BASE_DIR, '') + qrcodeimg, file.read(), 'image/png')
	
	email.send(fail_silently=False)
	
class VisitorUpdateView(LoginRequiredMixin, UpdateView):
	model = Visitor
	fields = ['name', 'purpose', 'no_of_people', 'email', 'mobile', 'photo_id_number', 'photo_id', 'user']
	success_url = reverse_lazy('home')
	template_name = 'entry/visitor_booking.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['employees'] = Employee.objects.all()
		
		return context