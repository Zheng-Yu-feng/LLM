from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
import uuid
import time
import tempfile, os
from werkzeug.utils import secure_filename
from model_manager import ModelManager
from extensions import db
from flask_migrate import Migrate
from models import Message
#from memory import SessionMemoryManager
from memory import RedisSessionMemoryManager
import chardet

def create_app():
    app = Flask(__name__, static_folder="dist", static_url_path="/")
    
    #app = Flask(__name__)
    app.secret_key = '123456'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    #CORS(app, resources={r"/*": {"origins": ["http://localhost:9100"]}}, supports_credentials=True)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    return app

app = create_app()

# model_name_or_path = 'baichuan'
# chatbot = ChatBot(model_name_or_path)
#memory_manager = SessionMemoryManager(memory_dir="session_memory")
memory_manager = RedisSessionMemoryManager(max_history=3, session_ttl=3600*24*30)
chatbot = ModelManager()

@app.route("/api/get_parameters", methods=["GET"])
def get_parameters():
    parameters = chatbot.parameters
    current_params = {
        "temperature": parameters["temperature"],
        "top_k": parameters["top_k"],
        "top_p": parameters["top_p"],
        "max_length": parameters["max_length"]
    }
    print(current_params)
    return jsonify(current_params)

#api
@app.route('/api/change_parameters', methods=['POST'])
def change_parameters():
    data = request.json
    chatbot.set_parameters(
        temperature=data.get('temperature'),
        top_p=data.get('top_p'),
        max_length=data.get('max_length'),
        top_k=data.get('top_k'),
        thinking=data.get('thinking')
    )
    return jsonify({'message': 'Parameters changed successfully'})

current_model = {"model":  "九格", "loading": False}
@app.route("/api/set_model", methods=["POST"])
def set_model():
    global current_model
    model_name = request.json.get("model")
    try:
        print(f"切换模型为：{model_name}")
        current_model["loading"] = True  # 开始加载
        if model_name in chatbot.model_classes_api:
            chatbot.set_api(model_name)
        else:
            chatbot.set_model(model_name)    # 假设这里是耗时操作
        current_model["model"] = model_name
        current_model["loading"] = False  # 加载完成
        return jsonify({"message": f"模型 {model_name} 切换成功"})
    except Exception as e:
        current_model["loading"] = False
        return jsonify({"error": str(e)}), 400
    finally:
        current_model["loading"] = False
    
@app.route("/api/get_model", methods=["GET"])
def get_model():
    return jsonify({
        "model": current_model["model"],
        "loading": current_model["loading"]
    })
    


@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def generate_response():
    print('~~~~~~~~~~~~~')
    if request.method == 'OPTIONS':
        # 预检请求处理
        response = make_response() #
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    data = request.json
    # messages = data.get('messages', [])
    # print("前端消息记录：",messages)
    max_length = data.get('max_length', 100000)
    current_message = data.get('currentMessage', '')
    user_id = request.cookies.get('user_id')
    model_type = data.get('model_type')
    print(f"模型类型：{model_type}")
    print(f"当前模型：{current_model['model']}")
    if not user_id:
        user_id = str(uuid.uuid4())
    
    print('~~~~~~~~~~~')
    print(f'{user_id}:{current_message}')
    print('~~~~~~~~~~~~~')
    if model_type != 'local':
        if current_model['model'] in chatbot.model_classes_api:
            history = memory_manager.get_context(user_id)
            history.extend([current_message])
            print(f"历史记录：{history}")
            response = chatbot.call_api_chat(history, params=None)
        else:
            response = "请选择api模型"
    else:
        if current_model['model'] in chatbot.model_classes:
            history = memory_manager.get_context(user_id)
            print(f"历史记录：{history}")
            response = chatbot.generate_response(history,current_message)
            # resp.set_cookie('user_id', user_id, httponly=True, secure=False, samesite='Lax', max_age=3600*24*30)
            memory_manager.save_message(user_id, 'user', current_message['content'])
            memory_manager.save_message(user_id, 'assistant', response)
        else:
            response = "请选择本地模型"
    
    
    resp = make_response(jsonify({'response': response, 'user_id': user_id}))
    resp.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
    resp.headers.add('Access-Control-Allow-Credentials', 'true')
    resp.set_cookie('user_id', user_id, httponly=True, secure=True, samesite='None', max_age=3600*24*30)
    print('<<<<<<<<<<<<<<<<<<<<<')
    print(f'bot: {user_id}->{response}')
    print('>>>>>>>>>>>>>>>>>>>>>>')
    print(f"Setting cookie: user_id={user_id}")
    return resp

