answerbButtons = [...document.getElementsByClassName("answer")]
answerbButtons.forEach(button => {
    button.addEventListener("click",(event)=>{
        window.location.href= `/answer?value=${event.target.value}`
    })
    
});
backButton = document.getElementsByClassName("back")
if (backButton.length) {
    backButton[0].addEventListener("click",()=>{
        window.location.href = "/back"
    })
}