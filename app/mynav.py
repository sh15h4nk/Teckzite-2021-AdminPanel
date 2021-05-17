from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View

from app import app
from flask_login import current_user,login_required



mynav = Nav()

@login_required
@mynav.navigation("my_nav")
def my_nav():

	if current_user.is_anonymous:
		index = View("index", 'index')

		return Navbar('Teckzite\'21',index)


	elif current_user.role == "admin":
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
	

	elif current_user.role == "event_manager":

		dashboard = View("Dashboard",'event_manager.dashboard')

		view_events = View("Event",'event_manager.dashboard')		
		add_event = View("Add Event",'event_manager.dashboard')
		event_menu = Subgroup("Events",view_events,add_event)

		view_coord = View("View",'event_manager.dashboard')
		add_coord = View("Add",'event_manager.dashboard')
		coord_menu = Subgroup("Event Co-ordinators",view_coord,add_coord)

		view_org = View("View",'event_manager.dashboard')
		orag_menu = Subgroup("Event Organisers",view_org)

		profile = View("Profile",'event_manager.dashboard')
		edit = View("Update",'event_manager.dashboard')
		profile_menu = Subgroup(current_user.userId,profile,edit)

		logout = View("Logout", 'event_manager.logout')

		return Navbar('Teckzite\'21',dashboard, event_menu, coord_menu, orag_menu, profile_menu, logout)
	

	elif current_user.role == "event_coordinator":

		dashboard = View("Dashboard",'event_coordinator.dashboard')

		view_events = View("Event",'event_manager.dashboard')		
		add_event = View("Add Event",'event_manager.dashboard')
		event_menu = Subgroup("Events",view_events,add_event)

		view_org = View("View",'event_manager.dashboard')
		orag_menu = Subgroup("Event Organisers",view_org)

		profile = View("Profile",'event_coordinator.dashboard')
		edit = View("Update",'event_coordinator.dashboard')
		profile_menu = Subgroup(current_user.userId,profile,edit)

		logout = View("Logout", 'event_coordinator.logout')

		return Navbar('Teckzite\'21',dashboard, event_menu, orag_menu, profile_menu, logout)

	elif current_user.role == "event_organiser":
		dashboard = View("Dashboard",'event_organiser.dashboard')

		view_event = View("My Event", 'event_organiser.dashboard')
		update_event = View("Edit Event", 'event_organiser.dashboard')

		profile = View("Profile",'event_organiser.dashboard')
		edit = View("Update",'event_organiser.dashboard')
		profile_menu = Subgroup(current_user.userId,profile,edit)

		logout = View("Logout", 'event_organiser.logout')

		return Navbar('Teckzite\'21',dashboard, view_event, update_event, profile_menu, logout)


	elif current_user.role == "workshop_manager":
		dashboard = View("Dashboard",'workshop_manager.dashboard')

		add_workshop = View("Add WorkShop",'workshop_manager.dashboard')
		view_workshops = View("Workshops",'workshop_manager.dashboard')
		workshop_menu = Subgroup("Workshops",view_workshops,add_workshop)

		view_coord = View("View",'workshop_manager.dashboard')
		add_coord = View("Add",'workshop_manager.dashboard')
		coord_menu = Subgroup("Workshop Co-ordinators",view_coord,add_coord)

		profile = View("Profile",'workshop_manager.dashboard')
		edit = View("Update",'workshop_manager.dashboard')
		profile_menu = Subgroup(current_user.userId,profile,edit)

		logout = View("Logout", 'workshop_manager.logout')

		return Navbar('Teckzite\'21',dashboard, workshop_menu, coord_menu, profile_menu,logout)

	elif current_user.role == "workshop_coordinator":
		dashboard = View("Dashboard",'workshop_coordinator.dashboard')

		view_workshop = View("My WorkShop", 'workshop_coordinator.dashboard')
		update_workshop = View("Edit WorkShop", 'workshop_coordinator.dashboard')

		profile = View("Profile",'workshop_coordinator.dashboard')
		edit = View("Update",'workshop_coordinator.dashboard')
		profile_menu = Subgroup(current_user.userId,profile,edit)

		logout = View("Logout", 'workshop_coordinator.logout')

		return Navbar('Teckzite\'21',dashboard, view_workshop, update_workshop, profile_menu, logout)
