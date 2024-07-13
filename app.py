from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

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

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook


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

# @router_v1.put('/students/{stu_id}')
# async def update_student(stu_id: int, response: Response,db: Session = Depends(get_db)):
#     response.status_code = 404

# @router_v1.post('/students')
# async def create_student(stu: dict, response: Response, db: Session = Depends(get_db)):
#     # TODO: Add validation
#     newstu = models.Book(fname=stu['fname'], lname=stu['lname'], stuid=stu['id'], studob=stu['dob'], stusex=stu['sex'])
#     db.add(newstu)
#     db.commit()
#     db.refresh(newstu)
#     response.status_code = 201
#     return newstu


# @router_v1.patch('/books/{book_id}')
# async def update_book(book_id: int, book: dict, db: Session = Depends(get_db)):
#     pass

# @router_v1.delete('/books/{book_id}')
# async def delete_book(book_id: int, db: Session = Depends(get_db)):
#     pass

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=3000)