@app.route('/api/upload', methods=['POST', 'OPTIONS'])
def upload():
    if request.method == 'OPTIONS':
        resp = make_response()
        resp.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        resp.headers.add('Access-Control-Allow-Credentials', 'true')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return resp

    f = request.files.get('file')
    if not f:
        return jsonify({'error': '请选择文件'}), 400

    filename = f.filename
    if not filename.lower().endswith(('.txt', '.md')):
        return jsonify({'error': '仅支持 TXT/MD 文本格式'}), 400

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        f.save(tmp.name)
        tmp_path = tmp.name
    try:
        text = open(tmp_path, 'r', encoding='utf-8', errors='ignore').read()
        print(f"上传文件内容：{text}")
    finally:
        os.unlink(tmp_path)

    user_id = request.cookies.get('user_id') or str(uuid.uuid4())
    #if user_id is first upload: init histories
    #chatbot.upload_file(user_id, text)
    memory_manager.save_message(user_id, 'user', "解析以下内容:\n"+text)
    resp = make_response(jsonify({
        'message': '上传成功',
        'text_preview': text[:200],
        'user_id': user_id
    }))
    resp.set_cookie('user_id', user_id, httponly=True, secure=False, samesite='None', max_age=30*24*3600)
    resp.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
    resp.headers.add('Access-Control-Allow-Credentials', 'true')
    return resp

# @app.route('/api/upload', methods=['POST', 'OPTIONS'])
# def upload():
#     # 处理 preflight 请求
#     if request.method == 'OPTIONS':
#         resp = make_response()
#         resp.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
#         resp.headers.add('Access-Control-Allow-Credentials', 'true')
#         resp.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         return resp

#     # 获取上传文件
#     f = request.files.get('file')
#     if not f:
#         return jsonify({'error': '请选择文件'}), 400

#     # 中文文件名处理：只替换非法字符，不删除中文
#     import re
#     filename = re.sub(r'[\\/*?:"<>|]', "_", f.filename)

#     # 文件类型检查
#     if not filename.lower().endswith(('.txt', '.md')):
#         return jsonify({'error': '仅支持 TXT/MD 文本格式'}), 400

#     # 保存到临时文件（二进制模式避免编码问题）
#     with tempfile.NamedTemporaryFile(delete=False, mode='wb') as tmp:
#         f.save(tmp.name)
#         tmp_path = tmp.name

#     # 读取文件内容并自动检测编码
#     try:
#         with open(tmp_path, 'rb') as fr:
#             raw = fr.read()
#             enc = chardet.detect(raw)['encoding'] or 'utf-8'
#             text = raw.decode(enc, errors='ignore')
#             print(f"上传文件内容：{text}")
#     finally:
#         os.unlink(tmp_path)

#     # 生成或获取 user_id
#     user_id = request.cookies.get('user_id') or str(uuid.uuid4())

#     # TODO: 保存文件内容到内存或数据库
#     # memory_manager.save_message(user_id, 'user', "解析以下内容:\n"+text)

#     # 返回响应
#     resp = make_response(jsonify({
#         'message': '上传成功',
#         'text_preview': text[:200],
#         'user_id': user_id
#     }))
#     resp.set_cookie(
#         'user_id',
#         user_id,
#         httponly=True,
#         secure=False,       # 生产环境 HTTPS 推荐改为 True
#         samesite='Lax',     # 跨域上传时可以用 'None'，但需配合 secure=True
#         max_age=30*24*3600
#     )
#     resp.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
#     resp.headers.add('Access-Control-Allow-Credentials', 'true')
#     return resp


@app.route('/api/set_api_key', methods=['POST'])
def set_api_key():
    data = request.json
    api_key = data.get('api_key')
    chatbot.api_key = api_key
    print(f"API Key 设置成功: {api_key}")
    return jsonify({"message": "API Key 设置成功"})

# @app.route('/delete_session', methods=['POST'])
# def delete_session():
#     data = request.json
#     user_id = data.get('user_id')
#     success = memory_manager.delete_session(user_id)
#     print("删除会话成功")
#     return jsonify({"success": success})

# @app.route('/reset', methods=['POST'])
# def reset_history():
#     user_id = request.cookies.get('user_id')
#     if user_id:
#         chatbot.reset_history(user_id)
#         return jsonify({'message': f'History reset for user {user_id}'})
#     else:
#         return jsonify({'error': 'No user ID found'}), 400

# @app.route('/history', methods=['GET'])
# def get_history():
#     user_id = request.cookies.get('user_id')
#     messages = (
#         db.session.execute(db.select(Message)
#             .filter_by(user_id=user_id)
#             .order_by(Message.timestamp))
#         .scalars().all()
#     )
#     return jsonify([{'role': m.role, 'content': m.content} for m in messages])


#兜底路由
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, "index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
