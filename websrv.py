from flask import Flask, render_template, request, redirect
from markupsafe import escape
import csv

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(f'{page_name}.html')

def write_to_md(data):
    with open('log.md', mode='a') as my_md:
        name, email, message = data['contact_name'], data['contact_email'], data['contact_message']
        my_md.write(f'| `{name}` | `{email}` | `{message}` |\n')

def write_to_csv(data):
    with open('submitted.csv', mode='a') as my_csv:
        name, email, message = data['contact_name'], data['contact_email'], data['contact_message']
        csv_writer = csv.writer(my_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, message])

@app.route("/<page>")
def username(page=None):
    return render_template('pig0.html', name=page)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route("/post")
def post():
    return "This is a post page"

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/p/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /p/
    return f'Your subpath is: {escape(subpath)}'

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            # print(data)
            write_to_md(data)
            write_to_csv(data)
            # return redirect('/thankyou')
            return redirect('/index#popup1')
        except:
            return 'Did not save to database '
    else:
        return 'smth wrng'
