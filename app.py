from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import joinedload

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

class OrderItemCreate(BaseModel):
    menuId: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    description: str
    orderItems: List[OrderItemCreate]

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'], detail=book['detail'], synopsis=book['synopsis'], category=book['category'],image=book['image'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.patch('/books/{book_id}')
async def update_book(book_id: str, book: dict, response: Response, db: Session = Depends(get_db)):
    bk = db.query(models.Book).filter(models.Book.id == book_id).first()
    if (bk is None):
        response.status_code = 400
        return {
            "message" : "Book's ID not found."
        }
    keys = ["id", "title", "author", "year", "is_published", "detail", "synopsis", "category", "image"]
    for key in keys:
        if key in book:
            setattr(bk, key, book[key])
    db.commit()
    response.status_code = 201
    return {
        "message" : "Book's info edited successfully"
    }

@router_v1.delete('/books/{book_id}')
async def delete_book(book_id: str, response: Response, db: Session = Depends(get_db)):
    bk = db.query(models.Book).filter(models.Book.id == book_id).first()
    if (bk is not None):
        db.delete(bk)
        db.commit()
        response.status_code = 201
        return {
            "message" : "delete info successfully"
        }
    response.status_code = 400
    return {
        "message" : "Book's ID not found."
    }




@router_v1.get('/menu')
async def get_menu(db: Session = Depends(get_db)):
    return db.query(models.Beverages).all()

@router_v1.get('/menu/{menu_id}')
async def get_menu(menu_id: int, db: Session = Depends(get_db)):
    return db.query(models.Beverages).filter(models.Beverages.id == menu_id).first()

@router_v1.post('/menu')
async def create_menu(menu: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newMenu = models.Beverages(name=menu['name'], price=menu['price'], menuImage=menu['menuImage'])
    db.add(newMenu)
    db.commit()
    db.refresh(newMenu)
    response.status_code = 201
    return newMenu

@router_v1.patch('/menu/{menu_id}')
async def update_menu(menu_id: str, menu: dict, response: Response, db: Session = Depends(get_db)):
    bk = db.query(models.Beverages).filter(models.Beverages.id == menu_id).first()
    if (bk is None):
        response.status_code = 400
        return {
            "message" : "Menu's ID not found."
        }
    keys = ["id", "name", "price", "menuImage"]
    for key in keys:
        if key in menu:
            setattr(bk, key, menu[key])
    db.commit()
    response.status_code = 201
    return {
        "message" : "Menu's info edited successfully"
    }

@router_v1.delete('/menu/{id}')
async def delete_book(id: str, response: Response, db: Session = Depends(get_db)):
    bk = db.query(models.Beverages).filter(models.Beverages.id == id).first()
    if (bk is not None):
        db.delete(bk)
        db.commit()
        response.status_code = 201
        return {
            "message" : "delete info successfully"
        }
    response.status_code = 400
    return {
        "message" : "Menu's ID not found."
    }


@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    return db.query(models.Students).all()

@router_v1.get('/students/{stu_id}')
async def get_student(stu_id: str, db: Session = Depends(get_db)):
    student = db.query(models.Students).filter(models.Students.stu_id == stu_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
    
@router_v1.post('/students')
async def create_student(stu: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newStu = models.Students(stu_id=stu['stu_id'], fname=stu['fname'], lname=stu['lname'], dob=stu['dob'], gender=stu['gender'])
    db.add(newStu)
    db.commit()
    db.refresh(newStu)
    response.status_code = 201
    return newStu

@router_v1.delete('/students/{stu_id}')
async def delete_student(stu_id: str, response: Response, db: Session = Depends(get_db)):
    student = db.query(models.Students).filter(models.Students.stu_id == stu_id).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()

    response.status_code = 204
    return {
        "detail" : "Student deleted successfully"
    }

@router_v1.patch('/students/{student_id}')
async def update_student(student_id: str, student: dict, response: Response,db: Session = Depends(get_db)):
    stu = db.query(models.Students).filter(models.Students.stu_id == student_id).first()
    if stu is None:
        response.status_code = 400
        return {
            "message" : "Student not found"
        }
    stu.stu_id = student["stu_id"] if "stu_id" in student else stu.stu_id
    stu.fname = student["fname"] if "fname" in student else stu.fname
    stu.lname = student["lname"] if "lname" in student else stu.lname
    stu.dob = student["dob"] if "dob" in student else stu.dob
    stu.gender = student["gender"] if "gender" in student else stu.gender

    db.commit()

    response.status_code = 201
    return stu

@router_v1.get('/orders')
async def get_orders(db: Session = Depends(get_db)):
    # ดึงข้อมูลคำสั่งซื้อพร้อมกับโหลดข้อมูล order_items และ menu
    orders = db.query(models.Order).options(
        joinedload(models.Order.order_items).joinedload(models.OrderItem.menu)
    ).all()

    result = []
    for order in orders:
        result.append({
            "id": order.id,
            "date": order.date,
            "description": order.description,
            "total_price": order.total_price,
            "order_items": [
                {
                    "id": item.id,
                    "order_id": item.order_id,
                    "menu_id": item.menu_id,
                    "quantity": item.quantity,
                    "price": item.price,
                    "total_price": item.total_price,
                    "menu": {
                        "id": item.menu.id,
                        "name": item.menu.name,
                        "price": item.menu.price,
                    }
                } for item in order.order_items
            ]
        })

    return result



@router_v1.get('/orders/{order_id}')
async def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).options(
        joinedload(models.Order.order_items).joinedload(models.OrderItem.menu)
    ).filter(models.Order.id == order_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    result = {
        "id": order.id,
        "date": order.date,
        "description": order.description,
        "total_price": order.total_price,
        "order_items": [
            {
                "id": item.id,
                "order_id": item.order_id,
                "menu_id": item.menu_id,
                "quantity": item.quantity,
                "price": item.price,
                "total_price": item.total_price,
                "menu": {
                    "id": item.menu.id,
                    "name": item.menu.name,
                    "price": item.menu.price
                }
            } for item in order.order_items
        ]
    }
    return result


@router_v1.post('/orders')
async def create_order(order: OrderCreate, response: Response, db: Session = Depends(get_db)):
    total_price = sum(item.price * item.quantity for item in order.orderItems)
    
    new_order = models.Order(
        description=order.description,
        total_price=total_price
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order.orderItems:
        order_item = models.OrderItem(
            order_id=new_order.id,
            menu_id=item.menuId,
            quantity=item.quantity,
            price=item.price,
            total_price=item.price * item.quantity
        )
        db.add(order_item)
        print(f"Added OrderItem: {order_item}")  # Debugging line

    db.commit()
    response.status_code = 201
    return {"id": new_order.id}

@router_v1.delete('/orders/{order_id}')
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=3000)
