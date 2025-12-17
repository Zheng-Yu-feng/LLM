<template>
  <div class="login-background">
    <div class="login-container">
      <div class="title-container">
        <h2 class="title">大语言模型对话系统</h2>
      </div>

      <form @submit.prevent="handleLogin">

        <div class="form-group">
          <label for="username">用户名</label>
          <div class="input-container">
            <i class="icon fa fa-user"></i>
            <input
              type="text"
              id="username"
              v-model="username"
              placeholder="请输入用户名"
              required
            />
          </div>
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <div class="input-container">
            <i class="icon fa fa-lock"></i>
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="请输入密码"
              required
            />
          </div>
        </div>
        <button type="submit">登录</button>
      </form>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'login',
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '', // 用于显示错误信息
    };
  },
  methods: {
    handleLogin() {
      // 模拟登录逻辑，假设用户名是 'admin' 密码是 'password'
      if (this.username === 'admin' && this.password === '123') {
        // 登录成功，将登录状态存储到 localStorage 中
        localStorage.setItem('isAuthenticated', 'true');
        this.$router.push('/conversation');  // 登录成功后跳转到首页
      } else {
        this.errorMessage = '用户名或密码错误';
      }
    },
  },
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
.extra-links {
  margin-top: 20px;
  
}

.login-background {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #bec0c4, #3678f1);
}

.title-container {

    margin-bottom: 55px;
    .title {
      font-size: 36px;
      color: rgb(102, 104, 109);
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
}
.login-container {
  width: 560px;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0px 4px 16px rgba(0, 0, 0, 0.2);
  text-align: center;
}

h2 {
  color: #333;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
}

.input-container {
  position: relative;
}

.icon {
  position: absolute;
  top: 50%;
  left: 8px;
  transform: translateY(-50%);
  color: #888;
}

input {
  width: 90%;
  padding: 0.5rem 0.5rem 0.5rem 2.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s, box-shadow 0.3s;
}


button:hover {
  background-color: #357abd;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.15);
}

.error-message {
  color: red;
  margin-top: 1rem;
  font-size: 0.9rem;
}
</style>
