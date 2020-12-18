
export const formatDate = timestamp => {
    const date = new Date(+timestamp*1000); //这里timestamp是10位可能js解析时间戳为13位
    const y = date.getFullYear()
    const m = date.getMonth() + 1 < 10 ? `0${date.getMonth() + 1}` : date.getMonth() + 1  //月份是从0开始所以加1
    const d = date.getDate() < 10 ? `0${date.getDate()}` : date.getDate()
    return y+"-"+m+"-"+d
}

export const formatTime = timestamp => {
    const date = new Date(+timestamp*1000);
    const y = date.getFullYear()
    const m = date.getMonth() + 1 < 10 ? `0${date.getMonth() + 1}` : date.getMonth() + 1
    const d = date.getDate() < 10 ? `0${date.getDate()}` : date.getDate()

    const ho = date.getHours() < 10 ? `0${date.getHours()}` : date.getHours()
    const mi = date.getMinutes() < 10 ? `0${date.getMinutes()}` : date.getMinutes()
    const se = date.getSeconds() < 10 ? `0${date.getSeconds()}` : date.getSeconds()
    return y+"-"+m+"-"+d+" "+ho+":"+mi+":"+se
}
