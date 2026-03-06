from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Card, db

views = Blueprint('views', __name__)

# แสดงข้อมูลและการค้นหา (Read & Search)
@views.route('/')
@login_required
def home():
    query = request.args.get('q')
    if query:
        # ระบบค้นหาข้อมูลตามชื่อการ์ด
        cards = Card.query.filter(Card.name.icontains(query), Card.user_id == current_user.id).all()
    else:
        cards = current_user.cards
    return render_template("home.html", user=current_user, cards=cards)

# เพิ่มข้อมูล (Create)
@views.route('/add-card', methods=['GET', 'POST'])
@login_required
def add_card():
    if request.method == 'POST':
        name = request.form.get('name')
        new_card = Card(
            name=name, 
            card_type=request.form.get('card_type'),
            attribute=request.form.get('attribute'),
            description=request.form.get('description'),
            user_id=current_user.id
        )
        db.session.add(new_card)
        db.session.commit()
        flash('เพิ่มการ์ดเรียบร้อยแล้ว!', category='success')
        return redirect(url_for('views.home'))
    return render_template("add_card.html", user=current_user)

# แก้ไขข้อมูล (Update)
@views.route('/edit-card/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_card(id):
    card = Card.query.get_or_404(id)
    if card.user_id != current_user.id:
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        card.name = request.form.get('name')
        card.card_type = request.form.get('card_type')
        card.attribute = request.form.get('attribute')
        card.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('views.home'))
    
    return render_template("edit_card.html", user=current_user, card=card)

# ลบข้อมูล (Delete)
@views.route('/delete-card/<int:id>')
@login_required
def delete_card(id):
    card = Card.query.get(id)
    if card and card.user_id == current_user.id:
        db.session.delete(card)
        db.session.commit()
    return redirect(url_for('views.home'))