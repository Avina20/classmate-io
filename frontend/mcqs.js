let questions
let user
let accessToken
let round = 1
let notes
const questionEL = document.getElementById("question");
const answerButtonsEL = document.getElementById("answer-buttons");
const nextBtnEL = document.getElementById("next-btn");

let currentQuestionIndex = 0;
let score = 0;

const apiEndpoint =
  "https://qfhdl3ixb1.execute-api.us-east-1.amazonaws.com/test";


window.onload = async()=>{
    user = 'test';
    if(sessionStorage.getItem('user')){
        user = sessionStorage.getItem('user')
        accessToken = sessionStorage.getItem('access_token')
    }
    document.getElementById('userName').innerText = user

    response = await fetch(apiEndpoint + "/viewAll",{
        headers:{
            "Authorization": accessToken
        }
    })
    notesJSON = await response.json()
    notes = notesJSON
    notesJSON.forEach(option => {
        const optionElement = document.createElement("option");
        optionElement.value = option.NoteId;
        optionElement.textContent = option.NoteId;
        dropdown.appendChild(optionElement);
    });
};

function showQuestion() {
    resetState();
    const currentQuestion = questions[currentQuestionIndex];
    const questionNo = currentQuestionIndex + 1;
    questionEL.innerHTML = `${questionNo}. ${currentQuestion.question}`;

    currentQuestion.choices.forEach(option => {
        const button = createAnswerButton(option, currentQuestion.correct_answer == option);
        answerButtonsEL.appendChild(button);
    });
}

function createAnswerButton(text, isCorrect) {
    const button = document.createElement("button");
    button.innerHTML = text;
    button.classList.add("btn");
    if (isCorrect) {
        button.dataset.correct = "true";
    }
    button.addEventListener("click", selectAnswer);
    return button;
}

function resetState() {
    nextBtnEL.style.visibility = "hidden";
    while (answerButtonsEL.firstChild) {
        answerButtonsEL.removeChild(answerButtonsEL.firstChild);
    }
}

function selectAnswer(e) {
    const selectedBtn = e.target;
    const isCorrect = selectedBtn.dataset.correct === "true";
    if (isCorrect) {
        selectedBtn.classList.add("correct");
        score++;
    } else {
        selectedBtn.classList.add("incorrect");
    }
    Array.from(answerButtonsEL.children).forEach(button => {
        if (button.dataset.correct === "true") {
            button.classList.add("correct");
        }
        button.disabled = true;
    });
    nextBtnEL.style.visibility = "visible";
}

function showScore() {
    resetState();
    questionEL.innerHTML = `You scored ${score} out of ${questions.length}!`;
    nextBtnEL.innerHTML = "Play Again";
    nextBtnEL.style.visibility = "visible";
    round = 2
}

function handleNextButton() {
    currentQuestionIndex++;
    if (currentQuestionIndex < questions.length) {
        showQuestion();
    } else {
        showScore();
    }
}

nextBtnEL.addEventListener("click", () => {
    if (currentQuestionIndex < questions.length) {
        handleNextButton();
    } else {
        startQuiz();
    }
});

 async function getMCQ(){
    document.getElementById('quizC').style.display = 'block'
    let noteId = document.getElementById('dropdown').value
    let noteContent;

    notes.forEach(note=>{
        if (note.NoteId === noteId){
            noteContent = note.Content
        }
    })

    payload = {
        "content": noteContent
    }

    try{
        response = await fetch("https://6va32u1p1g.execute-api.us-east-1.amazonaws.com/Mcq_stage1/mcq",{
            method: "POST",
            body: JSON.stringify(payload)
        })
        questions = await response.json()
    } catch (e){
        console.log('Error Fetching MCQ')
    } 
    startQuiz();
}

function startQuiz() {
    currentQuestionIndex = 0;
    score = 0;
    nextBtnEL.innerHTML = "Next";
    showQuestion();
}
