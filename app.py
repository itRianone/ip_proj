from config import app, db, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, cache
from data import quizes,victs
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from models import User
from sqlalchemy.exc import IntegrityError as sql_error
import os

# tell Flask to use the above defined config

# @cache.cached(timeout=500)
@app.route('/')
def main():
  # username = request.cookies.get('username')
  try:
    user_name = session['username']
    username = User.query.filter_by(username=str(session['username'])).one()
    session['prof_pic'] = username.profile_picture
    pic = username.profile_picture
    return render_template('home.html', pic=pic)
  except:
    username = None
    return render_template('home.html')

  #print(username)

@app.route('/<quiz_type>/<quizname>')
def quiz_page(quiz_type, quizname):
  print(quiz_type, quizname)
  try:
    description = description[quizname]
  except:
    description=''
  return render_template('quiz_page.html', quiz_type=quiz_type, description=description, quizname=quizname)


# @app.errorhandler(Exception)
# def err(e):
#   return render_template('err.html', error=e)

def nearest(lst, target):
  return min(lst, key=lambda x: abs(x-target))

# @cache.cached(timeout=500)
@app.route('/test/<quizname>/<question_num>', methods=["GET", "POST"])
def quiz(quizname, question_num):
  if request.method == "POST":
    #print(quiz_type)
    try:
      req = request.form

      #cache.set(f'{question_num}', f'{req["option"]}')
      session[f'{question_num}'] = f'{req["option"]}'
      print(req['option'], list(quizes[quizname]['questions'].values())[int(question_num)-1])
    except:
      error = 'Выбери что нибудь'
      return render_template('question.html', quest=list(quizes[quizname]['questions'].keys())[int(question_num)-1],
                                          opts=quizes[quizname]['options'][int(question_num)-1],
                                          quizname=quizname,
                                          error=error,
                                          question_num=question_num)

    return redirect(url_for('quiz', quizname=quizname, question_num=int(question_num)+1))



  try:
    #print(list(quizes[quizname]['questions'].keys())[int(question_num)],quizes[quizname]['options'][int(question_num)-1])
    return render_template('question.html', quest=list(quizes[quizname]['questions'].keys())[int(question_num)-1],
                                        opts=quizes[quizname]['options'][int(question_num)-1],
                                        quizname=quizname,
                                        question_num=question_num)
  except IndexError:
    correct_answers_count = 0
    answers = []
    correct_answers = []
    for i in range(1, int(question_num)):

      # q = cache.get(str(i))
      try:
        answer = session[f'{i}']
        if answer is None:
          continue
        
        print(answer,list(quizes[quizname]['questions'].values())[int(i)-1])
        if str(answer) == list(quizes[quizname]['questions'].values())[int(i)-1]:
          answers.append({'answer': answer, 'is_correct': True})

          print(correct_answers_count)
          correct_answers_count += 1
          correct_answers.append(answer)
        else:
          answers.append({'answer': answer, 'is_correct': False})

        print(answers, correct_answers)

      except KeyError:
        pass
    return render_template('end.html', correct_answers_count=correct_answers_count,
                                       answers=answers,
                                       correct_answers=correct_answers,
                                       quest_amount=int(question_num)-1)
  
  except KeyError:
    return "<body style='background-color:black;color:white;'>no such quiz</body>"

