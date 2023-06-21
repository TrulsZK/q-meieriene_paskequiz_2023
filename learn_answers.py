import requests
import csv

# Settings
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
numberofrounds = 1000
csvfilepath = "known_questions.csv"

# Remove Extra Spaces
def removeextraspaces(string):
    string = ' '.join(string.split())
    string = string.strip()

    return string

quizcount = 0

while quizcount < numberofrounds:

    # Start Session
    session = requests.Session()

    # Start Quiz
    start_url = "https://quiz.q-meieriene.no/"
    start_payload = {}

    start_response = session.post(start_url, json=start_payload, headers=headers)

    #print(start_response.json())

    # Check / Enter code
    checkcode_url = "https://quiz.q-meieriene.no/api/app/access_code/check"
    checkcode_payload = {"code": "quiz"}

    checkcode_response = session.post(checkcode_url, json=checkcode_payload, headers=headers)

    print(checkcode_response.json())

    # Run 20 questions
    questioncount = 1

    while questioncount <= 20:

        # Question 
        pickquestion_url = "https://quiz.q-meieriene.no/api/app/quiz/pick-question"
        pickquestion_payload = {"turn": questioncount}

        pickquestion_response = session.post(pickquestion_url, json=pickquestion_payload, headers=headers)
        question = pickquestion_response.json()["question"]
        questionclean = removeextraspaces(question)

        print(pickquestion_response.json())
        print(questionclean)

        # Submit / Check Answer 
        checkanswer_url = "https://quiz.q-meieriene.no/api/app/quiz/check-answer"
        #checkanswer_payload = {'answer': 'placeholder','score': 99}
        checkanswer_payload = {}
        checkanswer_response = session.post(checkanswer_url, json=checkanswer_payload, headers=headers)
        answer = checkanswer_response.json()["correct"]
        answerclean = removeextraspaces(answer)

        print(checkanswer_response.json())
        print(answerclean)

        questionincsv = 0

        # CSV File
        # Check if question exista
        with open(csvfilepath, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if row[0] == questionclean:
                    questionincsv = 1
                    print("Question Found in CSV")

        # Write to CSV
        if questionincsv == 0:
            with open(csvfilepath, "a") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([questionclean, answerclean])
                print("Question Written to CSV")

        questioncount = questioncount + 1

    quizcount = quizcount + 1
