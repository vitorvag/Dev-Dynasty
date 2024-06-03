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