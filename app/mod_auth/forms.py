# Import Form and RecaptchaField (optional)
from flask_wtf import Form
from wtforms.fields import TextField, BooleanField, PasswordField, TextAreaField, IntegerField
# Import Form elements such as TextField and BooleanField (optional)


# Import Form validators
from wtforms.validators import Required, Email, EqualTo


# Define the login form (WTForms)

class LoginForm(Form):
    email    = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])

class RegisterForm(Form):
    username = TextField('Name', [
                Required(message='Introduce an username')])
    email    = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])


class RecipeForm(Form):
    titulo = TextField('Titulo', [
                Required(message='Must provide a title. ;-)')])
    descripcion    = TextAreaField('Introduce the recipe description:', [
                Required(message='You must introduce a description')])

class BuscarRestaurantesForm(Form):
    nombre = TextField('Nombre', [
                Required(message='Introduzca el nombre del diccionario del que desea buscar sus datos: ')])

class ModificarRestaurantesForm(Form):
    nombre = TextField('Nombre', [
                Required(message='Introduzca el nombre del diccionario del que desea buscar sus datos: ')])
    tcocina = TextField('Tipo cocina', [
                Required(message='Introduce el tipo de cocina del restaurante: ')])

class InsertarRestaurantesForm(Form):
    bloque = TextField('Bloque', [
                Required(message='Introduzca el nombre del diccionario del que desea buscar sus datos: ')])
    calle = TextField('Tipo cocina', [
                Required(message='Introduce el tipo de cocina del restaurante: ')])
    coordenada1 = IntegerField('Coordenada1', [
                Required(message='Introduzca el nombre del diccionario del que desea buscar sus datos: ')])

    coordenada2 = IntegerField('Coordenada2', [
                Required(message='Introduzca el nombre del diccionario del que desea buscar sus datos: ')])

    cocina = TextField('Tipo cocina', [
                Required(message='Introduce el tipo de cocina del restaurante: ')])
    nombre = TextField('Nombre', [
                Required(message='Introduzca el nombre del diccionario del que desea buscar sus datos: ')])
    id = TextField('Tipo cocina', [
                Required(message='Introduce el tipo de cocina del restaurante: ')])
