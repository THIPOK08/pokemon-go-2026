from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# ตารางที่ 1: ระบบสมาชิก (โจทย์ข้อ 1)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # เชื่อมโยงไปยังตารางการ์ด (One-to-Many)
    cards = db.relationship('Card', backref='owner', lazy=True)

# ตารางที่ 2: ข้อมูลการ์ดยูกิ (โจทย์ข้อ 3)
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)   # ชื่อการ์ด
    card_type = db.Column(db.String(50))               # Monster, Spell, Trap
    attribute = db.Column(db.String(50))               # ธาตุ
    description = db.Column(db.Text)                  # ความสามารถ
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # เจ้าของการ์ด