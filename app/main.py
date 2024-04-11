from app.routes.task_7 import CustomMiddleware
from fastapi import FastAPI
#import psycopg2

app = FastAPI()
app.add_middleware(CustomMiddleware)

# try:
#     conn = psycopg2.connect(
#         host='localhost',
#         database='task11',
#         port=5432,
#         user='postgres',
#         password='Q12tn16l'
#     )
 
#     cursor = conn.cursor()
#     print("Connection established.")
 
# except Exception as err:
#     print("Something went wrong.")
#     print(err)


from app.routes.task_1 import router as r_1
app.include_router(r_1)

from app.routes.task_2 import router as r_2
app.include_router(r_2)

from app.routes.task_3 import router as r_3
app.include_router(r_3)

from app.routes.task_4 import router as r_4
app.include_router(r_4)

from app.routes.task_5 import router as r_5
app.include_router(r_5)

from app.routes.task_6 import router as r_6
app.include_router(r_6)

from app.routes.task_8 import router as r_8
app.include_router(r_8)