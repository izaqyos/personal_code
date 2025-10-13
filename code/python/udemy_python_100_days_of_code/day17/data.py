from opentdb import OpenTDB
# animal qs: https://opentdb.com/api.php?amount=10&category=27&difficulty=easy&type=boolean
#openTDB_obj = OpenTDB('https://opentdb.com/api.php?amount=30&category=27&difficulty=easy&type=boolean')

#openTDB_obj = OpenTDB('https://opentdb.com/api.php?amount=15&category=25&difficulty=easy&type=boolean')
openTDB_obj = OpenTDB('https://opentdb.com/api.php?amount=30&category=26')


question_data_opentdb = openTDB_obj.get_questions()
#question_data_opentdb = {
#    "response_code": 0,
#    "results": [
#        {
#            "category": "Animals",
#            "type": "boolean",
#            "difficulty": "easy",
#            "question": "The Axolotl is an amphibian that can spend its whole life in a larval state.",
#            "correct_answer": "True",
#            "incorrect_answers": [
#                "False"
#            ]
#        },
#        {
#            "category": "Animals",
#            "type": "boolean",
#            "difficulty": "easy",
#            "question": "Kangaroos keep food in their pouches next to their children.",
#            "correct_answer": "False",
#            "incorrect_answers": [
#                "True"
#            ]
#        },
#        {
#            "category": "Animals",
#            "type": "boolean",
#            "difficulty": "easy",
#            "question": "A bear does NOT defecate during hibernation. ",
#            "correct_answer": "True",
#            "incorrect_answers": [
#                "False"
#            ]
#        },
#        {
#            "category": "Animals",
#            "type": "boolean",
#            "difficulty": "easy",
#            "question": "In 2016, the IUCN reclassified the status of Giant Pandas from endangered to vulnerable.",
#            "correct_answer": "True",
#            "incorrect_answers": [
#                "False"
#            ]
#        },
#        {
#            "category": "Animals",
#            "type": "boolean",
#            "difficulty": "easy",
#            "question": "Rabbits are rodents.",
#            "correct_answer": "False",
#            "incorrect_answers": [
#                "True"
#            ]
#        },
#        {
#            "category": "Animals",
#            "type": "boolean",
#            "difficulty": "easy",
#            "question": "Cats have whiskers under their legs.",
#            "correct_answer": "True",
#            "incorrect_answers": [
#                "False"
#            ]
#        },
#        {
#            "category": "Animals",
#            "type": "boolean",
#            "difficulty": "easy",
#            "question": "The Killer Whale is considered a type of dolphin.",
#            "correct_answer": "True",
#            "incorrect_answers": [
#                "False"
#            ]
#        },
#        {
#            "category": "Animals",
#            "type": "boolean",
#            "difficulty": "easy",
#            "question": "Rabbits can see what&#039;s behind themselves without turning their heads.",
#            "correct_answer": "True",
#            "incorrect_answers": [
#                "False"
#            ]
#        },
#        {
#            "category": "Animals",
#            "type": "boolean",
#            "difficulty": "easy",
#            "question": "Rabbits are carnivores.",
#            "correct_answer": "False",
#            "incorrect_answers": [
#                "True"
#            ]
#        },
#        {
#            "category": "Animals",
#            "type": "boolean",
#            "difficulty": "easy",
#            "question": "The internet browser Firefox is named after the Red Panda.",
#            "correct_answer": "True",
#            "incorrect_answers": [
#                "False"
#            ]
#        }
#    ]
#}
#
def normalize_tdb_questions(tdb_questions):
    #print(f"normalize_tdb_questions. normalizing {tdb_questions}")
    question_data = []
    for q in tdb_questions["results"]:
        #print(f"normalize_tdb_questions. add {q}")
        if q["type"] == "boolean":
            question_data.append({"text": q["question"], "answer": q["correct_answer"]  })
    return question_data

question_data = [
    {"text": "A slug's blood is green.", "answer": "True"},
    {"text": "The loudest animal is the African Elephant.", "answer": "False"},
    {"text": "Approximately one quarter of human bones are in the feet.", "answer": "True"},
    {"text": "The total surface area of a human lungs is the size of a football pitch.", "answer": "True"},
    {"text": "In West Virginia, USA, if you accidentally hit an animal with your car, you are free to take it home to eat.", "answer": "True"},
    {"text": "In London, UK, if you happen to die in the House of Parliament, you are entitled to a state funeral.", "answer": "False"},
    {"text": "It is illegal to pee in the Ocean in Portugal.", "answer": "True"},
    {"text": "You can lead a cow down stairs but not up stairs.", "answer": "False"},
    {"text": "Google was originally called 'Backrub'.", "answer": "True"},
    {"text": "Buzz Aldrin's mother's maiden name was 'Moon'.", "answer": "True"},
    {"text": "No piece of square dry paper can be folded in half more than 7 times.",
        "answer": "False"},
    {"text": "A few ounces of chocolate can to kill a small dog.", "answer": "True"}
]

# ofc can use opentdb api (see: https://opentdb.com/api_config.php)
# e.g. https://opentdb.com/api.php?amount=10&category=20&difficulty=easy&type=boolean - 10 easy true/false mythology questions
