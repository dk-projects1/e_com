import pytz
from datetime import date, datetime
from django.utils.text import slugify
from pyexpat.errors import messages
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from base64 import b64encode
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import check_password
from bson import ObjectId
from django.core.files.base import ContentFile
from admin_d.models import Admin, N_coupon, N_product, n_category, N_collection, home_page, telegram_cr, email, footer

# Create your views here.

def admin_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = Admin.objects.get(username=username)
            if check_password(password, admin.password):
                request.session['admin_id'] = str(admin._id)
                return redirect('dashboard')
            else:
                error = "Invalid admin credentials. Please try again."
        except Admin.DoesNotExist:
            error = "Admin account not found. Please check your username."

    return render(request, 'login.html', {'error': error})

def dashboard(request):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))
            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)
            return render(request, 'dashboard.html', {'initials': initials})
        except Admin.DoesNotExist:
            return redirect('admin')
    else:
        return redirect('admin')
    
def logout(request):
    request.session.clear()
    return redirect('admin')

def collection_list(request):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))

            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)

            collection = N_collection.objects.all().order_by('-created_date')
            paginator = Paginator(collection, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, 'collections/collection_list.html', {'initials': initials,'collections': page_obj, 'page_obj': page_obj,}) 
        except Admin.DoesNotExist:
            return redirect('admin')   
        
    return redirect('admin')

def new_collection(request):    
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))
            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)

            if request.method == 'POST':
                name = request.POST.get('name')
                slug_input = request.POST.get('slug')
                slug = slugify(slug_input or name)
                description = request.POST.get('description')
                status = request.POST.get('status')
                image_file = request.FILES.get('image')

                image = b64encode(image_file.read()).decode("utf-8") if image_file else ""

                new_collection = N_collection(
                    name=name,
                    slug=slug,
                    description=description,
                    image=image,
                    is_active=(status == 'active')
                )
                new_collection.save()
                return redirect('collection_list')

            return render(request, 'collections/new_collection.html', {'initials': initials})

        except Admin.DoesNotExist:
            return redirect('admin')
    return redirect('admin')

def collection_edit(request, post_id):
    if 'admin_id' not in request.session:
        return redirect('admin')

    collection = get_object_or_404(N_collection, _id=ObjectId(post_id))

    try:
        admin_id = request.session['admin_id']
        admin = Admin.objects.get(pk=ObjectId(admin_id))
        name_parts = admin.username.strip().split()
        initials = ''.join(part[0].upper() for part in name_parts if part)

        if request.method == 'POST':
            name = request.POST.get('name')
            slug_input = request.POST.get('slug')
            slug = slugify(slug_input or name)
            description = request.POST.get('description')
            is_active = request.POST.get('status') == 'active'

            # Image update
            image_file = request.FILES.get('image')
            if image_file:
                image = b64encode(image_file.read()).decode("utf-8")
            else:
                image = collection.image  # Keep existing

            # Update collection fields
            collection.name = name
            collection.slug = slug
            collection.description = description
            collection.image = image
            collection.is_active = is_active

            collection.save()
            return redirect('collection_list')  # Replace with your actual redirect name

        return render(request, 'collections/edit_collection.html', {
            'collection': collection,
            'initials': initials
        })

    except Admin.DoesNotExist:
        return redirect('admin')

def delete_collections(request, post_id):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))  # Validate admin

            # Check if post_id is a valid ObjectId
            try:
                post = N_collection.objects.get(_id=ObjectId(post_id))
            except N_product.DoesNotExist:
                raise Http404("not found")

            post.delete()
            return redirect('collection_list')

        except Admin.DoesNotExist:
            return redirect('admin')
    else:
        return redirect('admin')

def new_coupon(request):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))

            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)

            if request.method == 'POST':
                code = request.POST.get('code')
                description = request.POST.get('description')
                is_active = request.POST.get('is_active') == 'on'
                discount_type = request.POST.get('discount_type')
                discount_value = request.POST.get('discount_value')
                free_shipping = request.POST.get('free_shipping') == 'on'
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')

                coupon = N_coupon(
                    code=code,
                    description=description,
                    is_active=is_active,
                    discount_type=discount_type,
                    discount_value=discount_value,
                    start_date=start_date,
                    end_date=end_date,
                    free_shipping=free_shipping
                )
                coupon.save()
                return redirect('coupon_list') 

            return render(request, 'new_coupon.html', {'initials': initials, 'categories': categories})

        except Admin.DoesNotExist:
            return redirect('admin')   
        
    return redirect('admin')

