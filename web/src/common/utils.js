import M from "materialize-css"

export function serverError() {
    let toastHTML = '<span>系统状态异常!</span>';
    M.toast({html: toastHTML});
}

export function download(data, fileName) {
    if (!data) {
      return
    }
    let url = window.URL.createObjectURL(new Blob([data]))
    let link = document.createElement('a')
    link.style.display = 'none'
    link.href = url
    link.setAttribute('download', fileName)
    link.click()
    window.URL.revokeObjectURL(url)
}