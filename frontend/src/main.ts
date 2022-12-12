import { createApp } from 'vue'
import { router } from './router'
import App from './App.vue'
import { Request } from './utils/request';
import VueAxios from 'vue-axios'

import 'element-plus/theme-chalk/el-loading.css';
import 'element-plus/theme-chalk/el-message.css';
import 'element-plus/theme-chalk/el-notification.css';
const app = createApp(App)

app.use(router).use(VueAxios, Request.init())
app.mount('#app')