updateQuestions();
dothething();
function mirror(number){   
    selected = document.getElementById('correct-answer-'+number)
    incorrect =  document.getElementById('incorrect-answer-'+number)
    for(let j=0; j<4;j++){
        incorrect.children[j].selected = !selected.children[j].selected
    }
}
function validateSubmission(e) {
    e.preventDefault()
    dothething()
    e.submit()
}
