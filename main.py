from flask import Flask, request, render_template
import util
import os, uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html', res=[],msg='')

@app.route('/classify_leaf', methods=['POST'])
def classify_leaf():
  if request.method == 'POST':

    file1 = request.files['file1']
    filename1 = secure_filename(file1.filename)
    extension1 = os.path.splitext(filename1)
    file2 = request.files['file2']
    filename2 = secure_filename(file2.filename)
    extension2 = os.path.splitext(filename2)
    file3 = request.files['file3']
    filename3 = secure_filename(file3.filename)
    extension3 = os.path.splitext(filename3)
    file4 = request.files['file4']
    filename4 = secure_filename(file4.filename)
    extension4 = os.path.splitext(filename4)
    file5 = request.files['file5']
    filename5 = secure_filename(file5.filename)
    extension5 = os.path.splitext(filename5)

    allowed_extensions = {'.jpg'}
    if extension1[1] in allowed_extensions and extension2[1] in allowed_extensions and extension3[1] in allowed_extensions and extension4[1] in allowed_extensions and extension5[1] in allowed_extensions:
      f_name1 = str(uuid.uuid4()) + str(extension1[1])
      f_name2 = str(uuid.uuid4()) + str(extension2[1])
      f_name3 = str(uuid.uuid4()) + str(extension3[1])
      f_name4 = str(uuid.uuid4()) + str(extension4[1])
      f_name5 = str(uuid.uuid4()) + str(extension5[1])
      app.config['UPLOAD_FOLDER'] = 'static/Uploads'
      file1.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name1))
      file2.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name2))
      file3.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name3))
      file4.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name4))
      file5.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name5))
      file_list=[]
      file_list.append(f_name1)
      file_list.append(f_name2)
      file_list.append(f_name3)
      file_list.append(f_name4)
      file_list.append(f_name5)
      res = util.get_expense(file_list)

      print(res)
      return render_template('index.html', res=res,msg='')
    else:
      return render_template('index.html', res=[],msg='Upload images of jpg format only!')




  else:
    return render_template('index.html', res=[],msg='')


if __name__ == "__main__":
    util.load_saved_artifacts()
    app.run(debug=True)