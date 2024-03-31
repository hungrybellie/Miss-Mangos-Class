from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Mom, Expert, Product, Comment, Post
from . import db

auth = Blueprint("auth", __name__)