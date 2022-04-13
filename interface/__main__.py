from .main import app
from fastapi.openapi.docs import get_redoc_html


html = get_redoc_html(
    openapi_url="./openapi",
    title=app.title + " - ReDoc",
    # redoc_js_url="/static/redoc.standalone.js",
)

print(html.body)
print(app.openapi())
