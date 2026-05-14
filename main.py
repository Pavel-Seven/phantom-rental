from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import init_db, get_videos # Импортируем нашу базу

app = FastAPI()

# Инициализируем базу данных при запуске
init_db()

# Указываем, где лежат картинки и стили
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Теперь берем данные из базы!
    videos_from_db = get_videos()
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"videos": videos_from_db}
    )

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse(request=request, name="admin.html")

@app.post("/admin/add")
async def handle_add_video(title: str = Form(...), url: str = Form(...)):
    from database import add_video
    add_video(title, url)
    return RedirectResponse(url="/", status_code=303)
