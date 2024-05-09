#!/usr/local/bin/node

const { exit } = require('process');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

times = Math.floor(Math.random() * (56 - 50 + 1)) + 50;

console.log(Array.from({length: 5}, () => Math.random()));

function getUserInput(n, randomNumber) {
  rl.question('Please input a number: ', (answer) => {
    if (n < 55) {
      if(randomNumber === Number(answer)) {
        console.log("Nice guess! continue...");
        getUserInput(n+1, Math.random());
      } else {
        console.log("Wrong!!,Try again... \nBye!!!");
        rl.close();
        exit(0);
      }
    } else {
        console.log("You won!");
        console.log("Spark{PR3D1CT10N_M4ST3R_GG}");
        rl.close();
    }
  }); 
}

getUserInput(1, Math.random());