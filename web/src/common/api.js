import axios from 'axios'
import qs from 'qs'

const fetchData = (url = '', data = {}, method = 'GET') => {
    if (method === 'GET') {
        let param = qs.stringify(data)
        return new Promise(resolve => {
            axios.get(url+'?'+param).then((resp) => {
                resolve(resp.data)
            })
        })

    } else {
        return new Promise(resolve => {
            axios({
                method: method,
                url: url,
                data: data
            }).then((resp) => {
                resolve(resp.data)
            });
        })

    }
}

export const EmailCaptchaAPI = data => fetchData('/api/EmailCaptchaAPI', data, 'GET')
export const LoginAPI = data => fetchData('/api/LoginAPI', data, 'POST')
export const RegistAPI = data => fetchData('/api/RegistAPI', data, 'POST')
export const LogoutAPI = () => fetchData('/api/LogoutAPI', {}, 'POST')
export const AuthInfoAPI = () => fetchData('/api/AuthInfoAPI', {}, 'GET')
export const CheckAuthAPI = () => fetchData('/api/checkauth', {}, 'GET')

export const GetPhotoListAPI = data => fetchData('/api/PhotoListAPI', data, 'GET')
export const GetPhotoAPI = data => fetchData('/api/PhotoAPI', data, 'GET')
export const GetCategoryAPI = () => fetchData('/api/CategoryAPI', {}, 'GET')
export const ThumbPhotoAPI = data => fetchData('/api/ThumbPhotoAPI', data, 'POST')
export const DownloadPhotoAPI = data =>
  axios({
    method: 'POST',
    responseType: 'blob',
    url: '/api/DownloadPhotoAPI',
    data: qs.stringify(data),
  })
    .then(response => response)
    .catch(err => err)