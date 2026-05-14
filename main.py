from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import init_db, get_videos, add_video, add_order, get_orders
from translations import translations
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_telegram_notification(name: str, contact: str, date: str, comments: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
        
    text = (
        f"🚨 <b>Новый заказ / New Booking!</b>\n\n"
        f"<b>Имя:</b> {name}\n"
        f"<b>Контакты:</b> {contact}\n"
        f"<b>Даты:</b> {date}\n"
        f"<b>Комментарий:</b> {comments}"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json=payload)
        except Exception as e:
            print(f"Ошибка при отправке в Telegram: {e}")


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
    await send_telegram_notification(name, contact, date, comments)
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
