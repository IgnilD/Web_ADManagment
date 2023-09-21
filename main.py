import json
import os
from subprocess import PIPE, Popen
from flask import Flask, render_template, request, render_template_string, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

# with open(file="templates/index.html", mode="r") as file:
#     source = file.read()

def extract_users():
    os.system("net user >> users.txt")

    with open(file="users.txt", mode="r") as file_users:
        data_users = file_users.readlines()

    os.system("del /f users.txt")
    users = data_users[4:-2]
    list_of_users = []

    for line in users:
        elements = line.strip("\n").split(" ")
        while "" in elements:
            elements.remove("")
        for element in elements:
            list_of_users.append(element)
    return list_of_users


def check_user_info(username):
    net_user_info = cmdline(f"net user {username}")



def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


def return_info(user):
    os.system(f"net user {user} > users_test_info.txt")

    with open("users_test_info.txt", mode="r") as user_info_file:
        user_info = user_info_file.readlines()

    os.system("del /f users_test_info.txt")
    user_info = user_info[0:-2]

    for element in user_info:
        element.replace("\n", "")
        if element == '\n':
            user_info.remove(element)

    list_of_parameters = []
    for line in user_info:
        elements = line.strip("\n").split(" ")
        elements[7] = "|"
        while "" in elements:
            elements.remove("")
        list_of_parameters.append(elements)

    username = " ".join(str(e) for e in list_of_parameters[0]).split("|")
    fullname = " ".join(str(e) for e in list_of_parameters[1]).split("|")
    comment = " ".join(str(e) for e in list_of_parameters[2]).split("|")
    user_comment = " ".join(str(e) for e in list_of_parameters[3]).split("|")
    region_code = " ".join(str(e) for e in list_of_parameters[4]).split("|")
    account_active = " ".join(str(e) for e in list_of_parameters[5]).split("|")
    account_expires = " ".join(str(e) for e in list_of_parameters[6]).split("|")
    password_last_set = " ".join(str(e) for e in list_of_parameters[7]).split("|")
    password_expires = " ".join(str(e) for e in list_of_parameters[8]).split("|")
    password_changeable = " ".join(str(e) for e in list_of_parameters[9]).split("|")
    password_required = " ".join(str(e) for e in list_of_parameters[10]).split("|")
    user_may_change_password = " ".join(str(e) for e in list_of_parameters[11]).split("|")
    workstations_allowed = " ".join(str(e) for e in list_of_parameters[12]).split("|")
    logon_script = " ".join(str(e) for e in list_of_parameters[13]).split("|")
    user_profile = " ".join(str(e) for e in list_of_parameters[14]).split("|")
    home_directory = " ".join(str(e) for e in list_of_parameters[15]).split("|")
    last_logon = " ".join(str(e) for e in list_of_parameters[16]).split("|")
    logon_hours_allowed = " ".join(str(e) for e in list_of_parameters[17]).split("|")
    local_group_memberships = " ".join(str(e) for e in list_of_parameters[18]).split("|")

    global_group = list_of_parameters[19:len(list_of_parameters)]

    global_group_memberships = []
    for group in global_group:
        for element in group:
            if element != "|":
                global_group_memberships.append(element)

    global_group_memberships = " ".join(str(e) for e in global_group_memberships).split("*")


    user_params = {
        username[0]: username[1],
        fullname[0]: fullname[1],
        comment[0]: comment[1],
        user_comment[0]: user_comment[1],
        region_code[0]: region_code[1],
        account_active[0]: account_active[1],
        account_expires[0]: account_expires[1],
        password_last_set[0]: password_last_set[1],
        password_expires[0]: password_expires[1],
        password_changeable[0]: password_changeable[1],
        password_required[0]: password_required[1],
        user_may_change_password[0]: user_may_change_password[1],
        workstations_allowed[0]: workstations_allowed[1],
        logon_script[0]: logon_script[1],
        user_profile[0]: user_profile[1],
        home_directory[0]: home_directory[1],
        last_logon[0]: last_logon[1],
        logon_hours_allowed[0]: logon_hours_allowed[1],
        local_group_memberships[0]: local_group_memberships[1],
        global_group_memberships[0]: global_group_memberships[1:len(global_group_memberships)]
    }

    return user_params


def transform_in_json(users_list):
    users = users_list
    users = users[0:4]
    list_of_dicts = []
    for user in users:
        user_info = return_info(user)
        list_of_dicts.append(user_info)

    dicts = {users[n]: list_of_dicts[n] for n in range(len(list_of_dicts))}
    # print(dicts)

    with open(file="users.json", mode="w") as json_file:
        json.dump(dicts, json_file, indent=4)

class MyForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired()])
    begin_date = StringField('Start Date(DD.MM.YYYY):', validators=[InputRequired()])
    fin_date = StringField('Final Date(DD.MM.YYYY):', validators=[InputRequired()])
    message = TextAreaField('Message:', validators=[InputRequired()])

class UserForm(FlaskForm):
    comment = StringField('Change Comment:', validators=[])
    status = StringField('Change Status(Yes=active/No=blocked):', validators=[])
    reset_pass = PasswordField('Reset Password:', validators=[])
    # auto_block = SubmitField(label="AutoBlock")


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        print("succes")
        username = form.username.data
        begin_date = form.begin_date.data
        fin_date = form.fin_date.data
        message = form.message.data

        with open(file="start_data.txt", mode="a") as start_file:
            start_file.write(f"{username}|{begin_date}|{begin_date}-{fin_date} {message}\n")

        with open(file="fin_data.txt", mode="a") as fin_file:
            fin_file.write(f"{username}|{fin_date}\n")

        return f'Username: {username} ' \
               f'<br> Start Date: {begin_date}' \
               f'<br> Final Date: {fin_date}' \
               f'<br> Message: {message} '
    return render_template('index.html', form=form)

users = extract_users()
transform_in_json(users)

with open(file="users.json", mode="r") as file_json:
    json_data = json.load(file_json)

@app.route('/users/', methods=['GET', 'POST'])
def users():
    form = UserForm()
    username = request.args.get('username', default="*", type=str)
    if username in extract_users():
        if form.validate_on_submit():
            if request.form.get("change_comment") == "Change":
                comment = form.comment.data
                os.system(f'net user {username} /comment:"{comment}"')
                return f'<h1>Comment: "{comment}" for User: {username} is submitted successfully!!'
            elif request.form.get("change_status") == "Change":
                status = form.status.data.lower()
                os.system(f'net user {username} /active:"{status}"')
                return f'<h1>Status: "{status}" for User: {username} is submitted successfully!! </h1>'
            elif request.form.get("reset_pass") == "ResetPass":
                reset_pass = form.reset_pass.data
                os.system(f'start notepad.exe')
                return f'<h1>Pass: "{reset_pass}" is submitted successfully!! </h1>'
            else:
                pass

        return render_template("user.html", username=username, json_data=json_data, form=form)
    return render_template("users.html", users=extract_users(), form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
