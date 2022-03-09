// select all elements
const start = document.getElementById("start");
const quiz = document.getElementById("quiz");
const question = document.getElementById("question");
const qImg = document.getElementById("qImg");
const choiceA = document.getElementById("A");
const choiceB = document.getElementById("B");
const choiceC = document.getElementById("C");
const choiceD = document.getElementById("D");
const counter = document.getElementById("counter");
const container = document.getElementById("container");
const timeGauge = document.getElementById("timeGauge");
const progress = document.getElementById("progress");
const scoreDiv = document.getElementById("scoreContainer");
const scoreImg = document.getElementById("scoreImg");
const scoreText = document.getElementById("scoreText");
const again = document.getElementById("again");


// create our questions
let questions = [
    {
        question : "Кто на картинке?",
        imgSrc : "img/len.jpg",
        choiceA : "Сталин",
        choiceB : "Гитлер",
        choiceC : "Ленин",
        choiceD : "Не знаю",
        correct : "C"
    },{
        question: "Кто на картинке?",
        imgSrc: "img/Elizabeth_of_Russia_by_V.Eriksen.jpg",
        choiceA: "Елизавета Петровна",
        choiceB : "Пушкин",
        choiceC : "Екатерина",
        choiceD : "Женщина",
        correct : "A"
    },{
        question: "Кто на картинке?",

        imgSrc : "img/пет3.jpg",
        choiceA : "Петя 3",
        choiceB : "Величайший",
        choiceC: "Император",
        choiceD : ".",
        correct : "A"
    },{
        question: "Кто на картинке?",

        imgSrc: "img/ель.jpg",
        choiceA : "ded",
        choiceB: "Ельцин",
        choiceC : "ahah",
        choiceD : ")",
        correct : "B"
    }
];

// create some variables

const lastQuestion = questions.length - 1;
let runningQuestion = 0;
let count = 0;
const questionTime = 10; // 10s
const gaugeWidth = 150; // 150px
const gaugeUnit = gaugeWidth / questionTime;
let TIMER;
let score = 0;

// render a question
function renderQuestion(){
    let q = questions[runningQuestion];
    
    question.innerHTML = "<p>"+ q.question +"</p>";
    qImg.innerHTML = "<img src="+ q.imgSrc +">";
    choiceA.innerHTML = q.choiceA;
    choiceB.innerHTML = q.choiceB;
    choiceC.innerHTML = q.choiceC;
    choiceD.innerHTML = q.choiceD;
}

start.addEventListener("click",startQuiz);

// start quiz
function startQuiz(){

    start.style.display = "none";
    renderQuestion();
    quiz.style.display = "block";
    renderProgress();
    renderCounter();
    TIMER = setInterval(renderCounter,1000); // 1000ms = 1s
}

// render progress
function renderProgress(){
    for(let qIndex = 0; qIndex <= lastQuestion; qIndex++){
        progress.innerHTML += "<div class='prog' id="+ qIndex +"></div>";
    }
}

// counter render

function renderCounter(){
    if(count <= questionTime){
        counter.innerHTML = count;
        timeGauge.style.width = count * gaugeUnit + "px";
        count++
    }else{
        count = 0;
        // change progress color to red
        answerIsWrong();
        if(runningQuestion < lastQuestion){
            runningQuestion++;
            renderQuestion();
        }else{
            // end the quiz and show the score
            clearInterval(TIMER);
            scoreRender();
        }
    }
}

// checkAnwer

function checkAnswer(answer){
    if( answer == questions[runningQuestion].correct){
        // answer is correct
        score++;
        // change progress color to green
        answerIsCorrect();
    }else{
        // answer is wrong
        // change progress color to red
        answerIsWrong();
    }
    count = 0;
    if(runningQuestion < lastQuestion){
        runningQuestion++;
        renderQuestion();
    }else{
        // end the quiz and show the score
        clearInterval(TIMER);
        scoreRender();
    }
}

// answer is correct
function answerIsCorrect(){
    document.getElementById(runningQuestion).style.backgroundColor = "#0f0";
}

// answer is Wrong
function answerIsWrong(){
    document.getElementById(runningQuestion).style.backgroundColor = "#f00";
}
function redirect(){
    window.location.href = 'https://itrianone.github.io/ip_proj/';

}

again.addEventListener('click',redirect)
// score render
function scoreRender(){
    quiz.innerHTML = ''

    scoreDiv.style.display = "flex";
    again.style.display = "block";
    
    // calculate the amount of question percent answered by the user
    const scorePerCent = Math.round(100 * score/questions.length);
    
    // choose the image based on the scorePerCent
    let img = (scorePerCent >= 80) ? "img/5.png" :
              (scorePerCent >= 60) ? "img/4.png" :
              (scorePerCent >= 40) ? "img/3.png" :
              (scorePerCent >= 20) ? "img/2.png" :
              "img/1.png";
    let text = (scorePerCent >= 80) ? "Отлично" :
              (scorePerCent >= 60) ? "Норм" :
              (scorePerCent >= 40) ? "Так себе" :
              (scorePerCent >= 20) ? "чел.." : ".";
    
    scoreImg.innerHTML = "<img src="+ img +">";
    scoreImg.innerHTML += "<p>"+ scorePerCent +"%</p>";
    scoreText.innerHTML += "<p>" + text + "</p>";
}





















