function getComputerChoice() {
    choice = Math.random();
    if (choice < 0.3) {
        choice = 'rock';
    }    
    else if (choice > 0.3 && choice < 0.66) {
        choice = 'paper';
    }    
    else {
        choice = 'scissors';
    }
    return choice
}

function getHumanChoice() {
    return prompt('rock, paper, scissor?')
}

let humanScore = 0
let computerScore = 0

function playRound(HumanChoice, ComputerChoice) {
    if (HumanChoice == ComputerChoice) {
        return 'a tie'
    }
    if (humanChoice == 'rock')
}

const humanChoice = getHumanChoice.toLowerCase();
const computerChoice = getComputerChoice.toLowerCase();

playRound(humanChoice, computerChoice)