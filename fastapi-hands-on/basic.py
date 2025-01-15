from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

news = {
    1: {
        "id": 1,
        "title": "Top 10 programming languages",
        "content": "Python is the most popular programming language according to the TIOBE index. Other popular",
        "author": "Kalim"
    },
    2: {
        "id": 2,
        "title": "LLM race in modern era",
        "content": "Content on modern LLM models both close & open source",
        "author": "Ibrahim"
    },
    3: {
        "id": 3,
        "title": "Latest LLM models from Mistral!!!",
        "content": "Content on modern LLM models both close & open",
        "author": "Kalim"
    },
    4: {
        "id": 4,
        "title": "What's the Google calls on LLM!!",
        "content": "Content on modern LLM models both close & open",
        "author": "Kalim"
    },
}

class News(BaseModel):
    title: str
    content: str | None = None
    author: str

@app.get("/news")
def all_news():
    return news

@app.get("/news/author/{author}")
def news_by_author(author: str):
    filtered_news = [item for item in news.values() if item["author"].lower() == author.lower()]
    return filtered_news

@app.get("/news/{id}")
def news_by_id(id: int):
    if id not in news:
        return {"error": f"News with id {id} not found"}
    return news[id]

@app.get("/news/search")
def news_by_title(title_contains: str):
    filtered_news = [item for item in news.values() if title_contains.lower() in item["title"].lower()]
    if not filtered_news:
        return {"data": f"No news found with title containing '{title_contains}'"}
    return filtered_news

@app.get("/news/author-title/{author}")
def news_filter_by_author_title(author: str, title_contains: str = None):
    filtered_news = [item for item in news.values() if item["author"].lower() == author.lower()]
    if title_contains:
        filtered_news = [item for item in filtered_news if title_contains.lower() in item["title"].lower()]
        if not filtered_news:
            return {"data": f"No news found from author '{author}' with title containing '{title_contains}'"}
    return filtered_news

@app.post("/create-news")
def create_news(response_news: News):
    new_id = max(news.keys()) + 1
    news[new_id] = {
        "id": new_id,
        "title": response_news.title,
        "content": response_news.content,
        "author": response_news.author
    }
    return news[new_id]

@app.get("/")
def hearbeat():
    return {"message": "I'm up and running!"}

if __name__ == '__main__':
    uvicorn.run("basic:app", host='localhost', port=8000, reload=True)
