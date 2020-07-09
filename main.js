import Vue from 'vue'
import App from './App'
// main.js

import Axios from 'axios'
import VueAxios from 'vue-axios'

const MyAxios = Axios.create({
  transformRequest: [function (data) {
    // 将数据转换为表单数据
    let ret = ''
    for (let it in data) {
      ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
    }
    return ret
  }],
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
})

Vue.use(VueAxios, MyAxios)