# @cache.cached(timeout=500)
@app.route('/victorin/<quizname>/<question_num>', methods=["GET", "POST"])
def victorin(quizname, question_num):
  if request.method == "POST":
    #print(quiz_type)
    try:
      req = request.form

      #balls = []
      right = list(victs[quizname]['questions'].values())[int(question_num)-1]
      opt = victs[quizname]['options'][int(question_num)-1]
      balls=zip(right.split(),opt)
      # print(right, [i for i in balls])
      #cache.set(f'{question_num}', f'{req["option"]}')
      for i in balls:
        #print(1, req["option"], i[1])
        if req["option"] == i[1]:
          session[f'{question_num}'] = i[0]
          print(i[0], i[1], req["option"])


      #print(req['option'], list(victs[quizname]['questions'].values())[int(question_num)-1])
    except:
      error = 'Выбери что нибудь'
      return render_template('question.html', quest=list(victs[quizname]['questions'].keys())[int(question_num)-1],
                                          opts=victs[quizname]['options'][int(question_num)-1],
                                          quizname=quizname,
                                          error=error,
                                          question_num=question_num)

    return redirect(url_for('victorin', quizname=quizname, question_num=int(question_num)+1))


  try:
    #print(list(quizes[quizname]['questions'].keys())[int(question_num)],quizes[quizname]['options'][int(question_num)-1])
    return render_template('question.html', quest=list(victs[quizname]['questions'].keys())[int(question_num)-1],
                                        opts=victs[quizname]['options'][int(question_num)-1],
                                        quizname=quizname,
                                        question_num=question_num)
  except IndexError:
    balls_count = 0
    for i in range(1, int(question_num)):

      # q = cache.get(str(i))
      try:
        answer = session[f'{i}']
        if answer is None:
          continue
        
        #print(answer,list(victs[quizname]['questions'].values())[int(i)-1])
        #if str(answer) == list(victs[quizname]['questions'].values())[int(i)-1]:
        balls_count += int(answer)
        end_variants_values = list(victs[quizname]['variants'].values())
        #end_variants_values = [int(x) for x in end_variants_values]
        near = nearest(end_variants_values, balls_count)
        #list(victs[quizname]['variants'].keys())
        res_of_victorin = list(victs[quizname]['variants'].keys())[list(victs[quizname]['variants'].values()).index(near)]

      except KeyError:
        pass
    return render_template('end_vict.html', quest_amount=int(question_num)-1, res_of_victorin=res_of_victorin)
  
  # except KeyError:
  #   return "<body style='background-color:black;color:white;'>no such quiz</body>"


@app.route('/logout', methods=['POST', 'GET']) 
def logout():
    
  if session['username']:
    session['username'] = None 
  else: 
    pass

  return redirect(url_for('main'))

# @app.errorhandler(500)
@app.route('/login', methods=['POST', 'GET']) 
def login():
  if not session['username']:
    if request.method == 'POST':
      data = request.form
      username = data['login_name']
      password = data['login_passw']
      
      user = User.query.filter_by(username=username).first()
      print(user)
        
      if user and password == user.password:
        session['username'] = username
        return redirect(url_for('main'))

      else:
        error = 'нет такого либо неверный пароль' 
        return render_template('login.html', error=error) 
      # resp = make_response()
      # resp.set_cookie('username', username)


    return render_template('login.html')      
  return redirect(url_for('main'))
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/lk', methods=['GET', 'POST'])
def profile():
  user = session['username']
  if user:
    username = User.query.filter_by(username=str(session['username'])).one()
    if request.method == 'POST':
      print('ea')
      file = request.files['pic']
      print('ok')
      if file and allowed_file(file.filename):

        #image_name = secure_filename(file.filename) ????
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        username.profile_picture = file.filename
        session['prof_pic']=username.profile_picture
        db.session.commit()
        return render_template('lk.html', pic=username.profile_picture)#
    return render_template('lk.html', pic=username.profile_picture)
  return redirect(url_for('registration'))

# @app.errorhandler(500)
@app.route('/registration', methods=['POST', 'GET']) 
def registration():
  if not session['username']:
    if request.method == 'POST':
      data = request.form
      username = data['reg_name']
      password = data['reg_passw']
      if len(username) >= 5 and len(password) >= 5:
        print('ok go')
      else:
          
        error ='Имя и пароль минимум по 5 символов'
        return render_template('registration.html', error=error)

      try:
        user = User(username=username, password=password,profile_picture=None)
        db.session.add(user)
        db.session.commit()

        session['username'] = username
        # resp = make_response()
        # resp.set_cookie('username', username)

        return redirect(url_for('main'))
      except sql_error as e:
        print(e)
        error = 'Уже есть в бд такой юзер'
        return render_template('registration.html', error=error)
    return render_template('registration.html') 
  return redirect(url_for('main'))

if __name__=="__main__":
  app.run()