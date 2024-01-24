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
tabs = ["Geräteverwaltung", "Nutzerverwaltung", "Wartungsmanagement"]
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

            # Jetzt wird der "Speichern"-Button hinzugefügt
            if st.button("Gerät speichern"):
                new_device = Device(device_name, responsible_user_id, new_reservation)
                new_device.store_data()
                st.success("Gerät erfolgreich angelegt!")

    elif operation == "Gerät ändern":
        st.write("### Gerät ändern")

        # Lade alle vorhandenen Geräte für die Auswahl
        all_devices = Device.load_all_devices()
        device_names = [device.device_name for device in all_devices]

        selected_device_name = st.selectbox("Gerät auswählen", device_names)

        # Finde das ausgewählte Gerät anhand des Namens
        selected_device = next((device for device in all_devices if device.device_name == selected_device_name), None)

        if selected_device:
            st.write(f"Gerät gefunden: {selected_device}")

            # Jetzt wird der "Speichern"-Button hinzugefügt
            if st.button("Gerät speichern"):
                # Änderungen am Gerät vornehmen und speichern
                selected_device.store_data()
                st.success("Gerät erfolgreich geändert!")

        else:
            st.warning("Gerät nicht gefunden. Bitte überprüfen Sie den Gerätenamen.")


# Tab "Nutzerverwaltung"
elif selected_tab == "Nutzerverwaltung":
    st.write("## Nutzerverwaltung")

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
