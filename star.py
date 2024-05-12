from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, or_
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, joinedload

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)


class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    store_id = Column(Integer, ForeignKey('stores.id'))
    quantity = Column(Integer)
    total_price = Column(Float)
    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    store = relationship("Store", back_populates="sales")


Product.sales = relationship("Sale", order_by=Sale.id, back_populates="product")
Customer.sales = relationship("Sale", order_by=Sale.id, back_populates="customer")
Store.sales = relationship("Sale", order_by=Sale.id, back_populates="store")

# ======================================= C - 创建 ========================================
engine = create_engine('sqlite:///star_schema.db')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# 假设我们已经有了一个活动的数据库会话 session

# 为 Product 表增加数据
products = [
    Product(name='product1', price=100),
    Product(name='product2', price=200),
    Product(name='product3', price=300),
]
session.add_all(products)

# 为 Customer 表增加数据
customers = [
    Customer(name='Bill', email='Bill@example.com'),
    Customer(name='Jack', email='Jack@example.com'),
    Customer(name='Lucy', email='Lucy@example.com'),
]
session.add_all(customers)

# 为 Store 表增加数据
stores = [
    Store(name='store1', location='store1 location1'),
    Store(name='store2', location='store1 location2'),
    Store(name='store3', location='store1 location3'),
]
session.add_all(stores)

# 为 Sale 表增加数据，关联先前创建的 Product, Customer, Store
sales = [
    Sale(product=products[0], customer=customers[0], store=stores[0], quantity=1, total_price=products[0].price),
    Sale(product=products[1], customer=customers[0], store=stores[0], quantity=1, total_price=products[1].price),
    Sale(product=products[1], customer=customers[0], store=stores[1], quantity=1, total_price=products[1].price),
    Sale(product=products[2], customer=customers[0], store=stores[0], quantity=1, total_price=products[2].price),
    Sale(product=products[0], customer=customers[1], store=stores[0], quantity=1, total_price=products[0].price),
    Sale(product=products[1], customer=customers[1], store=stores[0], quantity=1, total_price=products[1].price),
    Sale(product=products[2], customer=customers[1], store=stores[0], quantity=1, total_price=products[2].price),
    Sale(product=products[0], customer=customers[2], store=stores[0], quantity=1, total_price=products[0].price),
    Sale(product=products[1], customer=customers[2], store=stores[0], quantity=1, total_price=products[1].price),
    Sale(product=products[2], customer=customers[2], store=stores[0], quantity=1, total_price=products[2].price),
]
session.add_all(sales)
session.commit()

# ======================================= R - 读取 ========================================
# 用户输入的查询字符串
query_string = "Bill product2"

# 将查询字符串按空格分割成关键字列表
keywords = query_string.split()

# 构建查询，连接所有相关的表
query = session.query(Sale, Customer, Product, Store) \
    .join(Sale.customer) \
    .join(Sale.product) \
    .join(Sale.store) \
    .options(
    joinedload(Sale.customer),
    joinedload(Sale.product),
    joinedload(Sale.store)
)

# 对每个关键字构建过滤条件，并使用 or_() 组合它们
for keyword in keywords:
    query = query.filter(or_(
        Customer.name.ilike(f'%{keyword}%'),
        Product.name.ilike(f'%{keyword}%'),
        Store.name.ilike(f'%{keyword}%')
    ))

print(query)
# 执行查询
results = query.all()

# 遍历查询结果并打印
for sale, customer, product, store in results:
    print(f"Sale ID: {sale.id}, Customer: {customer.name}, Product: {product.name}, Store: {store.name}, Total Price: {sale.total_price}")