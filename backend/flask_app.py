from flask import request
from db import app, db, User, Notebook, Page
from uuid import uuid4
from flask_cors import cross_origin
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def index():
    """
    It returns the string "hi there"
    :return: "hi there"
    """
    return "hi there"


@app.route("/api/users", methods=['GET'])
@cross_origin()
def get_all_users():
    """
    It gets all the users from the database and returns them as a list of dictionaries
    :return: A dictionary with a key of 'users' and a value of a list of dictionaries.
    """
    users = User.query.all()
    return {'users': [{'id': user.id, 'name': user.name} for user in users]}


@app.route("/api/users/<id>", methods=['GET'])
@cross_origin()
def get_user(id):
    """
    It gets a user from the database, and if it finds one, it returns a dictionary with the user's id,
    name, and password. If it doesn't find one, it returns a dictionary with an error message and a 404
    status code

    :param id: The id of the user to retrieve
    :return: A dictionary with a key of 'user' and a value of another dictionary with the keys 'id',
    'name', and 'password'
    """
    user = db.session.get(User, id)
    if user:
        return {'user': {
            'id': user.id,
            'name': user.name,
            'password': user.password
        }}
    else:
        return {'error': "User not found"}, 404


@app.route("/api/users", methods=['POST'])
@cross_origin()
def add_user():
    """
    It takes a JSON object from the request, creates a new user object, adds it to the database, and
    returns the new user object
    :return: A tuple of two values. The first value is a dictionary with the user's id, name, and
    password. The second value is the HTTP status code 201, which means "Created".
    """
    name = request.json['name']
    password = request.json['password']
    user = User(id=uuid4(), name=name, password=password)
    db.session.add(user)
    db.session.commit()
    return {'id': user.id, 'name': user.name, 'password': user.password}, 201


@app.route("/api/users/signin", methods=['POST'])
@cross_origin()
def signin():
    """
    If the user exists, return the user's id, name, and password. If the user doesn't exist, return an
    error message
    :return: A dictionary with a key of 'user' and a value of a dictionary with the keys 'id', 'name',
    and 'password'
    """
    name = request.json['name']
    password = request.json['password']
    user = User.query.filter_by(name=name, password=password).first()
    if user:
        return {'user': {
            'id': user.id,
            'name': user.name,
            'password': user.password
        }}
    else:
        return {'error': "User not found"}, 404