def categories(request):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))
            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)
            categories = n_category.objects.all()
            return render(request, 'category/category.html', {'initials': initials, 'categories':categories})
        except Admin.DoesNotExist:
            return redirect('admin')
    else:
        return redirect('admin')

def new_category(request):    
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))
            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)
            if request.method == 'POST':
                name = request.POST.get('name')
                img = request.FILES.get('image')
                image = b64encode(img.read()).decode("utf-8")
                dec = request.POST.get('description')
                Visibility_status = request.POST.get('status')
                url_key_in = request.POST.get('url_key')
                url_key = slugify(url_key_in or name)
                meta_titel = request.POST.get('meta_title')
                meta_keyword = request.POST.get('meta_keywords')
                meta_dec = request.POST.get('meta_description')
                data = n_category(
                    name=name,
                    image=image,
                    description=dec,
                    visibility_status=Visibility_status,
                    url_key=url_key,
                    meta_title=meta_titel,
                    meta_keyword=meta_keyword,
                    meta_description=meta_dec
                )
                data.save()
                return redirect('category')
            return render(request, 'category/new_category.html', {'initials': initials})
        except Admin.DoesNotExist:
            return redirect('admin')
    else:
        return redirect('admin')

def edit_category(request, post_id):
    if 'admin_id' not in request.session:
        return redirect('admin')
    
    admin_id = request.session['admin_id']
    admin = Admin.objects.get(pk=ObjectId(admin_id))
    name_parts = admin.username.strip().split()
    initials = ''.join(part[0].upper() for part in name_parts if part)
    category = get_object_or_404(n_category, _id=ObjectId(post_id))

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        visibility_status = request.POST.get('status')
        url_key_in = request.POST.get('url_key')
        if url_key_in == category.url_key:
            url_key = url_key
        else:
            url_key = url_key_in
        meta_title = request.POST.get('meta_title')
        meta_keywords = request.POST.get('meta_keywords')
        meta_description = request.POST.get('meta_description')

        # Handle base64 image
        image = request.FILES.get('image')
        if image:
            img = b64encode(image.read()).decode("utf-8")
        else:
            img = category.image  # Use existing image if none uploaded

        # Update the category fields
        category.name = name
        category.description = description
        category.visibility_status = visibility_status
        category.url_key = url_key
        category.meta_title = meta_title
        category.meta_keyword = meta_keywords
        category.meta_description = meta_description
        category.image = img

        category.save()
        return redirect('category')  # update with your category list view name

    return render(request, 'category/edit_category.html', {'initials':initials, 'category': category})

def delete_category(request, post_id):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))  # Validate admin

            # Check if post_id is a valid ObjectId
            try:
                post = n_category.objects.get(_id=ObjectId(post_id))
            except n_category.DoesNotExist:
                raise Http404("Category not found")

            post.delete()
            return redirect('category')

        except Admin.DoesNotExist:
            return redirect('admin')
    else:
        return redirect('admin')
    
