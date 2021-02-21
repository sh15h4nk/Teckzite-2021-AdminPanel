from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View

from app import app
from flask_login import current_user,login_required



mynav = Nav()

@login_required
@mynav.navigation("my_nav")
def my_nav():

	


	if current_user.role == 1:
		dashboard = View("Dashboard",'admin.dashboard')

		view_admin = View("Admin", 'admin.getAdminsView')
		add_admin = View("Add Admin",'admin.addAdmin')
		admin_menu = Subgroup("Admins",view_admin,add_admin)


		view_coord = View("Co-ordinators",'admin.getCoordinatorsView')
		add_coord = View("Add Co-ordinators",'admin.addCoordinator')
		coord_menu = Subgroup("Co-ordinators",view_coord,add_coord)


		view_orag_mech = View("MECH",'admin.getOrganisersView',dept ='MEC')
		view_orag_cse = View("CSE",'admin.getOrganisersView',dept='CSE')
		view_orag_ece = View("ECE",'admin.getOrganisersView',dept='ECE')
		view_orag_civ = View("CIV",'admin.getOrganisersView',dept='CIV')
		view_orag_mme = View("MME",'admin.getOrganisersView',dept='MME')
		view_orag_che = View("CHE",'admin.getOrganisersView',dept='CHE')

		view_orag_puc = View("PUC",'admin.getOrganisersView',dept='PUC')

		orag_menu = Subgroup("Organisers",view_orag_mech, view_orag_cse, view_orag_ece, view_orag_civ, view_orag_mme, view_orag_che, view_orag_puc)


		# view_events = View("Event",'admin.getEventsView')
		view_event_mech = View("MECH",'admin.getEventsView',dept ='MEC')
		view_event_cse = View("CSE",'admin.getEventsView',dept='CSE')
		view_event_ece = View("ECE",'admin.getEventsView',dept='ECE')
		view_event_civ = View("CIV",'admin.getEventsView',dept='CIV')
		view_event_mme = View("MME",'admin.getEventsView',dept='MME')
		view_event_che = View("CHE",'admin.getEventsView',dept='CHE')

		view_event_puc = View("PUC",'admin.getEventsView',dept='PUC')

		add_event = View("Add Event",'admin.addEventView')	#consider dept while extracting from database
		event_menu = Subgroup("Events",view_event_mech, view_event_cse, view_event_ece, view_event_civ, view_event_mme, view_event_che, view_event_puc,add_event)


		add_workshop = View("Add WorkShop",'admin.addWorkshopView')
		view_workshops = View("Workshops",'admin.dashboard')
		workshop_menu = Subgroup("Workshops",view_workshops,add_workshop)

		view_tz_users = View("Users",'admin.dashboard')
		add_tz_user = View("Add User",'admin.dashboard')
		tz_users_menu = Subgroup("Tz Users",view_tz_users,add_tz_user)



		profile = View("Profile",'admin.dashboard')
		edit = View("Update",'admin.dashboard')
		profile_menu = Subgroup(current_user.userId,profile,edit)

		logout = View("Logout", 'admin.logout')


		return Navbar('Teckzite\'21',dashboard,admin_menu,coord_menu,orag_menu,event_menu,workshop_menu,tz_users_menu,profile_menu,logout)
	

	elif current_user.role == 2:

		dashboard = View("Dashboard",'coordinate.dashboard')


		view_events = View("Event",'coordinate.dashboard')			
		add_event = View("Add Event",'coordinate.dashboard')	#consider dept while extracting from database
		event_menu = Subgroup("Events",view_events,add_event)

		profile = View("Profile",'coordinate.dashboard')
		edit = View("Update",'coordinate.dashboard')
		profile_menu = Subgroup(current_user.id,profile,edit)

		logout = View("Logout", 'coordinate.logout')


		return Navbar('Teckzite\'21',dashboard,event_menu,profile_menu,logout)
	elif current_user.role == 3:

		dashboard = View("Dashboard",'organiser.dashboard')


		profile = View("Profile",'organiser.dashboard')
		edit = View("Update",'organiser.dashboard')
		profile_menu = Subgroup(current_user.id,profile,edit)

		logout = View("Logout", 'organiser.logout')

		return Navbar('Teckzite\'21',dashboard,profile_menu,logout)

