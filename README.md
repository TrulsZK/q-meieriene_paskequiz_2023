# Automating Q-meieriene Påskequiz (Easter Quiz)

Script to automate playing the the Q-meieriene Påskequiz (Easter Quiz) and submitting the correct answer for all of the questions.

The quiz runs in the web browser and gives you 20 questions with 4 alternatives, the questions and answer alternatives are given at random. The objective of the quiz is to answer the questions as fast as possible, and give the correct answer.

The purpose of the scrips is to automate the process of answering the questions correctly and thus obtaining the highest possible score (or a score selected by the user).

The quiz was located at https://quiz.q-meieriene.no/ and was a time-based event for easter 2023, therefore the quiz may not be available today.

This consists of 2 Python scripts and 1 CSV file:

- ```learn_answers.py``` loop through the quiz 1000 times (number can be changed or aborted with ^c) and save question and answer combination to the CSV file
- ```run_quiz.py``` run the quiz and submit the answers found in the CSV file
- ```known_questions.csv``` CSV file to store the question and answer combination for each question

After 20 questions you get the opportunity to submit the score to the High Score (Toppliste) on the website.

When you start the quiz you send a POST request with the turn number to the ```pick-question``` endpoint. This request looks like this:

```JSON
{
  "turn": 1
}
```

You will then receive a response with a question and corresponding answer alternatives. The response looks like this:

```JSON
{
  "question": "Hva er et annet vanlig navn på blodappelsin?",
  "answers": [
    "Grønn appelsin",
    "Gul appelsin",
    "Blå appelsin",
    "Rød appelsin"
  ]
}
```

In the response there are also whitespaces (not shown here) These whitespaces are seemingly at random, and different for each time the same question is displayed. I needed to take this into consideration when making the script

When you answer the question the ```answer``` and ```score``` are sent to the endpoint ```check-answer```. The score (i.e. How fast you answer the question) is calculated using JavaScrip in the browser on your own computer and sendt as a POST request. The POST request looks like this:

```JSON
{
  "answer": "Rød appelsin",
  "score": 99
}
```

When the answer is correct the points are credited to your session. Here is the response for a correct answer:

```JSON
{
  "OK": true
}
```

And here is the response for an incorrect answer:

```JSON
{
  "OK": false,
  "correct": "Rød appelsin"
}
```

These API calls are used as bases for the scrip used to automate this quiz. See the script files for more details.