def new_product(request):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))

            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)

            categories = n_category.objects.all()
            collections = N_collection.objects.all()

            if request.method == 'POST':
                name = request.POST.get('name')
                categories_id = request.POST.get('category')
                category = n_category.objects.get(_id=ObjectId(categories_id))
                collections_id = request.POST.get('collection')
                collection = N_collection.objects.get(_id=ObjectId(collections_id))
                price = float(request.POST.get('price'))
                f_price = float(request.POST.get('F_price'))
                description = request.POST.get('description')
                patterns = request.POST.get('patterns')
                fabric = request.POST.get('fabric')
                Pocket = request.POST.get('Pocket')
                hight = request.POST.get('hight')
                sleeves = request.POST.get('sleeves')
                wash_car = request.POST.get('wash_car')
                img = request.FILES.get('image')
                image = b64encode(img.read()).decode("utf-8")
                free_delivery = request.POST.get('free_delivery')
                visibility = request.POST.get('visible')
                url_key_in = request.POST.get('url_key')
                url_key = slugify(url_key_in or name)
                meta_title = request.POST.get('meta_title')
                meta_keywords = request.POST.get('meta_keywords')
                meta_description = request.POST.get('meta_description')

                # Size-wise quantity
                stock_s = int(request.POST.get('stock_s', 0))
                stock_m = int(request.POST.get('stock_m', 0))
                stock_l = int(request.POST.get('stock_l', 0))
                stock_xl = int(request.POST.get('stock_xl', 0))

                # Store variants as dictionary in MongoDB
                variants = {
                    'S': stock_s,
                    'M': stock_m,
                    'L': stock_l,
                    'XL': stock_xl
                }

                product = N_product(
                    name=name,
                    category=category,
                    collection = collection,
                    price=price,
                    f_price = f_price,
                    description=description,
                    patterns=patterns,
                    Pocket=Pocket,
                    fabric=fabric,
                    hight=hight,
                    sleeves=sleeves,
                    wash_car=wash_car,
                    image=image,
                    free_delivery=free_delivery,
                    visibility=visibility,
                    url_key=url_key,
                    meta_title=meta_title,
                    meta_keywords=meta_keywords,
                    meta_description=meta_description,
                    variants=variants
                )
                product.save()
                return redirect('product_list')

            return render(request, 'product/new_product.html', {'initials':initials, 'categories': categories, 'collections':collections})

        except Admin.DoesNotExist:
            return redirect('admin')

    return redirect('admin')

def product_list(request):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))

            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)

            query = request.GET.get('q', '')
            category_id = request.GET.get('category', '')
            collection_id = request.GET.get('collection', '')
            free_delivery = request.GET.get('free_delivery', '')
            visibility = request.GET.get('visibility', '')

            products = N_product.objects.all()

            if query:
                products = products.filter(name__icontains=query)

            if category_id:
                products = products.filter(category_id=ObjectId(category_id))
            
            if collection_id:
                products = products.filter(collection_id=ObjectId(collection_id))

            if free_delivery:
                products = products.filter(free_delivery=free_delivery)

            if visibility:
                products = products.filter(visibility=visibility)

            # Sort products by latest
            products = products.order_by('-created_date')

            # Paginate the result
            paginator = Paginator(products, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            categories = n_category.objects.all()
            collection = N_collection.objects.all()

            return render(request, 'product/product_list.html', {
                'initials': initials,
                'page_obj': page_obj,
                'query': query,
                'category_id': category_id,
                'free_delivery': free_delivery,
                'visibility': visibility,
                'categories': categories,
                'collections':collection,
                'collection_id':collection_id
            })

        except Admin.DoesNotExist:
            return redirect('admin')

    return redirect('admin')

def product_edit(request, post_id):
    if 'admin_id' not in request.session:
        return redirect('admin')

    product = get_object_or_404(N_product, _id=ObjectId(post_id))
    categories = n_category.objects.all()
    category_id = n_category.objects.get(_id=ObjectId(product.category_id))
    collections = N_collection.objects.all()
    collection_id = N_collection.objects.get(_id=ObjectId(product.collection_id))

    if request.method == 'POST':
        name = request.POST.get('name')
        categories_id = request.POST.get('category')
        collections_id = request.POST.get('collection')
        collection = N_collection.objects.get(_id=ObjectId(collections_id))
        selected_category = n_category.objects.get(_id=ObjectId(categories_id))
        price = float(request.POST.get('price'))
        f_price = float(request.POST.get('price'))

        description = request.POST.get('description')

        # Image Handling
        image = request.FILES.get('image')
        if image:
            img = b64encode(image.read()).decode("utf-8")
        else:
            img = product.image

        # Size-wise quantities
        stock_s = int(request.POST.get('stock_s', 0))
        stock_m = int(request.POST.get('stock_m', 0))
        stock_l = int(request.POST.get('stock_l', 0))
        stock_xl = int(request.POST.get('stock_xl', 0))

        variants = {
            "S": stock_s,
            "M": stock_m,
            "L": stock_l,
            "XL": stock_xl
        }

        # Other fields
        free_delivery = request.POST.get('free_delivery')
        visibility = request.POST.get('visibility')
        url_key = request.POST.get('url_key')
        meta_title = request.POST.get('meta_title')
        meta_keywords = request.POST.get('meta_keywords')
        meta_description = request.POST.get('meta_description')

        # Update product
        product.name = name
        product.category = selected_category
        product.collection = collection
        product.price = price
        product.f_price = f_price
        product.image = img
        product.description = description
        product.variants = variants
        product.free_delivery = free_delivery
        product.visibility = visibility
        product.url_key = url_key
        product.meta_title = meta_title
        product.meta_keywords = meta_keywords
        product.meta_description = meta_description

        product.save()
        return redirect('product_list')

    return render(request, 'product/edit_product.html', {
        'product': product,
        'categories': categories,
        'category_id': category_id,
        'collection_id': collection_id,
        'collections':collections
    })

def delete_product(request, post_id):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))  # Validate admin

            # Check if post_id is a valid ObjectId
            try:
                post = N_product.objects.get(_id=ObjectId(post_id))
            except N_product.DoesNotExist:
                raise Http404("not found")

            post.delete()
            return redirect('product_list')

        except Admin.DoesNotExist:
            return redirect('admin')
    else:
        return redirect('admin')

