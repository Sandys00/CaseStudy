import streamlit as st
from queries import find_devices
from devices import Device
from devices import reservation
from users import User
from tinydb import Query
from datetime import datetime
from tinydb_serialization import SerializationMiddleware

# Eine Überschrift der ersten Ebene
st.write("# Gerätemanagement")
devices_in_db = find_devices()
# Tabs für verschiedene Funktionen
tabs = ["Geräteverwaltung", "Nutzerverwaltung", "Reservierungen", "Wartungsmanagement"]
selected_tab = st.sidebar.selectbox("Wähle eine Funktion:", tabs)

# Tab "Geräteverwaltung"
if selected_tab == "Geräteverwaltung":
    st.write("## Geräteverwaltung")

    operation = st.radio("Operation auswählen", ["Gerät anlegen", "Gerät ändern"])

    if operation == "Gerät anlegen":
        st.write("### Gerät anlegen")

        device_name = st.text_input("Gerätename")
        responsible_user_id = st.text_input("Geräteverantwortlicher (Nutzer-ID)")

        # Annahme: Du hast eine Klasse User mit einer Methode zum Laden von Nutzern nach Nutzer-ID
        responsible_user = User.load_user_by_id(responsible_user_id)

        start_date = datetime.strptime("2022-01-24", "%Y-%m-%d")
        end_date = datetime.strptime("2022-01-25", "%Y-%m-%d")
        new_reservation = reservation("Test Reservation", start_date, end_date)

        if responsible_user:
            st.write(f"Verantwortlicher Nutzer: {responsible_user.name}")

            # Hier könntest du weitere Eingabefelder für andere Gerätedaten hinzufügen
            end_of_life = st.date_input("End of life")
            first_maintenance = st.date_input("First maintenance")
            next_maintenance = st.date_input("Next maintenance")
            maintenance_interval = st.number_input("Maintenance interval")
            maintenance_cost = st.number_input("Maintenance cost")
            

            # Jetzt wird der "Speichern"-Button hinzugefügt
            if st.button("Gerät speichern"):
                new_device = Device(device_name,
                                    responsible_user_id, 
                                    end_of_life, first_maintenance, 
                                    next_maintenance, 
                                    maintenance_interval, 
                                    maintenance_cost)
                new_device.store_data()
                st.success("Gerät erfolgreich angelegt!")

    elif operation == "Gerät ändern":
        st.write("### Gerät ändern")

        # Lade alle vorhandenen Geräte für die Auswahl
        all_device_names = Device.get_all_names()
        device_name = st.selectbox("Gerät auswählen", all_device_names)
        show_code = 0
        col1, col2 = st.columns(2)

        # Button "Gerätedaten anzeigen"
        if col1.button("Gerätedaten anzeigen"):
            show_code = 1

        # Button "Gerätedaten ausblenden"
        if col2.button("Gerätedaten ausblenden"):
            show_code = 0
        
        if show_code:
            device = Device.load_device_by_name(device_name)
            device["device_name"] = st.text_input("Gerätename", device["device_name"])
            device["managed_by_user_id"] = st.text_input("Geräteverantwortlicher (Nutzer-ID)", device["managed_by_user_id"])
            device["end_of_life"] = st.date_input("End of life", device["end_of_life"])
            device["first_maintenance"] = st.date_input("First maintenance", device["first_maintenance"])
            device["next_maintenance"] = st.date_input("Next maintenance", device["next_maintenance"])
            device["_Device__maintenance_interval"] = st.number_input("Maintenance interval", device["_Device__maintenance_interval"])
            device["_Device__maintenance_cost"] = st.number_input("Maintenance cost", device["_Device__maintenance_cost"])
                
            
            
            if st.button("Gerät ändern"):
                #hier code zum speichern reinschreiben
                changed_device = Device(
                                        device_name=device["device_name"],
                                        managed_by_user_id=device["managed_by_user_id"],
                                        end_of_life=device["end_of_life"],
                                        first_maintenance=device["first_maintenance"],
                                        next_maintenance=device["next_maintenance"],
                                        maintenance_interval=device["_Device__maintenance_interval"],
                                        maintenance_cost=device["_Device__maintenance_cost"],
                                        reservation=device["reservation"]
                                        )    
                changed_device.store_data()                
                st.success("Gerät erfolgreich geändert!")
    


