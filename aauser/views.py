from django.utils import timezone
import json
import random
import smtplib
from django.http import HttpRequest, JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_POST
from admin_d.models import (
    N_product,
    n_category,
    N_collection,
    home_page,
    footer,
    Admin,
    N_coupon,
)
from .models import user_ID, Order, address


def home(request):
    homepage_layouts = home_page.objects.order_by("position")
    catelog = n_category.objects.all()
    footer_ = footer.objects.all()
    return render(
        request,
        "home.html",
        {"layouts": homepage_layouts, "catelog": catelog, "footer_": footer_},
    )


def view_collection(request, slug):
    try:
        collection = N_collection.objects.get(slug=slug)
        products = list(N_product.objects.filter(collection=collection))
        catelog = n_category.objects.all()
        footer_ = footer.objects.all()
        # Sorting
        sort_option = request.GET.get("sort")

        def parse_price(p):
            try:
                return float(p.price.replace(",", "").replace("Rs.", "").strip())
            except:
                return 0.0

        if sort_option == "low_to_high":
            products.sort(key=parse_price)
        elif sort_option == "high_to_low":
            products.sort(key=parse_price, reverse=True)
        elif sort_option == "newest":
            products.sort(key=lambda p: p.created_date, reverse=True)

        return render(
            request,
            "view_collection.html",
            {
                "collection": collection,
                "products": products,
                "sort_option": sort_option,
                "catelog": catelog,
                "footer_": footer_,
            },
        )

    except N_collection.DoesNotExist:
        return redirect("home")


def product_detail(request, url_key):
    try:
        products = N_product.objects.get(url_key=url_key)
        related_products = N_product.objects.filter(category=products.category)[:4]
        footer_ = footer.objects.all()
        return render(
            request,
            "view_product.html",
            {
                "product": products,
                "related_products": related_products,
                "footer_": footer_,
            },
        )

    except N_collection.DoesNotExist:
        return redirect("home")


def is_username_available(username):
    try:
        user_ID.objects.get(username=username)
        return False
    except user_ID.DoesNotExist:
        return True


def is_email_available(email):
    try:
        user_ID.objects.get(email=email)
        return False
    except user_ID.DoesNotExist:
        return True


def otp_verification(receiver_email):
    otp = str(random.randint(100000, 999999))

    sender_email = "devaprojects66@gmail.com"
    sender_password = "pcbz nmzw vxxi jfzx"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender_email, sender_password)

    subject = "Your OTP"
    body = f"Your OTP is: {otp}"
    message = f"Subject: {subject}\n\n{body}"

    server.sendmail(sender_email, receiver_email, message)

    server.quit()
    return otp


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        re_pass = request.POST["re_pass"]

        if not is_username_available(username):
            error = "Username is already taken. Please choose a different username."
            return render(request, "auth/signup.html", {"error": error})

        if not is_email_available(email):
            error = "This mail ID is already registered."
            return render(request, "auth/signup.html", {"error": error})

        if password == re_pass:
            otp = otp_verification(email)
            request.session["name"] = username
            request.session["email"] = email
            request.session["password"] = password
            request.session["otp"] = otp
            return redirect(reverse("otp_verify"))
        else:
            error = "Password mismatch!"
            return render(request, "signup.html", {"error": error})

    return render(request, "auth/signup.html")


def otp_verify(request):
    if request.method == "POST":
        name = request.session["name"]
        email = request.session.get("email")
        hashed_password = make_password(request.session["password"])
        otp = request.session["otp"]
        e_otp = request.POST["otp"]

        if otp == e_otp:
            user = user_ID(username=name, password=hashed_password, email=email)
            user.save()
            return redirect("login")
        else:
            error = "Invalid OTP. Please try again."
            return render(
                request, "auth/otp_verification.html", {"email": email, "error": error}
            )

    return render(request, "auth/otp_verification.html")


def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST["password"]
        re_pass = request.POST["re_pass"]
        try:
            user = user_ID.objects.get(username=username)
            otp = otp_verification(user.email)
            if password == re_pass:
                request.session["email"] = user.email
                request.session["password"] = password
                request.session["otp"] = otp
                return redirect(reverse("forgot_otp_verify"))
            else:
                error = "Password mismatch!"
            return render(request, "auth/forgot_password.html", {"error": error})
        except user_ID.DoesNotExist:
            error = "User does not exist. Please sign up."
            return render(request, "auth/forgot_password.html", {"error": error})
    return render(request, "auth/forgot_password.html")


