from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required 
from pokemon.extensions import db, bcrypt 
import sqlalchemy as sa

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
  page = request.args.get('page', type=int)   
  pokemons = db.paginate(sa.select(Pokemon), per_page=4, page=page)
  return render_template('core/index.html',
                         title='Home Page',
                         pokemons=pokemons)

@core_bp.route('/<int:id>/detail')
def detail(id):
  pokemon = db.session.get(Pokemon, id)
  return render_template('core/pokemon_detail.html',
                         title='Pokemon Detail Page',
                         pokemon=pokemon)

@core_bp.route('/change-password', methods=['GET', 'POST'])
@login_required 
def change_password():
    if request.method == 'POST':
        old_pw = request.form.get('old_password')
        new_pw = request.form.get('new_password')
        confirm_pw = request.form.get('confirm_password')

        if not bcrypt.check_password_hash(current_user.password, old_pw):
            flash('รหัสผ่านเดิมไม่ถูกต้อง', 'danger')
            return redirect(url_for('core.change_password'))

        if new_pw != confirm_pw:
            flash('รหัสใหม่และยืนยันรหัสไม่ตรงกัน', 'danger')
            return redirect(url_for('core.change_password'))

        hashed_pw = bcrypt.generate_password_hash(new_pw).decode('utf-8')
        current_user.password = hashed_pw
        db.session.commit() 

        flash('เปลี่ยนรหัสผ่านสำเร็จแล้ว!', 'success')
        return redirect(url_for('core.index'))
    
    return render_template('core/change_password.html')