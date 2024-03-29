import { createApp } from 'vue'
import router from './router'
import Antd from 'ant-design-vue'
import App from './App.vue'

createApp(App).use(router).use(Antd).mount('#app');

import "ant-design-vue/dist/antd.css";