def forgot_otp_verify(request):
    if request.method == "POST":
        email = request.session.get("email")
        hashed_password = make_password(request.session["password"])
        otp = request.session["otp"]
        e_otp = request.POST["otp"]
        if otp == e_otp:
            try:
                user = user_ID.objects.get(email=email)
                user.password = hashed_password
                user.save()
                return redirect("login")
            except user_ID.DoesNotExist:
                error = "User does not exist. Please sign up."
                return render(
                    request,
                    "auth/otp_verification.html",
                    {"email": email, "error": error},
                )
        else:
            error = "Invalid OTP. Please try again."
            return render(
                request, "auth/otp_verification.html", {"email": email, "error": error}
            )
    return render(request, "auth/otp_verification.html")


def login(request: HttpRequest):

    next_url = request.GET.get("next", "/")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if username == "admin":
            admin = Admin.objects.get(username=username)
            if check_password(password, admin.password):
                request.session["admin_id"] = str(admin._id)
                return redirect("admin")
            else:
                error = "Invalid admin credentials. Please try again."
                return render(request, "auth/login.html", {"error": error})
        else:
            try:
                user = user_ID.objects.get(username=username)
                if check_password(password, user.password):
                    request.session["user_id"] = str(user._id)
                    return redirect(next_url)
                else:
                    error = "Invalid credentials. Please try again."
                    return render(request, "auth/login.html", {"error": error})
            except user_ID.DoesNotExist:
                error = "User does not exist. Please sign up."
                return render(request, "auth/login.html", {"error": error})

    if "user_id" in request.session:
        return redirect("home")
    elif "admin_id" in request.session:
        return redirect("admin")
    else:
        return render(request, "auth/login.html")


def logout(request):
    request.session.clear()
    return redirect("login")

@csrf_exempt
def checkout(request):
    if "user_id" not in request.session:
        return redirect(f"/login/?next=/checkout/")

    user_id = request.session["user_id"]
    user_obj = user_ID.objects.get(_id=ObjectId(user_id))

    # 🏷 Coupon Apply (from form)
    if request.method == "POST" and request.content_type.startswith("application/x-www-form-urlencoded"):
        coupon_code = request.POST.get("coupon_code", "").strip()
        order_total = float(request.POST.get("order_total", 0))

        try:
            coupon = N_coupon.objects.get(code=coupon_code)
            today = timezone.now().date()

            if coupon.start_date <= today <= coupon.end_date:
                if coupon.discount_type == "fixed_order":
                    discount = coupon.discount_value
                elif coupon.discount_type == "percent_product":
                    discount = order_total * (coupon.discount_value / 100)
                else:
                    discount = 0

                discount = round(discount, 2)
                final_total = max(order_total - discount, 0)

                return JsonResponse({
                    "status": "success",
                    "message": f"Coupon '{coupon_code}' applied! Discount: ₹{discount:.2f}",
                    "final_total": round(final_total, 2)
                })

            return JsonResponse({"status": "error", "message": "Coupon is expired."})

        except N_coupon.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid coupon code."})

    # 📦 Place Order (from JS fetch)
    if request.method == "POST" and request.content_type.startswith("application/json"):
        try:
            data = json.loads(request.body or "{}")
        except Exception:
            data = {}

        cart_data = data.get("cart", {})
        coupon_code = (data.get("coupon_code") or "").strip()

        if not cart_data:
            return JsonResponse({"status": "error", "message": "Cart is empty or invalid."})

        total = sum(float(item["price"]) * int(item["qty"]) for item in cart_data.values())

        # Validate coupon again on backend
        discount = 0
        if coupon_code:
            try:
                coupon = N_coupon.objects.get(code=coupon_code)
                today = timezone.now().date()

                if coupon.start_date <= today <= coupon.end_date:
                    if coupon.discount_type == "fixed_order":
                        discount = coupon.discount_value
                    elif coupon.discount_type == "percent_product":
                        discount = total * (coupon.discount_value / 100)
                    discount = round(discount, 2)
                else:
                    coupon_code = ""  # expired
            except N_coupon.DoesNotExist:
                coupon_code = ""  # invalid

        final_total = max(total - discount, 0)

        # Save order
        new_order = Order(
            user_id=user_obj,
            items=cart_data,
            total=final_total,
            copun_code=coupon_code,
            status="Pending"
        )
        new_order.save()

        # Reduce stock
        for item in cart_data.values():
            try:
                product = N_product.objects.get(_id=ObjectId(item["id"]))
                variants = product.variants or {}

                if item.get("size") in variants:
                    variants[item["size"]] = max(0, variants[item["size"]] - int(item["qty"]))

                product.variants = variants
                product.save()
            except N_product.DoesNotExist:
                pass

        return JsonResponse({
            "status": "success",
            "redirect_url": "/order-success/"
        })

    return render(request, "cart/checkout.html", {"footer_": footer.objects.all()})

