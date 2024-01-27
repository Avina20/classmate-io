from flask import Flask, request, jsonify
import spacy

spacy

nlp = spacy.load('en_core_web_sm')

import random
from gensim.models import KeyedVectors

model = KeyedVectors.load('incorrect_answer_model.pkl')
model.most_similar(positive=['oxygen'])

app = Flask(__name__)


def ireplace(old, new, text):
    index_l = text.lower().index(old.lower())
    return text[:index_l] + new + text[index_l + len(old):]

def return_question_with_answer(text):
  try:
    text = str(text).replace('\n',' ')
    doc = nlp(text)
    if(len(doc.ents)>0):
      ans = str(random.choice(doc.ents))
      ques = ireplace(ans, '_______',text)
      return ques, ans
    else:
      return -1, -1
  except:
    return -1,-1


def distractor_generator(word):
  word = word.lower()
  if(word in model):
    similar = model.most_similar(positive=[word],topn=3)
    ans = []
    for tup in similar:
      ans.append(tup[0])
    return ans
  else:
    return []

@app.route('/')
def print_questions_with_answers():
 summary = request.args.get('summary')
 if summary:
      summary = summary.split('|')
      ctr = 0
      questions_with_answers = []
      for i in range(len(summary)):
        question, answer = return_question_with_answer(summary[i])
        if(question!=-1):
          choices = distractor_generator(answer)
          if(len(choices)>0):
            print('Q',(ctr+1),': ',question)
            choices.append(answer.lower())
            random.shuffle(choices)
            print("A.", choices[0], "\tB:", choices[1],"\tC:", choices[2], "\tD:", choices[3])
            print('Answer: ', answer)
            question_answer_set = {
                        'question': question,
                        'choices': choices,
                        'correct_answer': answer
                    }
            questions_with_answers.append(question_answer_set)
            ctr = ctr+1
      return questions_with_answers
 else:
    return "Error: 'summary' parameter is missing."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
