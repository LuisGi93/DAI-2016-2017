# -*- coding: utf-8 -*-
# Import flask dependencies
from flask import Flask, render_template
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, json

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db,restaurantes

# Import module forms
from app.mod_auth.forms import LoginForm, RecipeForm, RegisterForm, BuscarRestaurantesForm, ModificarRestaurantesForm, InsertarRestaurantesForm

# Import module models (i.e. User)
#from app.mod_auth.models import User, Receta
from bson.json_util import dumps
import shelve, os

from lxml import etree
from sax_parser import ParseRssNews
from rsstwitter import PopularidadNoticias
# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/')

# Define the blueprint: 'auth', set its url prefix: app.url/auth
app = Flask(__name__)

numero_accesos = 0

@mod_auth.route('/', methods=['GET', 'POST'])
def redirigir():
    form = LoginForm(request.form)
    return render_template('index.html', form=form)

# Set the route and accepted methods



@mod_auth.route('signin/', methods=['GET', 'POST'])
def signin():
    """
    Permite a un usuario registrado en el sistema iniciar sesion.

        Returns:
            En caso de que los datos introducidos por el usuario en el formulario de login sean correctos
            redirige al usuario a una ventana de bienvenida.
            En caso de que los datos introducidos sean incorrectos redirige al usuario de nuevo al página del formulario
            de login
        """
    # If sign in form is submitted
    form = LoginForm(request.form)
    userdb= shelve.open('user.db')
    existe=""
    if form.validate_on_submit():
        try:
            existe=userdb[str(form.email.data)]
        finally:
            if existe:
				if existe['email']==form.email.data and existe['password']==form.password.data:
					flash('Usuario ya existe', 'error-message')
					session['user_id'] = form.email.data
					session['logged_in'] = True
					flash('You were logged in')
					form = LoginForm(request.form)
					userdb.close()
					return render_template("index.html", form=form,  usuario=form.email.data)
            else:
                return render_template("index.html", form=form)

    return render_template("index.html", form=form)


@mod_auth.route('sigup/', methods=['GET', 'POST'])
def signup():
    """
    Permite a un usuario registrarse en el sistema

        Returns:
            Si no existe un usuario con los datos introducidos en el sistema lo añade al sistema y le redirige a la página de inicio de sesión.
            Si existe entonces lo redirige a la página de inicio de sesión.
        """

    userdb= shelve.open('user.db')
    existe=""
    # If sign in form is submitted
    form = RegisterForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        try:
            existe=userdb[str(form.email.data)]
        finally:
            if existe:
                flash('Usuario ya existe', 'error-message')
                form = LoginForm(request.form)
                return redirect(url_for("auth.signin"))
            else:
                userdb[str(form.email.data)]={ 'name' : form.username.data, 'email' : form.email.data, 'password' : form.password.data }
                form = LoginForm(request.form)
                userdb.close()
                return redirect(url_for("auth.signin"))

    return render_template("sigup.html", form=form)

@mod_auth.route('modificar/', methods=['GET', 'POST'])
def modificar():
    """
    Permite a un usuario registrarse en el sistema

        Returns:
            Si no existe un usuario con los datos introducidos en el sistema lo añade al sistema y le redirige a la página de inicio de sesión.
            Si existe entonces lo redirige a la página de inicio de sesión.
        """

    if session['user_id'] != "":
        userdb= shelve.open('user.db', writeback=True)
        existe=""
        # If sign in form is submitted
        form = RegisterForm(request.form)

        # Verify the sign in form
        if form.validate_on_submit():
            try:
                existe=userdb[str(session['user_id'])]
                #existe=userdb[str(form.email.data)]
            finally:
                if existe:
		    #existe={ 'name' : form.username.data, 'email' : form.email.data, 'password' : form.password.data }
                    del userdb[str(session['user_id'])]
                    userdb[str(form.email.data)]={ 'name' : form.username.data, 'email' : form.email.data, 'password' : form.password.data }
                    flash('Usuario ya existe', 'error-message')
                    form = LoginForm(request.form)
                    userdb.close();
                    session['user_id']=form.email.data
                    return redirect(url_for("auth.signin"))
                else:
                    #existe={ 'name' : form.username.data, 'email' : form.email.data, 'password' : form.password.data }
                    #userdb[str(session['user_id'])]=existe
                    form = LoginForm(request.form)
                    userdb.close()
                    return redirect(url_for("auth.signin"))

    return render_template("modificar.html", form=form)


