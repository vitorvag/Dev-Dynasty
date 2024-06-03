function vai(x){
    if(x.id == 'sim'){
     
      document.querySelector('input[id="nao"]').checked = false
    } else {
      document.querySelector('input[id="sim"]').checked = false
    }
  }

  window.onload = () => {
    let men = document.querySelector('li[class="menssagens"]');
    let div = document.getElementById('messages')
    if(men.innerHTML != ''){
      men.classList.add('men')
      setTimeout(()=>{
        men.classList.remove('men')
        men.style.display = 'none'
        div.style.display = 'none'
      },5000)
    }
  }

  function go(x){
    if(x.checked == true){
        document.querySelector("input[name='file']").value = ''
    }
   
}
setInterval(()=>{
    let d = document.querySelector("input[name='file']")
    let i = document.querySelector("input[name='img']")
    if(i.checked == false && d.value == ''){
        i.checked = true
    } else if(i.checked == true && d.value != '') {
        i.checked = false
    }
},500)