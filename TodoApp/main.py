from fastapi import FastAPI,Request,status
from .models  import Base
from .database import engine
from .routers import auth,todos,admin,users
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount('/static',StaticFiles(directory="TodoApp/static"),name='static')



@app.get("/")
def load_home(request:Request):
    return RedirectResponse(url='todos/todo-page',status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
