from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import init_db, get_videos, add_video, add_order, get_orders # Импортируем базу

app = FastAPI()

# Инициализируем базу данных при запуске
init_db()

# Указываем, где лежат картинки и стили
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Данные для галереи
    videos_from_db = get_videos()
    # Проверяем, пришел ли пользователь после отправки заявки
    success = request.query_params.get("success")
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"videos": videos_from_db, "success": success}
    )

@app.post("/submit-order")
async def handle_submit_order(
    name: str = Form(...), 
    contact: str = Form(...), 
    date: str = Form(""), 
    comments: str = Form("")
):
    add_order(name, contact, date, comments)
    # Возвращаем пользователя на главную с параметром success=1
    return RedirectResponse(url="/?success=1#booking-form", status_code=303)

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    # Получаем заявки для отображения
    orders = get_orders()
    return templates.TemplateResponse(request=request, name="admin.html", context={"orders": orders})

@app.post("/admin/add")
async def handle_add_video(title: str = Form(...), url: str = Form(...)):
    add_video(title, url)
    return RedirectResponse(url="/", status_code=303)
