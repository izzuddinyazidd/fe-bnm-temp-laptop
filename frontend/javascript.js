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

function playRound(humanChoice, computerChoice) {
    if (HumanChoice == ComputerChoice) {
        return 'a tie'
    }
    if (humanChoice == 'rock') {
        if (computerChoice == 'scissors') {
            return 'you win'
        }
        else {
            return 'you lose'
        }
    }
    if (humanChoice == 'scissors') {
        if (computerChoice == 'paper') {
            return 'you win'
        }
        else {
            return 'you lose'
        }
    }
    if (humanChoice == 'paper') {
        if (computerChoice == 'rock') {
            return 'you win'
        }
        else {
            return 'you lose'
        }
    }
}

const humanChoice = getHumanChoice.toLowerCase();
const computerChoice = getComputerChoice.toLowerCase();

playRound(humanChoice, computerChoice)