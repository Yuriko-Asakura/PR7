from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
import psycopg2


def index2(request):
    return render(request, 'zoo/index2.html')


def index(request):
    # Подключение к базе данных
    conn = psycopg2.connect(
        database='Zoo', 
        user='postgres',
        password='2005', 
        host='localhost', 
        port='5432'
    )
    cur = conn.cursor()

    # Выполнение запроса
    cur.execute("SELECT * FROM employees")

    # Получение результатов
    employees = cur.fetchall()

    # Закрытие курсора и соединения
    cur.close()
    conn.close()

    # Передача данных в шаблон
    context = {'employees': employees}
    return render(request, 'zoo/employee/page_employee.html', context)


#Сделано Animals
def Animal_page(request):
    # Подключение к базе данных
    conn = psycopg2.connect(
        database='Zoo', 
        user='postgres',
        password='2005', 
        host='localhost', 
        port='5432'
    )
    cur = conn.cursor()

    # Выполнение запроса
    cur.execute("SELECT * FROM animals")

    # Получение результатов
    animals = cur.fetchall()

    # Закрытие курсора и соединения
    cur.close()
    conn.close()
    paginator = Paginator(animals, 10)  
    page = request.GET.get('page')
    try:
        animals = paginator.page(page)
    except PageNotAnInteger:
        animals = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше максимального, переходим на последнюю страницу
        animals = paginator.page(paginator.num_pages)
    # Передача данных в шаблон
    context = {'animals': animals}
    return render(request, 'zoo/animal/page_animal.html', context)