def new_coupon(request):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))

            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)

            if request.method == 'POST':
                code = request.POST.get('code')
                description = request.POST.get('description')
                is_active = request.POST.get('is_active') == 'on'
                discount_type = request.POST.get('discount_type')
                discount_value = request.POST.get('discount_value')
                free_shipping = request.POST.get('free_shipping') == 'on'
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')

                coupon = N_coupon(
                    code=code,
                    description=description,
                    is_active=is_active,
                    discount_type=discount_type,
                    discount_value=discount_value,
                    start_date=start_date,
                    end_date=end_date,
                    free_shipping=free_shipping
                )
                coupon.save()
                return redirect('coupon_list') 

            return render(request, 'coupon/new_coupon.html', {'initials': initials, 'categories': categories})

        except Admin.DoesNotExist:
            return redirect('admin')   
        
    return redirect('admin')

def coupon_list(request):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))

            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)

            coupon = N_coupon.objects.all().order_by('-end_date')
            paginator = Paginator(coupon, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, 'coupon/coupon.html', {'initials': initials,'coupons': page_obj, 'page_obj': page_obj,}) 
        except Admin.DoesNotExist:
            return redirect('admin')   
        
    return redirect('admin')

def edit_coupon(request, post_id):
    if 'admin_id' in request.session:
        # Get the coupon
        coupon = get_object_or_404(N_coupon, _id=ObjectId(post_id))

        if request.method == 'POST':
            code = request.POST.get('code')
            description = request.POST.get('description')
            is_active = True if request.POST.get('is_active') == 'on' else False
            discount_type = request.POST.get('discount_type')
            discount_value = float(request.POST.get('discount_value') or 0)
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            free_shipping = True if request.POST.get('free_shipping') == 'on' else False

            # Assign values to the coupon
            coupon.code = code
            coupon.description = description
            coupon.is_active = is_active
            coupon.discount_type = discount_type
            coupon.discount_value = discount_value
            coupon.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            coupon.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            coupon.free_shipping = free_shipping

            coupon.save()
            return redirect('coupon_list')

        return render(request, 'coupon/edit_coupon.html', {'coupon': coupon})
    else:
        return redirect('admin')

def delete_coupon(request, post_id):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))  # Validate admin

            # Check if post_id is a valid ObjectId
            try:
                post = N_coupon.objects.get(_id=ObjectId(post_id))
            except N_coupon.DoesNotExist:
                raise Http404("Coupon not found")

            post.delete()
            return redirect('coupon_list')

        except Admin.DoesNotExist:
            return redirect('admin')
    else:
        return redirect('admin')
    
def paages(request):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))
            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)
            layouts = home_page.objects.all().order_by('position')
            footer_ = footer.objects.all()
            return render(request, 'home/home_a.html', {'initials': initials, 'layouts':layouts, 'footer_':footer_})
        except Admin.DoesNotExist:
            return redirect('admin')
    else:
        return redirect('admin')
    
def new_layout(request):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))

            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)
            collections = N_collection.objects.all()
            if request.method == 'POST':
                collection_id = request.POST.get('collection_name')
                position = request.POST.get('position')
                tagline = request.POST.get('Tagline')

                if collection_id and position:
                    collection = N_collection.objects.get(_id=ObjectId(collection_id))
                    homepage = home_page(collection_name=collection, Tagline=tagline, position=position)
                    homepage.save()
                    return redirect('paages')

            return render(request, 'home/new_home_page.html', {'initials':initials, 'collections': collections})
            

        except Admin.DoesNotExist:
            return redirect('admin')   
        
    return redirect('admin')

