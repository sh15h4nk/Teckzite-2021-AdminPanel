from operator import iadd
from typing import ItemsView
from flask import session, url_for
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View

from app import app
from app.admin.controllers import current_user,login_required



nav = Nav()

@nav.navigation("my_nav")
@login_required
def my_nav():


	dashboard = View("Dashboard",'admin.dashboard')

	view_admin = View("Admin", 'admin.retriveAdminRows', role=1)
	add_admin = View("Add Admin",'admin.register')
	admin_menu = Subgroup("Admins",view_admin,add_admin)


	view_coord = View("Co-ordinators",'admin.retriveAdminRows', role=2)
	add_coord = View("Add Co-ordinators",'admin.register')
	coord_menu = Subgroup("Co-ordinators",view_coord,add_coord)


	view_orag = View("organisers",'admin.retriveAdminRows', role=3)
	add_orag = View("Add organisers",'admin.register')	#consider dept while extracting from database
	orag_menu = Subgroup("Organisers",view_orag,add_orag)


	view_events = View("Event",'admin.retriveEvents')			
	add_event = View("Add Event",'admin.addEvent')	#consider dept while extracting from database
	event_menu = Subgroup("Events",view_events,add_event)


	add_workshop = View("Add WorkShop",'admin.retriveWorkshops')
	view_workshops = View("Workshops",'admin.dashboard')
	workshop_menu = Subgroup("Workshops",view_workshops,add_workshop)

	view_tz_users = View("Users",'admin.dashboard')
	add_tz_user = View("Add User",'admin.dashboard')
	tz_users_menu = Subgroup("Tz Users",view_tz_users,add_tz_user)



	profile = View("Profile",'admin.dashboard')
	edit = View("Update",'admin.dashboard')
	profile_menu = Subgroup(current_user.id,profile,edit)

	logout = View("Logout", 'admin.logout')


	if current_user.role == 1:
		return Navbar('Teckzite\'21',dashboard,admin_menu,coord_menu,orag_menu,event_menu,workshop_menu,tz_users_menu,profile_menu,logout)
	elif current_user.role == 2:
		return Navbar('Teckzite\'21',dashboard,event_menu,profile_menu,logout)
	elif current_user.role == 3:
		return Navbar('Teckzite\'21',dashboard,profile_menu,logout)

