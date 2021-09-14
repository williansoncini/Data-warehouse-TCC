function request(url, method, csrf_token,data){
    // alert('Função!')
    axios({
        url: url,
        method: method,
        headers:{"X-CSRFToken": csrf_token},
        data: data});
}
