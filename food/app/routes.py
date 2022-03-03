from flask import Blueprint, render_template, request, redirect, url_for
from food.models import Food, Day
from food.extensions import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    days = Day.query.order_by(Day.date.desc()).all()

    day_foods = []

    for day in days:
        proteins = 0
        carbs = 0
        fats = 0
        calories = 0

        for food in day.foods:
            proteins += food.proteins
            carbs += food.carbs 
            fats += food.fats
            calories += food.calories

        day_foods.append({
            'day' : day,
            'proteins' : proteins,
            'carbs' : carbs,
            'fats' : fats,
            'calories' : calories
        })

    return render_template('index.html', day_foods = day_foods)


@main.route('/create-log', methods=['POST'])
def create_day():
    date = request.form.get('date')
    

    day = Day(date=datetime.strptime(date, '%Y-%m-%d'))
    db.session.add(day)
    db.session.commit()

    return redirect(url_for('main.view', id=day.id))

@main.route('/add')
def add():
    foods = Food.query.all()

    return render_template('add.html', foods=foods, food=None)

@main.route('/add', methods=['POST'])
def add_post():
    food_name = request.form.get('food-name')
    proteins = request.form.get('protein')
    carbs = request.form.get('carbohydrates')
    fats = request.form.get('fat')

    food_id = request.form.get('food-id')

    if food_id:
        food = Food.query.get(food_id)
        food.name = food_name
        food.proteins = proteins
        food.carbs = carbs
        food.fats = fats
        db.session.commit()
    else:
        new_food = Food(
            name = food_name,
            proteins = proteins,
            carbs = carbs,
            fats = fats
            )

        db.session.add(new_food)
        db.session.commit()

    return redirect(url_for('main.add'))


@main.route('/view/<int:id>')
def view(id):
    day = Day.query.get_or_404(id)
    foods = Food.query.all()

    totals = {
        'proteins': 0,
        'carbs': 0,
        'fats': 0,
        'calories': 0,
    }

    for food in day.foods:
        totals['proteins'] += food.proteins
        totals['carbs'] += food.carbs
        totals['fats'] += food.fats
        totals['calories'] += food.calories

    return render_template('view.html', foods=foods, day=day, totals=totals)


@main.route('/delete/<int:id>')
def delete_food(id):
    food = Food.query.get(id)
    db.session.delete(food)
    db.session.commit()

    return redirect(url_for('main.add'))


@main.route('/edit/<int:id>')
def edit(id):
    food = Food.query.get(id)
    foods = Food.query.all()

    return render_template('add.html', food=food, foods=foods)

@main.route('/add_to_day/<int:day_id>', methods=['POST'])
def add_to_day(day_id):
    day = Day.query.get_or_404(day_id)
    selected_food = request.form.get('food-select')
    food = Food.query.get(int(selected_food))

    day.foods.append(food)
    db.session.commit()

    return redirect(url_for('main.view', id = day_id))


@main.route('/remove_food_from_day/<int:day_id>/<int:food_id>')
def remove_food_from_day(day_id, food_id):
    day = Day.query.get(day_id)
    food = Food.query.get(food_id)

    day.foods.remove(food)
    db.session.commit()
    return redirect(url_for('main.view', id=day_id))
