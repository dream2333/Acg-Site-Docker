<script setup lang="ts">
import "element-plus/es/components/dialog/style/css";
import "element-plus/theme-chalk/display.css";
import {
  ElementPlus,
  Eleme,
  Message,
  Iphone,
  User,
  Key,
} from "@element-plus/icons-vue";
import { FormInstance, ElDialog, ElMessage } from "element-plus/es";
import { login, register } from "../../api";

const form1 = reactive({ username: "", password: "" });
const form2 = reactive({ phonenumber: "", vcode: "" });
const rules = reactive({
  username: [
    { required: true, message: "请输入用户名", trigger: "blur" },
    {
      min: 5,
      max: 12,
      message: "长度在 5 到 12 个字符",
      trigger: "blur",
    },
  ],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    {
      min: 5,
      max: 12,
      message: "长度在 5 到 12 个字符",
      trigger: "blur",
    },
  ],
});
const emit = defineEmits(["logged"]);
const loading = ref(false);
const show = ref(false);
const ruleFormRef = ref<FormInstance>();

const handleSubmit = (e: Event) => {
  ruleFormRef.value!.validate((valid, fields) => {
    if (valid) {
      const param = {
        username: form1.username,
        password: form1.password,
      };
      loading.value = true;
      login(param)
        .then((response) => {
          loading.value = false;
          if (response.data["status"] == 1) {
            localStorage.setItem("ACCESS_TOKEN", response.data["token"]);
            emit("logged", response.data["msg"]);
            window.location.reload()
            ElMessage({
              message: "登陆成功，现在您可以尽情游览了",
              type: "success",
              offset: 40,
            });
          } else {
            ElMessage({
              message: "用户名或密码不正确",
              type: "error",
              offset: 40,
            });
          }
        })
        .catch((e) => {
          loading.value = false;
        });
    } else {
      ElMessage({
        message: "账号密码格式不正确",
        type: "error",
        offset: 40,
      });
    }
  });
};

const handleRegisiter = (e: Event) => {
  ruleFormRef.value!.validate((valid, fields) => {
    if (valid) {
      const param = {
        username: form1.username,
        password: form1.password,
      };
      loading.value = true;
      register(param)
        .then((response) => {
          loading.value = false;
          if (response.data["status"] == 1) {
            ElMessage({
              message: "注册成功，现在可以登录您的账号了",
              type: "success",
              offset: 40,
            });
          } else {
            ElMessage({
              message: "注册失败，请重试",
              type: "error",
              offset: 40,
            });
          }
        })
        .catch((e) => {
          loading.value = false;
        });
    } else {
      ElMessage({
        message: "账号密码格式不正确",
        type: "error",
        offset: 40,
      });
    }
  });
};
</script>
<template>
  <el-dialog v-model="show" width="600px" append-to-body>
    <div v-loading="loading">
      <el-row align="middle" style="margin-bottom: 20px; padding-left: 20px; padding-right: 20px">
        <el-col :lg="8" class="hidden-md-and-down">
          <el-space direction="vertical">
            <span>扫一扫查看项目说明</span>
            <img style="width: 100%; height: 100%" src="../../assets/qrcode.png" />
            <span class="text">
              请使用微信客户端
              <br />扫码登录或查看项目说明
            </span>
          </el-space>
        </el-col>
        <el-col :lg="2" class="hidden-md-and-down">
          <el-divider direction="vertical" style="height: 270px" />
        </el-col>
        <el-col :lg="14">
          <el-tabs model-value="first">
            <el-tab-pane label="账号密码登录" name="first">
              <el-form :model="form1" :rules="rules" ref="ruleFormRef">
                <el-form-item prop="username">
                  <el-input v-model="form1.username" placeholder="账号" :prefix-icon="User" size="large" />
                </el-form-item>
                <el-form-item prop="password">
                  <el-input v-model="form1.password" placeholder="密码" :prefix-icon="Key" size="large" type="password"
                    show-password />
                </el-form-item>
              </el-form>

              <el-row justify="space-between">
                <el-button style="width: 47%" size="large" @click="handleRegisiter">注册</el-button>
                <el-button type="primary" style="width: 47%" size="large" @click="handleSubmit">登录</el-button>
              </el-row>
            </el-tab-pane>
            <el-tab-pane label="手机号登录" name="second">
              <el-form :model="form1">
                <el-form-item>
                  <el-input v-model="form2.phonenumber" placeholder="手机号" :prefix-icon="Iphone" size="large" />
                </el-form-item>
                <el-row :gutter="16">
                  <el-col :lg="14">
                    <el-form-item>
                      <el-input v-model="form2.vcode" placeholder="验证码" :prefix-icon="Message" size="large"
                        style="width: 100%" />
                    </el-form-item>
                  </el-col>
                  <el-col :lg="10">
                    <el-button style="width: 100%" size="large">验证码</el-button>
                  </el-col>
                </el-row>
              </el-form>
              <el-row>
                <el-button type="primary" style="width: 100%" size="large">登录</el-button>
              </el-row>
            </el-tab-pane>
          </el-tabs>
          <el-row class="text" justify="center" style="margin-top: 20px; margin-bottom: 20px">其他登陆方式</el-row>
          <el-row justify="center">
            <el-button type="primary" :icon="ElementPlus" circle />
            <el-button type="success" :icon="Eleme" circle />
            <el-button type="info" :icon="Message" circle />
          </el-row>
        </el-col>
      </el-row>
      <el-row justify="center">
        <span class="text233">
          未注册过本网站的账号请先进行注册
          <br />登录或完成注册即代表你同意《用户协议》和《隐私政策》
        </span>
      </el-row>
    </div>
  </el-dialog>
</template>

<style>
.el-dialog {
  border-radius: 20px;
  box-shadow: 0 0 20px rgba(49, 49, 49, 0.301);
}

.text233 {
  font-size: 10px;
  text-align: center;
  color: rgba(85, 85, 85, 0.5);
}
</style>
