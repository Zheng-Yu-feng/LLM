FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

COPY requirements_docker.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 再复制项目代码（后端 + dist 等）
COPY . /app

# 声明模型目录为挂载点（只是声明，不会往镜像里塞模型）
VOLUME ["/app/9G7B_MHA", "/app/baichuan", "/app/mistral", "/app/qwen", "/app/Yi", "/app/zephyr"]

# 对外端口
EXPOSE 5000

# 启动 Flask（确认 app.py 里是 host="0.0.0.0"）
CMD ["python", "app.py"]
