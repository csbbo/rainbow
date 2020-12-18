import axios from 'axios'
axios.defaults.timeout = 330000
// 添加请求头
axios.get('/api/csrftoken').then(resp => {
    axios.defaults.headers['X-CSRF-TOKEN'] = resp.data.data['X-CSRF-TOKEN']
})
