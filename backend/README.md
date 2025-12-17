# 本地多模型大语言模型交互系统

本项目是一个支持本地多模型部署的大语言模型交互系统，后端基于 **Python 3.10 + Flask**，前端使用 **Vue 3** 构建并打包为 `dist` 静态资源。系统支持在 **Windows** 和 **Linux** 上运行，可通过本地部署或 Docker 部署两种方式启动，提供统一的 Web 页面与多个开源大模型进行对话和文档问答。

---

## 功能简介

- 支持接入多个本地大语言模型：九格、Baichuan2、Mistral、Qwen3、Yi、Zephyr 等。
- 在同一个 Web 页面中自由切换当前使用的模型。
- 支持多轮对话、会话历史管理。
- 支持上传文档后进行基于文档内容的问答与摘要。
- 支持调节模型生成参数（温度、top_p 等），控制回答风格与长度。
- 支持对话历史导出，便于保存与复现。
- 支持本地部署和 Docker 部署，适合个人实验和局域网私有化使用。

---


> 默认仓库已经包含打包好的前端 `dist/`，普通用户不需要自己再执行前端构建。只有在你修改了前端 Vue 代码时，才需要重新 `npm run build` 并覆盖该目录。

---

## 模型下载与放置路径说明

系统默认从本地目录加载六个大语言模型，请 **务必在启动前下载好模型权重，并放在对应目录**：

| 模型名称                | 本地目录（相对项目根目录） | 参考下载链接                                                                                          |
| ------------------- | ------------- | ----------------------------------------------------------------------------------------------- |
| 九格                  | `./9G7B_MHA`  | [维基-启元实验室/九格通用基础大模型](https://www.osredm.com/jiuyuan/CPM-9G-8B##202565九格模型适配昇腾npu)               |
| Baichuan2           | `./baichuan`  | [baichuan-inc/Baichuan2](https://github.com/baichuan-inc/Baichuan2?tab=readme-ov-file#模型介绍)     |
| Mistral-7B-Instruct | `./mistral`   | [mistralai/Mistral-7B-Instruct-v0.3](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) |
| Qwen3-8B            | `./qwen`      | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B)                                           |
| Yi 系列               | `./Yi`        | [Yi-1.5 Collection](https://huggingface.co/collections/01-ai/yi-15-2024-05)                     |
| Zephyr-7B-Alpha     | `./zephyr`    | [HuggingFaceH4/zephyr-7b-alpha](https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha)           |

如果更改模型目录名称或路径，需要同时修改对应的模型加载代码（位于 `model_manager/` 或相关脚本中）。

---

## 环境要求

**硬件建议：**

* 64 位多核 CPU（推荐 ≥ 4 cores）
* 内存 ≥ 16 GB（视模型数量和并发情况可适当提高）
* 磁盘空间：至少预留数十 GB 用于六个模型和运行日志
* 可选：支持 CUDA 的 GPU，用于加速推理（若代码中已开启 GPU 逻辑）

**软件环境：**

* Python 3.10
* Redis 服务（本地或远程，默认连接本地服务，可在 `extensions.py` 等配置文件中调整）
* Conda / Miniconda（用于本地部署）
* Docker 与 Docker Compose（用于容器部署）

---

## 本地部署（Conda）

本地部署适合开发调试和单机实验使用。

1. **安装依赖工具**

   * 安装 Anaconda 或 Miniconda
   * 安装并启动 Redis（默认本地运行即可）

2. **创建并激活 Conda 环境**

   在项目根目录执行：

   ```bash
   conda env create -f environment.yml

   conda activate backend
   ```

3. **准备模型**

   按“模型下载与放置路径说明”章节，将六个模型下载到各自目录下。

4. **启动后端服务**

   ```bash
   python app.py
   ```

   默认会在本机 `5000` 端口启动服务。

5. **访问系统**

   打开浏览器，访问：

   ```text
   http://127.0.0.1:5000
   ```

   如果运行在远程服务器并希望在局域网访问，可将绑定地址修改为 `0.0.0.0`，并在浏览器中使用服务器 IP 替代 `127.0.0.1`。

---

## Docker 部署

Docker 部署适合在不同机器、不同操作系统之间快速复现一致的环境。

1. **安装 Docker 与 Docker Compose**

   * Windows 建议使用 Docker Desktop（确保启用 Linux 容器模式）
   * Linux 直接安装 Docker Engine 和 docker-compose 插件

2. **准备 Redis 服务**

   * 可以在宿主机安装 Redis 并启动
   * 或使用你已有的 Redis 实例
   * 确保 Redis 地址与端口与代码中配置一致

3. **准备模型目录**

   与本地部署相同，将六个模型下载到项目根目录下对应的目录中。
   `docker-compose.yml` 会将这些目录挂载到容器内，供 Flask 应用加载。

4. **构建并启动容器**

   在项目根目录执行：

   ```bash
   docker compose up -d --build
   ```

   该命令会根据 `Dockerfile` 和 `requirements_docker.txt` 构建镜像，并后台启动服务。

5. **查看状态与日志（可选）**

   ```bash
   docker compose ps
   docker compose logs -f
   ```

6. **访问系统**

   同样在浏览器访问：

   ```text
   http://127.0.0.1:5000
   ```

   部署在服务器上时，将 `127.0.0.1` 替换为服务器 IP 或域名。

7. **停止服务**

   ```bash
   docker compose down
   ```


## 前端修改与二次开发说明

如果你需要修改前端界面样式或交互逻辑，可以在原 Vue 工程中进行开发，并重新构建前端资源。典型流程为：

1. 在前端项目中开发并测试（`npm run dev`）。
2. 使用 `npm run build` 生成新的 `dist` 目录。
3. 将生成的 `dist` 覆盖本仓库根目录下同名目录，即可被 Flask 作为静态资源提供。

普通使用和后端开发一般不需要修改前端，可直接使用仓库中已打包好的 `dist`。

---