def delete_layout(request, post_id):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))  # Validate admin

            # Check if post_id is a valid ObjectId
            try:
                post = home_page.objects.get(_id=ObjectId(post_id))
            except home_page.DoesNotExist:
                raise Http404("Coupon not found")

            post.delete()
            return redirect('paages')

        except Admin.DoesNotExist:
            return redirect('admin')
    else:
        return redirect('admin')
 
def edit_layout(request, post_id):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))
            layout = get_object_or_404(home_page, _id=ObjectId(post_id))
            collections = N_collection.objects.all()

            if request.method == 'POST':
                collection_id = request.POST.get('collection_name')
                position = request.POST.get('position')
                tagline = request.POST.get('Tagline')

                if collection_id and position:
                    collection = N_collection.objects.get(_id=ObjectId(collection_id))

                    layout.collection_name = collection
                    layout.position = position
                    layout.Tagline = tagline
                    layout.save()
                    return redirect('paages')  # Redirect to layout listing page

            return render(request, 'home/edit_layout.html', {
                'layout': layout,
                'collections': collections,
                'initials': ''.join(part[0].upper() for part in admin.username.strip().split())
            })
        except Admin.DoesNotExist:
            return redirect('admin')
    else:
        return redirect('admin')

def show_credentials(request):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))
            name_parts = admin.username.strip().split()
            initials = ''.join(part[0].upper() for part in name_parts if part)
            email_id = email.objects.all()
            return render(request, 'credentials/credentials.html', {'initials': initials, 'email':email_id})
        except Admin.DoesNotExist:
            return redirect('admin')
    else:
        return redirect('admin')
    
def edit_credentials(request,post_id):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))

            # Check if ID exists in email model
            if email.objects.filter(_id=ObjectId(post_id)).exists():
                email_obj = email.objects.get(_id=ObjectId(post_id))

                if request.method == 'POST':
                    email_value = request.POST.get('email')
                    app_pass = request.POST.get('app_pass')

                    if email_value and app_pass:
                        email_obj.email_id = email_value
                        email_obj.app_pass = app_pass
                        email_obj.save()
                        return redirect('show_credentials')  # Adjust this name to your actual URL

                return render(request, 'credentials//edit_email.html', {
                    'email_obj': email_obj,
                    'initials': ''.join(part[0].upper() for part in admin.username.strip().split())
                })

            # If ID exists in telegram_cr instead, skip or pass
            elif telegram_cr.objects.filter(_id=ObjectId(post_id)).exists():
                pass  # No operation, or you can redirect or show message if needed

            # If ID exists in neither model
            else:
                return redirect('show_credentials')  # or render an error page

        except Admin.DoesNotExist:
            return redirect('admin')

    return redirect('admin')

def edit_footer(request, post_id):
    if 'admin_id' in request.session:
        try:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(pk=ObjectId(admin_id))

            if footer.objects.filter(_id=ObjectId(post_id)).exists():
                footer_obj = footer.objects.get(_id=ObjectId(post_id))

                if request.method == 'POST':
                    footer_obj.qotes = request.POST.get('qotes')
                    footer_obj.quotes = request.POST.get('quotes')
                    footer_obj.em = request.POST.get('em')
                    footer_obj.phone_no = request.POST.get('phone_no')
                    footer_obj.email_id = request.POST.get('email_id')
                    footer_obj.fb = request.POST.get('fb')
                    footer_obj.insta = request.POST.get('insta')
                    footer_obj.youtube = request.POST.get('youtube')
                    footer_obj.whatsapp = request.POST.get('whatsapp')
                    footer_obj.wno = request.POST.get('wno')
                    footer_obj.save()
                    return redirect('paages')  # Update this route name as needed

                return render(request, 'home/edit_footer.html', {
                    'footer_obj': footer_obj,
                    'initials': ''.join(part[0].upper() for part in admin.username.strip().split())
                })

            else:
                return redirect('show_footer')

        except Admin.DoesNotExist:
            return redirect('admin')

    return redirect('admin')

