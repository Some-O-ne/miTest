buttons = [...document.getElementsByClassName("answer")]
buttons.forEach(button => {
    button.addEventListener("click",(event)=>{
        window.location.href= `/answer?value=${event.target.value}`
    })
    
});