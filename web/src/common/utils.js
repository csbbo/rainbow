import M from "materialize-css"

export function serverError() {
    let toastHTML = '<span>系统状态异常!</span>';
    M.toast({html: toastHTML});
}