@mod_auth.route('logout/', methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it's there
    #session.pop('user_id', None)
    session.clear()
    #if session['user_id'] != "":
    return redirect(url_for("auth.signin"))

@mod_auth.route('show/', methods=['GET', 'POST'])
def show():
    if session['user_id'] != "":
        existing=""
        s = shelve.open('user.db')
        try:
            existing = s[str(session['user_id'])]
        finally:
            s.close()


            return render_template("show.html", user=existing)

@mod_auth.route('restaurantes/', methods=['GET', 'POST'])
def mostrar_restaurantes():
	if session['user_id'] != "":
		#restaurantes =db.restaurants
		form = BuscarRestaurantesForm(request.form)
        # Verify the sign in form
		if form.validate_on_submit():
				restaurante= restaurantes.find({"name": form.nombre.data})

				return render_template("mostrar_restaurantes.html", restaurante=dumps(restaurante))
		return render_template("mostrar_restaurantes.html", form=form)
	else:
		return redirect(url_for("auth.signin"))


@mod_auth.route('mrestaurantes/', methods=['GET', 'POST'])
def modificar_restaurantes():

	if session['user_id'] != "":
		#restaurantes =db.restaurants
            form = ModificarRestaurantesForm(request.form)
        # Verify the sign in form
            if form.validate_on_submit():
                restaurantes.update({"name":form.nombre.data},{"$set":{"cuisine":form.tcocina.data}})
                restaurante= restaurantes.find_one({"name": form.nombre.data})

                return render_template("mostrar_restaurantes.html", restaurante=restaurante)
            else:
				return render_template("mostrar_restaurantes.html", form=form)



	return redirect(url_for("auth.signin"))


@mod_auth.route('irestaurantes/', methods=['GET', 'POST'])
def introducir_restaurantes():

	if session['user_id'] != "":
		#restaurantes =db.restaurants
		form = InsertarRestaurantesForm(request.form)
        # Verify the sign in form
        if form.validate_on_submit():
                restaurantes.insert({"name":form.nombre.data,"address":{"building":form.bloque.data, "street":form.calle.data, "coord":[form.coordenada1.data,form.coordenada2.data]}, "cuisine":form.cocina.data, "restaurant_id":form.id.data})
                restaurante= restaurantes.find_one({"name": form.nombre.data})

                return render_template("mostrar_restaurantes.html", restaurante=restaurante)
        else:
				return render_template("mostrar_restaurantes.html", form=form)



	return redirect(url_for("auth.signin"))



@mod_auth.route('paginador/', methods=['GET', 'POST'])
def paginador():


				restaurante= restaurantes.find({"name": form.nombre.data})
				restaurantes.update({"name":form.nombre.data},{"$set":{"cuisine":form.tcocina.data}})

				return render_template("mostrar_restaurantes.html", restaurante=restaurante)


@mod_auth.route('nuevapagina/', methods=['GET', 'POST'])
def nuevapagina():
    pagina= request.args.get('pagina')

    if(pagina==None):
        pagina=1
    lista=restaurantes.find().skip((int(pagina)-1)*10).limit(10)


    tamanio=restaurantes.find().count()
    tamanio=int(tamanio/1000)

    return render_template("mostrar_restaurantes.html", restaurantes=lista, tamanio=tamanio)


@mod_auth.route('pagina/', methods=['GET', 'POST'])
def pagina():
    pagina= request.args.get('pagina')

    lista=restaurantes.find().skip((int(pagina)-1)*10).limit(10)

    return dumps(lista)


@mod_auth.route('rss/', methods=['GET', 'POST'])
def getrss():
    """
    Para evitar saturar de consultas twitter se consulta cada
    dos minutos y medio si no hay cambio de noticias para actualizar
    la gráfica de noticias del número de tweets relacionados con cada
    noticia, si hay cambio de noticias entonces se actualiza la gráfica
    independientemente del número de accessos

    """
    global numero_accesos

    noticia1= request.args.get('noticia1')
    noticia2= request.args.get('noticia2')
    noticia3= request.args.get('noticia3')


    parser_rss=ParseRssNews()
    parser = etree.XMLParser (target=parser_rss)
    etree.parse ('http://estaticos.elmundo.es/elmundo/rss/portada.xml', parser)

    lista=[]
    noticias=parser_rss.get_noticias()
    links=parser_rss.get_links_noticias()


    if(str(noticias[0])!= str(noticia1.encode('utf8')) or numero_accesos==5):
        print ' '
        print ' '
        print ' '
        print 'cambios'
        print noticias[0]
        print noticia1
        print 'cambios'
        print ' '
        print ' '
        print ' '
        numero_accesos=0
        obtener_popularidad=PopularidadNoticias()
        popularidad=[]
        for e in range(3):
            popularidad.append(obtener_popularidad.search(noticias[e]))

        for e in range(3):
            popularidad[e]

        for e in range(3):
                lista.append({'titulo': noticias[e], 'link': links[e], 'popularidad': popularidad[e]})

        return dumps(lista)
    else:
        numero_accesos +=1
        print ' '
        print ' '
        print ' '
        print 'sincambios'
        print noticias[0]
        print noticia1
        print 'sincambios'
        print ' '
        print ' '
        print ' '
        lista.append({'titulo': 'sincambios'})
        return dumps(lista)



@mod_auth.route('maps/', methods=['GET', 'POST'])
def maprestaurante():
	if session['user_id'] != "":

		return render_template("mostrar_restaurantes.html",  googlemaps=1)


	else:
		return redirect(url_for("auth.signin"))




@mod_auth.route('getcoordenadas/', methods=['GET', 'POST'])
def coordenadasrestaurante():
    nombre= request.args.get('restaurante')
    restaurante= restaurantes.find_one({"name": nombre})

    lista=[]
    lista.append({'zipcode':restaurante['address']['zipcode'],'calle':restaurante['address']['street'], 'longitud': restaurante['address']['coord'][0],'latitud': restaurante['address']['coord'][1]})

    print restaurante['address']['street']
    return dumps(lista)