@app.route("/api/users/<id>", methods=['DELETE'])
@cross_origin()
def remove_user(id):
    """
    It deletes a user from the database if the user exists

    :param id: The id of the user to be deleted
    :return: A tuple of a dictionary and an integer.
    """
    user = db.session.get(User, id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
    else:
        return {"error": "User not found"}, 404


@app.route('/api/users/<user_id>/notebooks', methods=['GET'])
@cross_origin()
def get_user_notebooks(user_id):
    """
    It takes a user_id, finds all the notebooks associated with that user_id, and returns a dictionary
    with a key of 'notebooks' and a value of a list of dictionaries, each of which has a key of 'id' and
    a key of 'title' and the corresponding values

    :param user_id: The id of the user whose notebooks you want to retrieve
    :return: A dictionary with a key of 'notebooks' and a value of a list of dictionaries.
    """
    notebooks = Notebook.query.filter_by(user_id=user_id).all()
    return {'notebooks': [{'id': notebook.id, 'title': notebook.title} for notebook in notebooks]}


@app.route('/api/users/<user_id>/notebooks', methods=['POST'])
@cross_origin()
def add_user_notebook(user_id):
    """
    > This function adds a notebook to the database

    :param user_id: The user id of the user who is adding the notebook
    :return: A tuple of a dictionary and an integer.
    """
    title = request.json['title']
    db.session.add(Notebook(id=uuid4(), user_id=user_id, title=title))
    db.session.commit()
    return {"message": "Notebook added successfully"}, 201


@app.route('/api/users/<user_id>/notebooks/<notebook_id>', methods=['PUT'])
@cross_origin()
def rename_notebook(user_id, notebook_id):
    """
    It takes a user_id and a notebook_id, finds the notebook with that id and user_id, and if it exists,
    renames it to the title in the request.json

    :param user_id: The id of the user who owns the notebook
    :param notebook_id: The id of the notebook to be renamed
    :return: a tuple of a dictionary and an integer.
    """
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if notebook:
        notebook.title = request.json['title']
        db.session.commit()
        return {"message": "Notebook renamed successfully"}, 201
    else:
        return {'error': "Notebook not found or user is not authorized"}, 404


@app.route('/api/users/<user_id>/notebooks/<notebook_id>', methods=['DELETE'])
@cross_origin()
def delete_notebook(user_id, notebook_id):
    """
    It deletes a notebook from the database if the notebook exists and the user is authorized to delete
    it

    :param user_id: The id of the user who owns the notebook
    :param notebook_id: The id of the notebook to be deleted
    :return: A tuple of a dictionary and an integer.
    """
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if notebook:
        db.session.delete(notebook)
        db.session.commit()
        return {'message': 'Notebook deleted successfully.'}, 200
    else:
        return {'error': 'Notebook not found or user is not authorized.'}, 404


@app.route('/api/users/<user_id>/notebooks/<notebook_id>/pages', methods=['GET'])
@cross_origin()
def get_notebook_pages(user_id, notebook_id):
    """
    It takes a user_id and a notebook_id, finds the notebook with that id, and returns a dictionary with
    the notebook's id, title, and a list of pages

    :param user_id: The id of the user who owns the notebook
    :param notebook_id: The id of the notebook you want to get the pages for
    :return: A dictionary with the notebook id, title, and a list of pages.
    """
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if not notebook:
        return {"error": "Notebook not found or user is not authorized"}, 404
    pages = Page.query.filter_by(notebook_id=notebook_id).all()
    return {
        'id': notebook.id,
        'title': notebook.title,
        'pages': [{'id': page.id, 'title': page.title, 'content': page.content} for page in pages]}


@app.route('/api/users/<user_id>/notebooks/<notebook_id>/pages', methods=['POST'])
@cross_origin()
def add_notebook_pages(user_id, notebook_id):
    """
    It adds a page to a notebook

    :param user_id: The user id of the user who created the notebook
    :param notebook_id: The id of the notebook to which the page will be added
    :return: a tuple of a dictionary and an integer.
    """
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if not notebook:
        return {"error": "Notebook not found or user is not authorized"}, 404
    title = request.json['title']
    content = request.json['content']
    db.session.add(Page(id=uuid4(), notebook_id=notebook_id,
                        title=title, content=content))
    db.session.commit()
    return {"message": "Page added successfully"}, 201


@app.route('/api/users/<user_id>/notebooks/<notebook_id>/pages/<page_id>', methods=['GET'])
@cross_origin()
def get_current_page(user_id, notebook_id, page_id):
    """
    It gets the current page by querying the database for the page with the given page_id and
    notebook_id, and then returns the page's id, title, and content

    :param user_id: The id of the user who owns the notebook
    :param notebook_id: The id of the notebook that the page belongs to
    :param page_id: The id of the page you want to get
    :return: A dictionary with a key of 'page' and a value of a dictionary with keys of 'id', 'title',
    and 'content'
    """
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if not notebook:
        return {'error': 'Notebook not found or user is not authorized.'}, 404
    page = Page.query.filter_by(id=page_id, notebook_id=notebook_id).first()
    if not page:
        return {'error': 'Page not found or user is not authorized.'}, 404
    return {'page': {'id': page.id, 'title': page.title, 'content': page.content}}


@app.route('/api/users/<user_id>/notebooks/<notebook_id>/pages/<page_id>', methods=['PUT'])
@cross_origin()
def update_page(user_id, notebook_id, page_id):
    """
    It takes a user_id, notebook_id, and page_id, and updates the page with the new title and content

    :param user_id: The id of the user who owns the notebook
    :param notebook_id: The id of the notebook that the page belongs to
    :param page_id: The id of the page to update
    :return: A dictionary with a message and a page.
    """
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if not notebook:
        return {'error': 'Notebook not found or user is not authorized.'}, 404
    page = Page.query.filter_by(id=page_id, notebook_id=notebook_id).first()
    if not page:
        return {'error': 'Page not found or user is not authorized.'}, 404

    page.title = request.json['title']
    page.content = request.json['content']
    db.session.commit()

    return {"message": "Page updated successfully", 'page': {'id': page.id, 'title': page.title, 'content': page.content}}


@app.route('/api/users/<user_id>/notebooks/<notebook_id>/pages/<page_id>', methods=['DELETE'])
@cross_origin()
def delete_page(user_id, notebook_id, page_id):
    """
    It deletes a page from a notebook if the notebook exists and the page exists

    :param user_id: The id of the user who owns the notebook
    :param notebook_id: The id of the notebook that the page belongs to
    :param page_id: The id of the page to be deleted
    :return: The return value is a tuple of the response object and the HTTP status code.
    """
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if not notebook:
        return {'error': 'Notebook not found or user is not authorized.'}, 404
    page = Page.query.filter_by(id=page_id, notebook_id=notebook_id).first()
    if page:
        db.session.delete(page)
        db.session.commit()
        return {'message': 'Page deleted successfully.'}, 200
    else:
        return {'error': 'Page not found or user is not authorized.'}, 404


# It's a way to make sure that the code in the if statement only runs when the file is run directly.
if __name__ == '__main__':
    app.run()
