# 对应 Java: com.sky.SkyApplication
from sky.config.web_mvc_configuration import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("sky.main:app", host="0.0.0.0", port=8080, reload=True)