# Tab "Nutzerverwaltung"
elif selected_tab == "Nutzerverwaltung":
    st.write("## Nutzerverwaltung")

    tabs = ["Nutzer anlegen", "Nutzer löschen"]
    selected_tab_nutzer = st.radio("Wähle eine Funktion:", tabs)
    
    if selected_tab_nutzer == "Nutzer anlegen":
        with st.form("Nutzer hinzufügen"):
            user_id = st.text_input("ID")
            user_name = st.text_input("Name")

            # Bestätigungsbutton für das Hinzufügen eines neuen Benutzers
            submitted_new_user = st.form_submit_button("Nutzer hinzufügen")

            if submitted_new_user:
                # Überprüfe, ob der Benutzer bereits existiert
                if not user_name.lstrip() or not user_id.lstrip():
                    st.warning("Bitte füllen Sie alle Felder aus.")
                else:   
                    UserQuery = Query()
                    existing_user = User.db_connector.get(UserQuery.id == user_id)

                    if existing_user:
                        st.warning("Benutzer existiert bereits.")
                    else:
                        # Füge den neuen Benutzer zur Datenbank hinzu
                        new_user = User(id=user_id, name=user_name)
                        User.db_connector.insert(new_user.__dict__)
                        st.success("Benutzer erfolgreich hinzugefügt.")

    if selected_tab_nutzer == "Nutzer löschen":
        with st.form("Nutzer löschen"):            

            auswahl_deletion = st.radio("Nutzer löschen mit", ["Name", "ID"])
            
            if auswahl_deletion == "Name":
                user_name = st.text_input("Name")
            if auswahl_deletion == "ID":
                user_id = st.text_input("ID")

            submitted_delete_user = st.form_submit_button("Nutzer löschen")

            if submitted_delete_user:
                if auswahl_deletion == "Name":
                    if not user_name.lstrip():
                        st.warning("Bitte füllen Sie alle Felder aus.")
                    else:
                        UserQuery = Query()
                        existing_user = User.db_connector.get(UserQuery.name == user_name)

                        if existing_user:
                            User.db_connector.remove(UserQuery.name == user_name)
                            st.success("Benutzer erfolgreich gelöscht.")
                        else:
                            st.warning("Benutzer existiert nicht.")
                
                elif auswahl_deletion == "ID":
                    if not user_id.lstrip():
                        st.warning("Bitte füllen Sie alle Felder aus.")
                    else:
                        UserQuery = Query()
                        existing_user = User.db_connector.get(UserQuery.id == user_id)

                        if existing_user:
                            User.db_connector.remove(UserQuery.id == user_id)
                            st.success("Benutzer erfolgreich gelöscht.")
                        else:
                            st.warning("Benutzer-ID existiert nicht.")




elif selected_tab == "Reservierungen":
    st.success("success message")
    st.write("Ändern sie ihre Reservierungen hier")
    tabs_reservierung = ["Reservierung machen", "Reservierung ändern"]
    selected_tab_reservierung = st.radio("Wähle eine Funktion: ", tabs_reservierung)

    if selected_tab_reservierung == "Reservierung machen":

        st.write("Reservierung machen")
        all_device_names = Device.get_all_names()
        device_name_reservation = st.selectbox("Gerät auswählen", all_device_names)
        
        if st.button("Für dieses Gerät eine Reservierung vornehmen:   " + device_name_reservation):
            
            with st.form("Reservierung machen"):
                device_reservation = Device.load_device_by_name(device_name_reservation)
                start_reservation = st.date_input("Gebe hier den Startzeitpunkt der Reservierung ein:")
                end_reservation = st.date_input("Gebe hier den Endzeitpunkt der Reservierung ein:")
                device_reservation["reservation"] = reservation(device_name_reservation, start_reservation, end_reservation)
                print("before submitted")

                submit_button_reservation = st.form_submit_button("Hier Reservierung bestätigen")
                if submit_button_reservation:
                    print("submitted")
                    changed_device_reservation = Device(
                                                        device_name=device_reservation["device_reservation_name"],
                                                        managed_by_user_id=device_reservation["managed_by_user_id"],
                                                        end_of_life=device_reservation["end_of_life"],
                                                        first_maintenance=device_reservation["first_maintenance"],
                                                        next_maintenance=device_reservation["next_maintenance"],
                                                        maintenance_interval=device_reservation["_device__maintenance_interval"],
                                                        maintenance_cost=device_reservation["_device__maintenance_cost"],
                                                        reservation=device_reservation["reservation"]
                                                        )   
                    changed_device_reservation.store_data()
                    st.success("Reservierung angelegt")
                