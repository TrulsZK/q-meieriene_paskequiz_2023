import requests
import csv

# Settings
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
csvfilepath = "known_questions.csv"
questionscores = [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99]
nametosubmit = "Truls Zhong Konstali" # Replace with your own name to submit score
numbertosubmit = "XXXXXXXX" # Replace with your own mobile number (Norwegian number without +47) to submit score

# Remove Extra Spaces
def removeextraspaces(string):
    string = ' '.join(string.split())
    string = string.strip()

    return string

# Get Defined Score To Submit
def scoretosubmit(questioncount):
    return questionscores[questioncount - 1]

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
    
    # Prosess Question and Answers
    question = pickquestion_response.json()["question"]
    questionclean = removeextraspaces(question)
    
    answer0 = pickquestion_response.json()["answers"][0]
    answer1 = pickquestion_response.json()["answers"][1]
    answer2 = pickquestion_response.json()["answers"][2]
    answer3 = pickquestion_response.json()["answers"][3]
    answer0clean = removeextraspaces(answer0)
    answer1clean = removeextraspaces(answer1)
    answer2clean = removeextraspaces(answer2)
    answer3clean = removeextraspaces(answer3)

    print(pickquestion_response.json())
    print(questionclean)
    print(answer0clean)
    print(answer1clean)
    print(answer2clean)
    print(answer3clean)

    correctanswer = "placeholder"
    correctanswerindex = 0
    correctanswertosubmit = "placeholder"

    # Find Question in CSV File
    with open(csvfilepath, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        answer_index = header.index('answer')
        for row in csvreader:
            if row[0] == questionclean:
                correctanswer = row[answer_index]
    
    correctanswerclean = removeextraspaces(correctanswer)
    print("Correct is")
    print(correctanswerclean)

    if correctanswerclean == answer0clean:
        correctanswerindex = 0
        correctanswertosubmit = answer0
    
    if correctanswerclean == answer1clean:
        correctanswerindex = 1
        correctanswertosubmit = answer1

    if correctanswerclean == answer2clean:
        correctanswerindex = 2
        correctanswertosubmit = answer2

    if correctanswerclean == answer3clean:
        correctanswerindex = 3
        correctanswertosubmit = answer3

    print("Index")
    print(correctanswerindex)

    # Submit Answer
    checkanswer_url = "https://quiz.q-meieriene.no/api/app/quiz/check-answer"
    checkanswer_payload = {'answer': correctanswertosubmit,'score': scoretosubmit(questioncount)}
    checkanswer_response = session.post(checkanswer_url, json=checkanswer_payload, headers=headers)

    print(checkanswer_response.json())

    questioncount = questioncount + 1

# Get Score
getscore_url = "https://quiz.q-meieriene.no/api/app/results/rating"
getscore_payload = {}
getscore_response = session.post(getscore_url, json=getscore_payload, headers=headers)

myposition = getscore_response.json()["position"]
myscore = getscore_response.json()["score"]

print(getscore_response.json())
print("Position")
print(myposition)
print("Score")
print(myscore)

# Do you want to submit
submitscore = 0
submitresponse = input("Submit Score? (y/n) ")
if submitresponse.lower() == "y":
    submitscore = 1
elif submitresponse.lower() == "n":
    submitscore = 0
else:
    print("Invalid Input")

if submitscore == 0:
    exit()

# Submit Score
submitscore_url = "https://quiz.q-meieriene.no/api/app/registration/apply"
submitscore_payload = {"name": nametosubmit,"phone": numbertosubmit}
submitscore_response = session.post(submitscore_url, json=submitscore_payload, headers=headers)

print(submitscore_response.json())

# Get SMS Code
submitresponse = input("Enter Code From SMS: ")

# Submit SMS Code
submitsms_url = "https://quiz.q-meieriene.no/api/app/registration/confirm"
submitsms_payload = {"code": submitresponse}
submitsms_response = session.post(submitsms_url, json=submitsms_payload, headers=headers)

print(submitscore_response.json())
