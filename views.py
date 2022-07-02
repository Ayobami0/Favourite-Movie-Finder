from flask import (
    Blueprint, request, redirect, render_template, url_for, flash)
import requests
import html

from random import randint

from model import MyForm

hello = Blueprint("hello", __name__)


favourite_movies_list = []


@hello.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm(csrf_enabled=False)
    page = 1
    if request.method == "POST":
        t = form.search_bar.data  # t==title
        return redirect(url_for(
            'hello.search_result',
            page=page,
            title=t)
            )
    return render_template(
                        'home.html',
                        form=form,
                        favourite_movies=favourite_movies_list)


@hello.route("/info/<movie_title>", methods=['GET', 'POST'])
def movie_page(movie_title):
    error = ''
    movie_data = requests.get(
            url=f'http://www.omdbapi.com/?apikey=22a96d18&plot=full&t={movie_title}'
                ).json()
    if request.method == "POST":
        if request.form["fav_toggle"] == 'add':
            for movie in favourite_movies_list:
                if movie_data['title'] == movie:
                    error = "Movie already exist in favourites"
                    flash(error, "error")
                    return redirect(url_for(
                        'hello.movie_page',
                        movie_title=movie_title))
            favourite_movies_list.append(movie_data)
            flash('Movie added to favourite', 'success')
        elif request.form["fav_toggle"] == 'remove':
            favourite_movies_list.remove(movie_data)
            flash("Removed from favourites", "success")
        return redirect(url_for('hello.movie_page', movie_title=movie_title))
    return render_template('movie_info.html', movie_data=movie_data)


@hello.route("/random")
def find_random_movie():
    id = randint(1111111, 9999999)
    imdb_id = f"tt{id}"
    data = requests.get(
                url=f'http://www.omdbapi.com/?apikey=22a96d18&plot=full&i={imdb_id}'
                ).json()
    if 'Error' in data:
        return redirect(url_for('hello.index'))
    movie_data = {
            'title': data['Title'],
            'year': data['Year'],
            'plot': data['Plot'],
            'poster': data['Poster'],
            }
    return redirect(
            url_for('hello.movie_page', movie_title=movie_data['title']))


@hello.route("/search/<title>", defaults={'page': 1})
@hello.route("/search/<title>/<int:page>")
def search_result(page, title):
    empty_icon = html.escape('∅', quote=False)
    try:
        result = requests.get(
                url=f'http://www.omdbapi.com/?apikey=22a96d18&s={title}&page={page}'
                ).json()
        result_list = result['Search']
    except KeyError:
        flash("Movie Title not found", "error")
        return redirect(url_for("hello.index"))
    total_results = int(result['totalResults'])
    total_page = round(total_results/10)
    return render_template(
            'search_page.html',
            result=result_list,
            page=page,
            total_page=total_page,
            empty=empty_icon,
            title=title,
           )
