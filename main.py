# 3.10 动态补丁，确保在任何库使用 time.clock 时替换为 time.perf_counter
# import time
# if not hasattr(time, 'clock'):
#     time.clock = time.perf_counter

# import collections
# if not hasattr(collections, 'Hashable'):
#     from collections.abc import Hashable
#     collections.Hashable = Hashable
    
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# 创建ChatBot实例
ai_bot = ChatBot(
    "ai",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///database.sqlite3"  # 使用SQLite数据库保存训练结果
)

# 检查数据库是否为空
if ai_bot.storage.count() == 0:
    # 使用ChatterBotCorpusTrainer进行训练
    trainer = ChatterBotCorpusTrainer(ai_bot)
    
    # 合并训练语料库
    trainer.train(
        # "chatterbot.corpus.chinese",
        "./custom_corpus/xiaohuangji.yml"
    )
    print("训练完成并保存到数据库。")
else:
    print("加载已训练的模型。")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/getChatBotResponse")
def get_bot_response(msg: str):
    start_time = time.time()
    response = ai_bot.get_response(msg)
    end_time = time.time()
    print(f"处理消息'{msg}'耗时: {end_time - start_time:.2f}秒")
    return str(response)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9988)
