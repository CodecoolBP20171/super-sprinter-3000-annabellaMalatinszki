from flask import Flask, request, render_template, url_for, redirect, flash
app = Flask(__name__)
app.debug = True


def open_file(file_name):
    with open(file_name) as file:
        lines = file.readlines()
    contents = [element.replace("\n", "").split(",") for element in lines]
    return contents


def append_file(file_name, new_line):
    with open(file_name, "a")as f:
        f.write(new_line)


def write_to_file(file_name, contents):
    with open(file_name, "w") as f:
        for row in contents:
            new_line = ','.join(row)
            f.write(new_line + "\n")


def update_file(file_name, edited_line, story_id):
    contents = open_file("user_stories.csv")
    contents = [item if item[0] != story_id else edited_line for item in contents]
    write_to_file("user_stories.csv", contents)


@app.route('/', methods=["GET", "POST"])
@app.route('/list', methods=["GET", "POST"])
def list():
    contents = open_file("user_stories.csv")
    return render_template("list.html", contents=contents)


@app.route('/story', methods=['GET', 'POST'])
@app.route('/story/<int:story_id>', methods=['GET', 'POST'])
def story(story_id=None):
    if story_id:
        contents = open_file("user_stories.csv")
        for line in contents:
            if str(story_id) in line:
                return render_template("form.html", story_id=story_id, line=line)
    else:
        return render_template("form.html")


@app.route('/delete/<int:story_id>', methods=['GET'])
def delete(story_id):
    contents = open_file("user_stories.csv")
    if request.method == "GET":
        del contents[story_id - 1]
        write_to_file("user_stories.csv", contents)
        return redirect(url_for('list'))


@app.route('/create', methods=['POST'])
def create():
    contents = open_file("user_stories.csv")
    new_content = []
    new_content.append(str(int(len(contents) + 1)))
    if request.method == "POST":
        new_content += [
            request.form['title'],
            request.form['userstory'],
            request.form['criteria'],
            request.form['value'],
            request.form['time'],
            request.form['status']
        ]
        new_line = str(','.join(new_content))
        append_file("user_stories.csv", new_line)
        return redirect(url_for('list'))


@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        edited_line = []
        story_id = request.form['story_id']
        edited_line.append(story_id)
        edited_line += [
            (request.form['title']),
            (request.form['userstory']),
            (request.form['criteria']),
            (request.form['value']),
            (request.form['time']),
            (request.form['status'])
        ]
        update_file("user_stories.csv", edited_line, story_id)
        return redirect(url_for('list'))


if __name__ == "__main__":
    app.run(debug=True)
