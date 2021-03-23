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

		view_admin = View("View", 'admin.getAdminsView')
		add_admin = View("Add",'admin.addAdmin')
		admin_menu = Subgroup("Admins",view_admin,add_admin)


		view_coord = View("View",'admin.getCoordinatorsView')
		add_coord = View("Add",'admin.addCoordinator')
		coord_menu = Subgroup("Co-ordinators",view_coord,add_coord)


		view_org = View("View",'admin.getOrganisersView')
		orag_menu = Subgroup("Organisers",view_org)


		view_events = View("Event",'admin.getEventsView')

		add_event = View("Add Event",'admin.addEventView')
		event_menu = Subgroup("Events",view_events, add_event)


		add_workshop = View("Add WorkShop",'admin.addWorkshopView')
		view_workshops = View("Workshops",'admin.getWorkshopsView')
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
		profile_menu = Subgroup(current_user.userId,profile,edit)

		logout = View("Logout", 'coordinate.logout')


		return Navbar('Teckzite\'21',dashboard,event_menu,profile_menu,logout)
	elif current_user.role == 3:

		dashboard = View("Dashboard",'organiser.dashboard')


		profile = View("Profile",'organiser.dashboard')
		edit = View("Update",'organiser.dashboard')
		profile_menu = Subgroup(current_user.userId,profile,edit)

		logout = View("Logout", 'organiser.logout')

		return Navbar('Teckzite\'21',dashboard,profile_menu,logout)

