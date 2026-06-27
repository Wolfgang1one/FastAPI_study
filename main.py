from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/news/{news_id}")
async def get_news_id(
        news_id: int = Path(
            ...,
            gt=1,
            lt=100,
            description="新闻分类id"
        )
):
    return {"news_id": news_id}


@app.get("/news/{news_name}")
async def get_news_name(
        news_name: str = Path(
            ...,
            min_length=2,
            max_length=10,
            description="新闻分类名称"
        )
):
    return {"news_name": news_name}
