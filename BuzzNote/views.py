from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Contact
from .forms import ContactForm
import phonenumbers
# Create your views here.

def front_page(request):
  return render(request, "index.html")

def add_contact(request):
  success = False
  added_contact = None
  if request.method == "POST":
    form = ContactForm(request.POST)
    if form.is_valid():
      new_contact = form.save()
      success = True
      added_contact = new_contact
      return render(request, "add_contact.html", {"form": form, "added_contact": added_contact, "success": success},)
  else:
    form = ContactForm()
  return render(request, "add_contact.html", {"form": form, "added_contact": added_contact, "success": success},)
  
def search_contact(request):
  page_number = request.GET.get("page", 1)
  name = request.GET.get("name", "").strip()
  phone = request.GET.get("phone", "").strip()
  email = request.GET.get("email", "").strip()
  address = request.GET.get("address", "").strip()

  if request.method == "POST":
    name = request.POST.get("name", "").strip()
    phone = request.POST.get("phone", "").strip()
    email = request.POST.get("email", "").strip()
    address = request.POST.get("address", "").strip()
    page_number = 1
  
  if name or phone or email or address:
    contacts = Contact.objects.filter(name__icontains=name, phone__icontains=phone, email__icontains=email, address__icontains=address).order_by("id")
  else:
    contacts = Contact.objects.all().order_by("id")

  paginator = Paginator(contacts, 10)
  page_obj = paginator.get_page(page_number)

  print(page_obj)
  return render(request, "search_contact.html", {"contacts": page_obj, "name_query": name, "phone_query": phone, "email_query": email, "address_query": address})

def edit_contact(request, contact_id, page_number):
  pn = request.GET.get("page", page_number)
  print(f"[DBG] edit_contact {contact_id}, {page_number}, {pn} <<<")
  success = False

  if request.method == "POST":
    contact = Contact.objects.get(id=contact_id)
    name = request.POST.get("name")
    try:
        phone = phonenumbers.parse(request.POST.get("phone"),None)
        if phonenumbers.is_possible_number(phone) and phonenumbers.is_valid_number(phone):
            phone = phonenumbers.format_number(phone, PhoneNumberFormat.E164)
        else:
            phone = contact.phone
    except:
        phone = contact.phone
    email = request.POST.get("email")
    address = request.POST.get("address")
    if contact.name != name or contact.phone != phone or contact.email != email or contact.address != address:
      contact.name = name
      contact.phone = phone
      contact.email = email
      contact.address = address
      contact.save()
      success = True
  
  contact_list = Contact.objects.all()
  paginator = Paginator(contact_list, 10)
  page_number = request.POST.get("page", request.GET.get("page", page_number))
  page_obj = paginator.get_page(page_number)
  return render(request, "edit_contact.html", {"contacts": page_obj, "success": success, "updated_contact_id": contact_id,},)

def delete_contact(request, contact_id, page_number):
  print("[DBG] delete_contact called for ID:", contact_id)
  if request.method == "POST":
    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    return redirect("edit_contact", contact_id=contact_id,page_number=page_number)
