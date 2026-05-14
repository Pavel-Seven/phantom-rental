from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import init_db, get_videos, add_video, add_order, get_orders
from translations import translations

app = FastAPI()

# Инициализируем базу данных при запуске
init_db()

# Указываем, где лежат картинки и стили
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, lang: str = "de"):
    if lang not in translations:
        lang = "de"
        
    t = translations[lang]
    success = request.query_params.get("success")
    
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"t": t, "lang": lang, "success": success}
    )

@app.post("/submit-order")
async def handle_submit_order(
    request: Request,
    name: str = Form(...), 
    contact: str = Form(...), 
    date: str = Form(""), 
    comments: str = Form("")
):
    add_order(name, contact, date, comments)
    lang = request.query_params.get("lang", "de")
    return RedirectResponse(url=f"/?lang={lang}&success=1#booking", status_code=303)

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    orders = get_orders()
    return templates.TemplateResponse(request=request, name="admin.html", context={"orders": orders})

@app.post("/admin/add")
async def handle_add_video(title: str = Form(...), url: str = Form(...)):
    add_video(title, url)
    return RedirectResponse(url="/", status_code=303)