def order_success(request):
    return render(request, "placeorder.html")

def orders(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        return redirect(f"/login/?next=/orders/")

    # Get user_id from session
    user_id = request.session["user_id"]

    try:
        # Fetch orders for this user from MongoDB
        user_orders = Order.objects.filter(user_id=ObjectId(user_id)).order_by('-created_at')
    except Exception as e:
        print("Error fetching orders:", e)
        user_orders = []

    return render(request, "order.html", {"orders": user_orders})

def order_detail(request, post_id):
    # Check if user is logged in
    if "user_id" not in request.session:
        return redirect(f"/login/?next=/orders/{post_id}/")

    try:
        # Get order only if it belongs to the logged-in user
        order = Order.objects.get(
            _id=ObjectId(post_id),
            user_id=ObjectId(request.session["user_id"])
        )
    except Order.DoesNotExist:
        return redirect("/orders/")  # If not found, go back to orders list

    return render(request, "order_detail.html", {"order": order, 'order_id':post_id})

def profile(request):
    if "user_id" not in request.session:
        return redirect(f"/login/?next=/profile/")

    try:
        user_obj = user_ID.objects.get(_id=ObjectId(request.session["user_id"]))
    except user_ID.DoesNotExist:
        return redirect("/login/")

    # Fetch all addresses for this user
    addresses = address.objects.filter(user_id=user_obj)

    return render(request, "profile.html", {
        "user": user_obj,
        "addresses": addresses
    })

def add_address(request):
    if "user_id" not in request.session:
        return redirect(f"/login/?next=/add-address/")

    try:
        user_obj = user_ID.objects.get(_id=ObjectId(request.session["user_id"]))
    except user_ID.DoesNotExist:
        return redirect("/login/")

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        street = request.POST.get("street")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")
        country = request.POST.get("country")

        new_address = address(
            user_id = user_obj,
            name= name,
            phone= phone,
            street= street,
            city=city,
            state= state,
            zipcode= zipcode,
            country= country
        )
        new_address.save()

        # Ensure addresses field exists
        if not hasattr(user_obj, "addresses") or user_obj.addresses is None:
            user_obj.addresses = []

        # Append new address
        user_obj.addresses.append(new_address)
        user_obj.save()

        messages.success(request, "Address added successfully.")
        return redirect("/profile/")

    return render(request, "add_address.html", {"user": user_obj})

def about(request):
    footer_ = footer.objects.all()
    return render(request, 'web_content/about_us.html', {"footer_": footer_})

def contact(request):
    footer_ = footer.objects.all()
    return render(request, 'web_content/contact.html', {"footer_": footer_})

def shipping(request):
    footer_ = footer.objects.all()
    return render(request, 'web_content/shipping.html', {"footer_": footer_})

def refund(request):
    footer_ = footer.objects.all()
    return render(request, 'web_content/refund.html', {"footer_": footer_})

def terms(request):
    footer_ = footer.objects.all()
    return render(request, 'web_content/ts.html', {"footer_": footer_})

def view_catlog(request, slug):
    try:
        collection = n_category.objects.get(url_key=slug)
        products = list(N_product.objects.filter(category=collection))
        catelog = n_category.objects.all()
        footer_ = footer.objects.all()
        # Sorting
        sort_option = request.GET.get("sort")

        def parse_price(p):
            try:
                return float(p.price.replace(",", "").replace("Rs.", "").strip())
            except:
                return 0.0

        if sort_option == "low_to_high":
            products.sort(key=parse_price)
        elif sort_option == "high_to_low":
            products.sort(key=parse_price, reverse=True)
        elif sort_option == "newest":
            products.sort(key=lambda p: p.created_date, reverse=True)

        return render(
            request,
            "view_catelog.html",
            {
                "collection": collection,
                "products": products,
                "sort_option": sort_option,
                "catelog": catelog,
                "footer_": footer_,
            },
        )

    except n_category.DoesNotExist:
        return redirect("home")
    