def C_animal(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        species = request.POST.get('species')
        breed = request.POST.get('breed')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image_url = request.POST.get('image_url')
        availability = request.POST.get('availability') == 'on'

        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        sql = """
            INSERT INTO animals (name, species, breed, age, gender, description, price, image_url, availability) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (name, species, breed, age, gender, description, price, image_url, availability)

        try:
            cur.execute(sql, data)
            conn.commit()  
            messages.success(request, f'Животное "{name}" успешно добавлено!')
            return redirect('animal_page')  
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении животного: {e}')
            return redirect('page_animal') 
        finally:
            cur.close()
            conn.close()

    else:
        return render(request, 'zoo/animal/pageC_animal.html')
def delete_animal(request, animal_id):
    if request.method == 'POST':
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        sql = "DELETE FROM animals WHERE animal_id = %s"
        try:
            cur.execute(sql, (animal_id,))
            conn.commit()
            messages.success(request, f'Животное с ID {animal_id} успешно удалено!')
            return redirect('animal_page')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении животного: {e}')
            return redirect('animal_page')  
        finally:
            cur.close()
            conn.close()

    else:
        return render(request, 'zoo/animal/pageD_animal.html', {'animal_id': animal_id})
def update_animal(request, animal_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        species = request.POST.get('species')
        breed = request.POST.get('breed')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image_url = request.POST.get('image_url')
        availability = request.POST.get('availability') == 'on'

        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        sql = """
            UPDATE animals
            SET name = %s, species = %s, breed = %s, age = %s, gender = %s, description = %s, 
                price = %s, image_url = %s, availability = %s
            WHERE animal_id = %s
        """
        data = (name, species, breed, age, gender, description, price, image_url, availability, animal_id)

        try:
            cur.execute(sql, data)
            conn.commit()
            messages.success(request, f'Животное с ID {animal_id} успешно обновлено!')
            return redirect('animal_page')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении животного: {e}')
            return redirect('animal_page')  # Перенаправление на страницу с животными
        finally:
            cur.close()
            conn.close()

    else:
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        cur.execute("SELECT * FROM animals WHERE animal_id = %s", (animal_id,))
        animal = cur.fetchone()
        cur.close()
        conn.close()

        animal_data = {
            'animal_id': animal[0],
            'name': animal[1],
            'species': animal[2],
            'breed': animal[3],
            'age': animal[4],
            'gender': animal[5],
            'description': animal[6],
            'price': animal[7],
            'image_url': animal[8],
            'availability': animal[9],
        }
        return render(request, 'zoo/animal/pageU_animal.html', {'animal': animal_data})

#True
def Customer_page(request):
    conn = psycopg2.connect(
        database='Zoo', 
        user='postgres',
        password='2005', 
        host='localhost', 
        port='5432'
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()
    cur.close()
    conn.close()
    paginator = Paginator(customers, 10)  
    page = request.GET.get('page')
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)
    context = {'customers': customers}
    return render(request, 'zoo/customer/page_customer.html', context)
def C_customer(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = """
            INSERT INTO customers (first_name, last_name, email, phone_number, address) 
            VALUES (%s, %s, %s, %s, %s)
        """
        data = (first_name, last_name, email, phone_number, address)

        try:
            cur.execute(sql, data)
            conn.commit() 
            messages.success(request, f'Клиент "{first_name} {last_name}" успешно добавлен!')
            return redirect('customer_page')  
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении клиента: {e}')
            return redirect('page_customer') 
        finally:
            cur.close()
            conn.close()

    else:
        return render(request, 'zoo/customer/pageC_customer.html')
def delete_customer(request, customer_id):
    if request.method == 'POST':
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        sql = "DELETE FROM customers WHERE customer_id = %s"
        try:
            cur.execute(sql, (customer_id,))
            conn.commit()
            messages.success(request, f'Клиент с ID {customer_id} успешно удален!')
            return redirect('customer_page')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении клиента: {e}')
            return redirect('customer_page')  
        finally:
            cur.close()
            conn.close()

    else:
        return render(request, 'zoo/customer/pageD_customer.html', {'customer_id': customer_id})
def update_customer(request, customer_id):
    if request.method == 'POST':
        # Получение данных из формы
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        customer_id = request.POST.get('customer_id')
        
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = """
            UPDATE customers
            SET first_name = %s, last_name = %s, email = %s, phone_number = %s, address = %s
            WHERE customer_id = %s
        """
        data = (first_name, last_name, email, phone_number, address, customer_id)
        try:
            cur.execute(sql, data)
            conn.commit()
            messages.success(request, f'Клиент с ID {customer_id} успешно обновлен!')
            return redirect('customer_page')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении клиента: {e}')
            return redirect('customer_page') 
        finally:
            cur.close()
            conn.close()
    else:
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        customer = cur.fetchone()
        cur.close()
        conn.close()
        customer_data = {
            'customer_id': customer[0],
            'first_name': customer[1],
            'last_name': customer[2],
            'email': customer[3],
            'phone_number': customer[4],
            'address': customer[5],
        }
        return render(request, 'zoo/customer/pageU_customer.html', {'customer': customer_data, 'customer_id': customer_id})

#True
def Category_page(request):
    conn = psycopg2.connect(
        database='Zoo', 
        user='postgres',
        password='2005', 
        host='localhost', 
        port='5432'
    )
    cur = conn.cursor()

    # Выполнение запроса
    cur.execute("SELECT * FROM categories")

    # Получение результатов
    categories = cur.fetchall()

    # Закрытие курсора и соединения
    cur.close()
    conn.close()
    paginator = Paginator(categories, 10)  
    page = request.GET.get('page')
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше максимального, переходим на последнюю страницу
        categories = paginator.page(paginator.num_pages)
    # Передача данных в шаблон
    context = {'categories': categories}
    return render(request, 'zoo/category/page_category.html', context)
def C_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        sql = """
            INSERT INTO categories (name, description) 
            VALUES (%s, %s)
        """
        data = (name, description)

        try:
            cur.execute(sql, data)
            conn.commit()  
            messages.success(request, f'Категория "{name}" успешно добавлена!')
            return redirect('category_page')  
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении категории: {e}')
            return redirect('page_category') 
        finally:
            cur.close()
            conn.close()

    else:
        return render(request, 'zoo/category/pageC_category.html')
def delete_category(request, category_id):
    if request.method == 'POST':
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        sql = "DELETE FROM categories WHERE category_id = %s"
        try:
            cur.execute(sql, (category_id,))
            conn.commit()
            messages.success(request, f'Категория с ID {category_id} успешно удалена!')
            return redirect('category_page')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении категории: {e}')
            return redirect('category_page')  
        finally:
            cur.close()
            conn.close()

    else:
        return render(request, 'zoo/category/pageD_category.html', {'category_id': category_id})
def update_category(request, category_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category_id')  
        
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        sql = """
            UPDATE categories
            SET name = %s, description = %s
            WHERE category_id = %s
        """
        data = (name, description, category_id)

        try:
            cur.execute(sql, data)
            conn.commit()
            messages.success(request, f'Категория с ID {category_id} успешно обновлена!')
            return redirect('category_page')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении категории: {e}')
            return redirect('category_page')  
        finally:
            cur.close()
            conn.close()

    else:
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        cur.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
        category = cur.fetchone()
        cur.close()
        conn.close()

        category_data = {
            'category_id': category[0],
            'name': category[1],
            'description': category[2],
        }

        return render(request, 'zoo/category/pageU_category.html', {'category': category_data, 'category_id': category_id}) 

def Order_page(request):
    conn = psycopg2.connect(
        database='Zoo', 
        user='postgres',
        password='2005', 
        host='localhost', 
        port='5432'
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    cur.close()
    conn.close()
    paginator = Paginator(orders, 10)  
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    context = {'orders': orders}
    return render(request, 'zoo/order/page_order.html', context)
def C_order(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        employee_id = request.POST.get('employee')  
        order_date = request.POST.get('order_date')
        total_price = request.POST.get('total_price')
        status = request.POST.get('status')
        shipping_address = request.POST.get('shipping_address')
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = """
            INSERT INTO orders (customer_id, employee_id, order_date, total_price, status, shipping_address) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (customer_id, employee_id, order_date, total_price, status, shipping_address)
        try:
            cur.execute(sql, data)
            conn.commit()  
            messages.success(request, f'Заказ успешно добавлен!')
            return redirect('order_page')  
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении заказа: {e}')
            return redirect('page_order') 
        finally:
            cur.close()
            conn.close()

    else:
        customers = Customer.objects.all() 
        employees = Employee.objects.all()  
        return render(request, 'zoo/order/pageC_order.html', {'customers': customers, 'employees': employees})
def delete_order(request, order_id):
    if request.method == 'POST':
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = "DELETE FROM orders WHERE order_id = %s"
        try:
            cur.execute(sql, (order_id,))
            conn.commit()
            messages.success(request, f'Заказ с ID {order_id} успешно удален!')
            return redirect('order_page')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении заказа: {e}')
            return redirect('order_page') 
        finally:
            cur.close()
            conn.close()
    else:
        return render(request, 'zoo/order/delete_order.html', {'order_id': order_id})
def update_order(request, order_id):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        employee_id = request.POST.get('employee') 
        order_date = request.POST.get('order_date')
        total_price = request.POST.get('total_price')
        status = request.POST.get('status')
        shipping_address = request.POST.get('shipping_address')
        order_id = request.POST.get('order_id')
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = """
            UPDATE orders
            SET customer_id = %s, employee_id = %s, order_date = %s, total_price = %s, status = %s, shipping_address = %s
            WHERE order_id = %s
        """
        data = (customer_id, employee_id, order_date, total_price, status, shipping_address, order_id)
        try:
            cur.execute(sql, data)
            conn.commit()
            messages.success(request, f'Заказ с ID {order_id} успешно обновлен!')
            return redirect('order_page')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении заказа: {e}')
            return redirect('order_page')  
        finally:
            cur.close()
            conn.close()
    else:
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        order = cur.fetchone()
        cur.close()
        conn.close()

        order_data = {
            'order_id': order[0],
            'customer_id': order[1],
            'employee_id': order[2],
            'order_date': order[3],
            'total_price': order[4],
            'status': order[5],
            'shipping_address': order[6],
        }

        customers = Customer.objects.all()
        employees = Employee.objects.all() 
        return render(request, 'zoo/order/pageU_order.html', {'order': order_data, 'customers': customers, 'employees': employees, 'order_id': order_id})
########
def OrderDetailAnimal_page(request):
    conn = psycopg2.connect(
        database='Zoo', 
        user='postgres',
        password='2005', 
        host='localhost', 
        port='5432'
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM order_details_animals")
    order_detail_animals = cur.fetchall()
    cur.close()
    conn.close()
    paginator = Paginator(order_detail_animals, 10)  
    page = request.GET.get('page')
    try:
        order_detail_animals = paginator.page(page)
    except PageNotAnInteger:
        order_detail_animals = paginator.page(1)
    except EmptyPage:
        order_detail_animals = paginator.page(paginator.num_pages)
    context = {'order_detail_animals': order_detail_animals}
    return render(request, 'zoo/orderDetailAnimal/page_orderDetailAnimal.html', context)
def C_order_detail_animal(request):
    if request.method == 'POST':
        order_id = request.POST.get('order')
        animal_id = request.POST.get('animal')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = """
            INSERT INTO order_details_animals (order_id, animal_id, quantity, unit_price) 
            VALUES (%s, %s, %s, %s)
        """
        data = (order_id, animal_id, quantity, unit_price)
        try:
            cur.execute(sql, data)
            conn.commit()  
            messages.success(request, f'Деталь заказа успешно добавлена!')
            return redirect('order_detail_animal_page')  
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении детали заказа: {e}')
            return redirect('page_order_detail_animal') 
        finally:
            cur.close()
            conn.close()
    else:
        orders = Order.objects.all()  
        animals = Animal.objects.all()  
        return render(request, 'zoo/orderDetailAnimal/pageC_orderDetailAnimal.html', {'orders': orders, 'animals': animals})
def delete_order_detail_animal(request, order_detail_id):
    if request.method == 'POST':
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = "DELETE FROM order_details_animals WHERE order_detail_id = %s"
        try:
            cur.execute(sql, (order_detail_id,))
            conn.commit()
            messages.success(request, f'Деталь заказа с ID {order_detail_id} успешно удалена!')
            return redirect('order_detail_animal_page')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении детали заказа: {e}')
            return redirect('order_detail_animal_page')  
        finally:
            cur.close()
            conn.close()
    else:
        return render(request, 'zoo/orderDetailAnimal/pageD_orderDetailAnimal.html', {'order_detail_id': order_detail_id})
def update_order_detail_animal(request, order_detail_id):
    if request.method == 'POST':
        order_id = request.POST.get('order')
        animal_id = request.POST.get('animal')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')
        order_detail_id = request.POST.get('order_detail_id')
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = """
            UPDATE order_details_animals
            SET order_id = %s, animal_id = %s, quantity = %s, unit_price = %s
            WHERE order_detail_id = %s
        """
        data = (order_id, animal_id, quantity, unit_price, order_detail_id)
        try:
            cur.execute(sql, data)
            conn.commit()
            messages.success(request, f'Деталь заказа с ID {order_detail_id} успешно обновлена!')
            return redirect('order_detail_animal_page')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении детали заказа: {e}')
            return redirect('order_detail_animal_page')  
        finally:
            cur.close()
            conn.close()
    else:
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM order_details_animals WHERE order_detail_id = %s", (order_detail_id,))
        order_detail_animal = cur.fetchone()
        cur.close()
        conn.close()
        order_detail_animal_data = {
            'order_detail_id': order_detail_animal[0],
            'order_id': order_detail_animal[1],
            'animal_id': order_detail_animal[2],
            'quantity': order_detail_animal[3],
            'unit_price': order_detail_animal[4],
        }
        orders = Order.objects.all()
        animals = Animal.objects.all()
        return render(request, 'zoo/orderDetailAnimal/pageU_orderDetailAnimal.html', {'order_detail_animal': order_detail_animal_data, 'orders': orders, 'animals': animals, 'order_detail_id': order_detail_id})

def OrderDetailProduct_page(request):
    conn = psycopg2.connect(
        database='Zoo', 
        user='postgres',
        password='2005', 
        host='localhost', 
        port='5432'
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM order_details_products")
    order_detail_products = cur.fetchall()
    cur.close()
    conn.close()
    paginator = Paginator(order_detail_products, 10)  
    page = request.GET.get('page')
    try:
        order_detail_products = paginator.page(page)
    except PageNotAnInteger:
        order_detail_products = paginator.page(1)
    except EmptyPage:
        order_detail_products = paginator.page(paginator.num_pages)
    context = {'order_detail_products': order_detail_products}
    return render(request, 'zoo/orderDetailProduct/page_orderDetailProduct.html', context)
def C_order_detail_product(request):
    if request.method == 'POST':
        order_id = request.POST.get('order')
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')

        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = """
            INSERT INTO order_details_products (order_id, product_id, quantity, unit_price) 
            VALUES (%s, %s, %s, %s)
        """
        data = (order_id, product_id, quantity, unit_price)
        try:
            cur.execute(sql, data)
            conn.commit()  
            messages.success(request, f'Деталь заказа успешно добавлена!')
            return redirect('order_detail_product_page')  
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении детали заказа: {e}')
            return redirect('page_order_detail_product') 
        finally:
            cur.close()
            conn.close()
    else:
        orders = Order.objects.all()  
        products = Product.objects.all()  
        return render(request, 'zoo/order_detail_product/pageC_order_detail_product.html', {'orders': orders, 'products': products})
def delete_order_detail_product(request, order_detail_id):
    if request.method == 'POST':
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = "DELETE FROM order_details_products WHERE order_detail_id = %s"
        try:
            cur.execute(sql, (order_detail_id,))
            conn.commit()
            messages.success(request, f'Деталь заказа с ID {order_detail_id} успешно удалена!')
            return redirect('order_detail_product_page')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении детали заказа: {e}')
            return redirect('order_detail_product_page') 
        finally:
            cur.close()
            conn.close()
    else:
        return render(request, 'zoo/orderDetailProduct/pageD_orderDetailProduct.html', {'order_detail_id': order_detail_id})
def update_order_detail_product(request, order_detail_id):
    if request.method == 'POST':
        order_id = request.POST.get('order')
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')
        order_detail_id = request.POST.get('order_detail_id')
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = """
            UPDATE order_details_products
            SET order_id = %s, product_id = %s, quantity = %s, unit_price = %s
            WHERE order_detail_id = %s
        """
        data = (order_id, product_id, quantity, unit_price, order_detail_id)
        try:
            cur.execute(sql, data)
            conn.commit()
            messages.success(request, f'Деталь заказа с ID {order_detail_id} успешно обновлена!')
            return redirect('order_detail_product_page')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении детали заказа: {e}')
            return redirect('order_detail_product_page') 
        finally:
            cur.close()
            conn.close()

    else:
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM order_details_products WHERE order_detail_id = %s", (order_detail_id,))
        order_detail_product = cur.fetchone()
        cur.close()
        conn.close()
        order_detail_product_data = {
            'order_detail_id': order_detail_product[0],
            'order_id': order_detail_product[1],
            'product_id': order_detail_product[2],
            'quantity': order_detail_product[3],
            'unit_price': order_detail_product[4],
        }
        orders = Order.objects.all()
        products = Product.objects.all()  
        return render(request, 'zoo/orderDetailProduct/pageU_orderDetailProduct.html', {'order_detail_product': order_detail_product_data, 'orders': orders, 'products': products, 'order_detail_id': order_detail_id})

def Product_page(request):
    conn = psycopg2.connect(
        database='Zoo', 
        user='postgres',
        password='2005', 
        host='localhost', 
        port='5432'
    )
    cur = conn.cursor()

    cur.execute("SELECT * FROM products")

    products = cur.fetchall()

    cur.close()
    conn.close()
    paginator = Paginator(products, 10)  
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'products': products}
    return render(request, 'zoo/product/page_product.html', context)
def C_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        image_url = request.POST.get('image_url')

        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        sql = """
            INSERT INTO products (name, category_id, description, price, stock_quantity, image_url) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (name, category_id, description, price, stock_quantity, image_url)

        try:
            cur.execute(sql, data)
            conn.commit()  
            messages.success(request, f'Продукт "{name}" успешно добавлен!')
            return redirect('product_page')  
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении продукта: {e}')
            return redirect('page_product') 
        finally:
            cur.close()
            conn.close()

    else:
        categories = Category.objects.all() 
        return render(request, 'zoo/product/pageC_product.html', {'categories': categories})
def delete_product(request, product_id):
    if request.method == 'POST':
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = "DELETE FROM products WHERE product_id = %s"
        try:
            cur.execute(sql, (product_id,))
            conn.commit()
            messages.success(request, f'Продукт с ID {product_id} успешно удален!')
            return redirect('product_page')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении продукта: {e}')
            return redirect('product_page')  
        finally:
            cur.close()
            conn.close()

    else:
        return render(request, 'zoo/product/pageD_product.html', {'product_id': product_id})
def update_product(request, product_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        image_url = request.POST.get('image_url')
        product_id = request.POST.get('product_id')
        
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        sql = """
            UPDATE products
            SET name = %s, category_id = %s, description = %s, price = %s, stock_quantity = %s, image_url = %s
            WHERE product_id = %s
        """
        data = (name, category_id, description, price, stock_quantity, image_url, product_id)
        try:
            cur.execute(sql, data)
            conn.commit()
            messages.success(request, f'Продукт с ID {product_id} успешно обновлен!')
            return redirect('product_page')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении продукта: {e}')
            return redirect('product_page')
        finally:
            cur.close()
            conn.close()

    else:
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cur.fetchone()
        cur.close()
        conn.close()
        product_data = {
            'product_id': product[0],
            'name': product[1],
            'category_id': product[2],
            'description': product[3],
            'price': product[4],
            'stock_quantity': product[5],
            'image_url': product[6],
        }

        categories = Category.objects.all()
        
        return render(request, 'zoo/product/pageU_product.html', {'product': product_data, 'categories': categories, 'product_id': product_id}) 

def Supply_page(request):
    conn = psycopg2.connect(
        database='Zoo', 
        user='postgres',
        password='2005', 
        host='localhost', 
        port='5432'
    )
    cur = conn.cursor()

    cur.execute("SELECT * FROM supplies")

    supplies = cur.fetchall()
    cur.close()
    conn.close()
    paginator = Paginator(supplies, 10)  
    page = request.GET.get('page')
    try:
        supplies = paginator.page(page)
    except PageNotAnInteger:
        supplies = paginator.page(1)
    except EmptyPage:
        supplies = paginator.page(paginator.num_pages)
    context = {'supplies': supplies}
    return render(request, 'zoo/supply/page_supplier.html', context)
def C_supply(request):
    if request.method == 'POST':
        # Получение данных из формы
        product_id = request.POST.get('product')
        supplier_id = request.POST.get('supplier')
        supply_date = request.POST.get('supply_date')
        quantity = request.POST.get('quantity')

        # Подключение к базе данных
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        # Создание SQL-запроса для вставки данных
        sql = """
            INSERT INTO supplies (
            product_id, supplier_id, 
            supply_date, quantity) 
            VALUES (%s, %s, %s, %s)
        """
        data = (product_id, supplier_id, supply_date, quantity)

        # Выполнение запроса
        try:
            cur.execute(sql, data)
            conn.commit()  # Сохранение изменений в базе данных
            messages.success(request, f'Поставка успешно добавлена!')
            return redirect('supply_page')  
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении поставки: {e}')
            return redirect('page_supply') 
        finally:
            cur.close()
            conn.close()

    else:
        # Отображение формы добавления поставки
        products = Product.objects.all()  # Получение всех продуктов из модели
        suppliers = Supplier.objects.all()  # Получение всех поставщиков из модели
        return render(request, 'zoo/supply/pageC_supply.html', {'products': products, 'suppliers': suppliers})
def delete_supply(request, supply_id):
    if request.method == 'POST':
        # Подключение к базе данных
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        # Выполнение запроса на удаление
        sql = "DELETE FROM supplies WHERE supply_id = %s"
        try:
            cur.execute(sql, (supply_id,))
            conn.commit()
            messages.success(request, f'Поставка с ID {supply_id} успешно удалена!')
            return redirect('supply_page')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении поставки: {e}')
            return redirect('supply_page')  # Перенаправление на страницу с животными
        finally:
            cur.close()
            conn.close()

    else:
        # Отображение подтверждения удаления
        return render(request, 'zoo/supply/delete_supply.html', {'supply_id': supply_id})
def update_supply(request, supply_id):
    if request.method == 'POST':
        # Получение данных из формы
        product_id = (
            request.POST.get('product'))
        supplier_id = (
            request.POST.get('supplier'))
        supply_date = (
            request.POST.get('supply_date'))
        quantity = (
            request.POST.get('quantity'))
        supply_id = (
            request.POST.get('supply_id'))  # Получаем supply_id из формы

        # Подключение к базе данных
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        # Создание SQL-запроса для обновления данных
        sql = """
            UPDATE supplies
            SET product_id = %s, supplier_id = %s, supply_date = %s, quantity = %s
            WHERE supply_id = %s
        """
        data = (product_id, supplier_id, supply_date, quantity, supply_id)

        # Выполнение запроса
        try:
            cur.execute(sql, data)
            conn.commit()
            messages.success(request, f'Поставка с ID {supply_id} успешно обновлена!')
            return redirect('supply_page')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении поставки: {e}')
            return redirect('supply_page')  # Перенаправление на страницу с животными
        finally:
            cur.close()
            conn.close()

    else:
        # Подключение к базе данных
        conn = psycopg2.connect(
            database='Zoo',
            user='postgres',
            password='2005',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        # Выполнение запроса для получения данных поставки
        cur.execute("SELECT * FROM supplies WHERE supply_id = %s", (supply_id,))
        supply = cur.fetchone()
        cur.close()
        conn.close()

        # Преобразование данных из кортежа в словарь
        supply_data = {
            'supply_id': supply[0],
            'product_id': supply[1],
            'supplier_id': supply[2],
            'supply_date': supply[3],
            'quantity': supply[4],
        }

        products = Product.objects.all()
        suppliers = Supplier.objects.all() 
        return render(request, 'zoo/supply/pageU_supply.html', {'supply': supply_data, 'products': products, 'suppliers': suppliers, 'supply_id': supply_id})







