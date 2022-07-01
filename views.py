from flask import (
    Blueprint, request, redirect, render_template, url_for, flash)
import requests
from random import randint

from model import MyForm

hello = Blueprint("hello", __name__)


favourite_movies = []


@hello.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm(csrf_enabled=False)

    if request.method == "POST":
        t = form.search_bar.data  # t==title
        data = requests.get(
                url=f'http://www.omdbapi.com/?apikey=22a96d18&plot=full&t={t}'
                ).json()

        global movie_data
        movie_data = {
                'title': data['Title'],
                'year': data['Year'],
                'plot': data['Plot'],
                'poster': data['Poster'],
                }
        return redirect(url_for(
            'hello.movie_page',
            movie_title=movie_data['title']))
    return render_template(
                        'base.html',
                        form=form, favourite_movies=favourite_movies)


@hello.route("/<movie_title>", methods=['GET', 'POST'])
def movie_page(movie_title):
    error = ''
    if request.method == "POST":
        if request.form["fav_toggle"] == 'add':
            for movie in favourite_movies:
                if movie_data['title'] == movie['title']:
                    error = "Movie already exist in favourites"
                    flash(error, "error")
                    return redirect(url_for(
                        'hello.movie_page',
                        movie_title=movie_title))
            favourite_movies.append(movie_data)
            flash('Movie added to favourite', 'success')
        elif request.form["fav_toggle"] == 'remove':
            favourite_movies[:] = [
                    movie for movie in favourite_movies
                    if movie['title'] != movie_data['title']]
            flash("Removed from favourites", "success")
        return redirect(url_for('hello.movie_page', movie_title=movie_title))
    return render_template('index.html', movie_data=movie_data)


@hello.route("/<movie_title>")
def get_movie_info(movie_title):
    for movie in favourite_movies:
        if movie['title'] == movie_title:
            global movie_data
            movie_data = movie
            return redirect(
                    url_for('hello.movie_page', movie_title=movie_title))


@hello.route("/random")
def find_random_movie():
    id = randint(1111111, 9999999)
    imdb_id = f"tt{id}"
    data = requests.get(
                url=f'http://www.omdbapi.com/?apikey=22a96d18&plot=full&i={imdb_id}'
                ).json()
    if 'Error' in data:
        return redirect(url_for('hello.index'))
    global movie_data
    movie_data = {
            'title': data['Title'],
            'year': data['Year'],
            'plot': data['Plot'],
            'poster': data['Poster'],
            }
    return redirect(
            url_for('hello.movie_page', movie_title=movie_data['title']))
