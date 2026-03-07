from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Card, db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    # ระบบค้นหา (Search) ตามโจทย์ข้อ 4
    search_query = request.args.get('q')
    if search_query:
        cards = Card.query.filter(Card.name.icontains(search_query), Card.user_id == current_user.id).all()
    else:
        cards = current_user.cards
    return render_template("home.html", user=current_user, cards=cards)

@views.route('/add-card', methods=['GET', 'POST'])
@login_required
def add_card():
    if request.method == 'POST':
        name = request.form.get('name')
        card_type = request.form.get('card_type')
        attribute = request.form.get('attribute')
        desc = request.form.get('description')
        
        new_card = Card(name=name, card_type=card_type, attribute=attribute, description=desc, user_id=current_user.id)
        db.session.add(new_card)
        db.session.commit()
        flash('เพิ่มการ์ดสำเร็จ!', category='success')
        return redirect(url_for('views.home'))
    return render_template("add_card.html", user=current_user)

@views.route('/delete-card/<int:id>')
@login_required
def delete_card(id):
    card = Card.query.get(id)
    if card and card.user_id == current_user.id:
        db.session.delete(card)
        db.session.commit()
    return redirect(url_for('views.home'))