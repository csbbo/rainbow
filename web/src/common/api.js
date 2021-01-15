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

// export const SendCodeAPI = data => fetchData('/api/code', data, 'POST')
export const LoginAPI = data => fetchData('/api/LoginAPI', data, 'POST')
export const RegistAPI = data => fetchData('/api/RegistAPI', data, 'POST')
// export const LogoutAPI = () => fetchData('/api/logout', {}, 'POST')
// // export const GetUserAPI = () => fetchData('/api/user', {}, 'GET')
export const CheckAuthAPI = () => fetchData('/api/checkauth', {}, 'GET')
// export const ArticleCreateAPI = data => fetchData('/api/article', data, 'POST')
// export const ShowArticlesAPI = () => fetchData('/api/showarticles', {}, 'GET')
// export const GetArticleListAPI = () => fetchData('/api/articlelist', {}, 'GET')

export const GetPhotoListAPI = data => fetchData('/api/PhotoListAPI', data, 'GET')
export const GetPhotoAPI = data => fetchData('/api/PhotoAPI', data, 'GET')
export const GetCategoryAPI = () => fetchData('/api/CategoryAPI', {}, 'GET')
// export const DownloadPhotoAPI = data => fetchData('/api/DownloadPhotoAPI', data, 'POST')
export const ThumbPhotoAPI = data => fetchData('/api/ThumbPhotoAPI', data, 'POST')

export const DownloadPhotoAPI = data =>
  axios({
    method: 'POST',
    responseType: 'blob',
    url: '/api/DownloadPhotoAPI',
    data: qs.stringify(data),
  }).then(response => response).catch(err => err)