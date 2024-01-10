import streamlit as st
from queries import find_devices
from devices import Device
from datetime import datetime

# Eine Überschrift der ersten Ebene
st.write("# Gerätemanagement")

# Eine Überschrift der zweiten Ebene
st.write("## Geräteauswahl")

# Tabs mit den Use Cases
tab1, tab2, tab3, tab4 = st.tabs(["Geräte Verwaltung", "Nutzer Verwaltung", "Reservierungssystem", "Wartungs-Management"])

with tab1:
    st.header("Geräte Verwaltung")
    st.write("Hier können Sie Geräte verwalten")

    # Button zum Gerät anlegen
    if st.button("Gerät anlegen"):
        st.header("Gerät anlegen")
        
        with st.form("Neues Gerät"):
            device_name = st.text_input("Name des Geräts")
            responsible_person = st.text_input("Geräteverantwortlicher Nutzer")
            end_of_life = st.date_input("Ende der Wartung")
            first_maintenance = st.date_input("Erste Wartung")
            maintenance_interval = st.number_input("Wartungsintervall (Tage)", min_value=1)
            maintenance_cost = st.number_input("Wartungskosten", min_value=0.0)

            submitted = st.form_submit_button("Gerät speichern")

            if submitted:
                new_device = Device(
                    name=device_name,
                    responsible_person=responsible_person,
                    end_of_life=end_of_life,
                    first_maintenance=first_maintenance,
                    maintenance_interval=maintenance_interval,
                    maintenance_cost=maintenance_cost
                )
                
                new_device.store_data()  # Implementiere die Methode, um Daten zu speichern
                
                # Überprüfe, ob das Gerät korrekt gespeichert wurde
                loaded_device = Device.load_data_by_device_name(device_name)
                if loaded_device:
                    st.success("Gerät erfolgreich angelegt!")
                else:
                    st.error("Fehler beim Speichern des Geräts.")
                    
    # Button zum Gerät ändern
    if st.button("Gerät ändern"):
    # Hier kannst du den Code für das Ändern eines Geräts implementieren
        st.session_state.edit_device = True

    # Überprüfe, ob der Benutzer auf "Gerät ändern" geklickt hat und zeige dann den entsprechenden Abschnitt
    if "edit_device" in st.session_state and st.session_state.edit_device:
        st.header("Gerät ändern")

        devices_in_db = [device['device_name'] for device in Device.db_connector.all()]

        if devices_in_db:  # Überprüfe, ob Geräte vorhanden sind
            current_device_name = st.selectbox(
                'Gerät auswählen',
                options=devices_in_db, key="sbDevice_edit")

            if current_device_name in devices_in_db:
                loaded_device = Device.load_data_by_device_name(current_device_name)
                st.write(f"Loaded Device: {loaded_device}")

                with st.form("Device"):
                    st.text_input("Gerätname", value=loaded_device.device_name, key="device_name")
                    st.text_input("Geräte-Verantwortlicher", value=loaded_device.managed_by_user_id, key="managed_by_user_id")

                    submitted = st.form_submit_button("Daten speichern")
                    if submitted:
                        # Hier keine __last_update setzen, da TinyDB automatisch ein Timestamp-Feld erstellt
                        # loaded_device.__last_update = datetime.now()
                        loaded_device.managed_by_user_id = st.session_state.device_managed_by_user_id
                        loaded_device.device_name = st.session_state.device_name

                        loaded_device.store_data()
                        st.success("Daten erfolgreich gespeichert!")
                        st.session_state.edit_device = False  # Setze den Status zurück, um auf die vorherige Seite zu wechseln
        # Anzeigen der Liste aller gespeicherten Geräte oder Vermerk, wenn keine vorhanden sind
        st.write("### Gespeicherte Geräte:")
        devices_in_db = [device['device_name'] for device in Device.db_connector.all()]
        if devices_in_db:
            for device_name in devices_in_db:
                st.write(f"- {device_name}")
        else:
            st.write("Kein Gerät gespeichert")

    with tab2:
        st.header("Nutzer Verwaltung")
        st.write("Hier können neue Nutzer angelegt werden")

        # Administrator wählt Nutzer anlegen
        if st.button("Nutzer anlegen"):
            st.header("Nutzer anlegen")

            # Administrator gibt Nutzerdaten ein
            with st.form("Neuer Nutzer"):
                user_email = st.text_input("E-Mail-Adresse des Nutzers")
                user_name = st.text_input("Name des Nutzers")

                submitted = st.form_submit_button("Nutzer anlegen")

                # System speichert Nutzerdaten
                if submitted:
                    new_user = User(id=user_email, name=user_name)
                    # Annahme: Hier wird die Methode zum Speichern der Nutzerdaten implementiert
                    # Beispiel: new_user.store_data()
                
                    st.success("Nutzer erfolgreich angelegt!")

            
    with tab3:
        st.header("Reservierungssystem")
        st.write("Hier können Sie Reservierungen verwalten")

        # Administrator wählt Gerät aus
        devices_in_db = find_devices()
        if devices_in_db:
            selected_device = st.selectbox('Gerät auswählen', options=devices_in_db, key="sbDevice_reservation")

        # Administrator gibt Reservierungsdaten ein
        reservation_start = st.date_input("Startdatum der Reservierung")
        reservation_end = st.date_input("Enddatum der Reservierung")
        user_name = st.text_input("Name des reservierenden Nutzers")

        # Validierung bestehender Reservierungen
        # (Hier können Sie Ihre Validierungslogik implementieren)

        # Administrator bestätigt Eingabe
        if st.button("Reservierung bestätigen"):
            # System speichert Reservierungsdaten
            # (Hier können Sie den Code zum Speichern der Reservierung implementieren)

            st.success("Reservierung erfolgreich gespeichert!")

        else:
            st.warning("Es sind keine Geräte vorhanden. Bitte legen Sie zuerst ein Gerät an.")

with tab4:
    st.header("Wartungs-Management")
    st.write("Hier erhalten Sie einen Überblick über Wartungen und Wartungskosten")

    # System zeigt nächste Wartungstermine an
    st.write("Nächste Wartungstermine")

    # Annahme: Hier werden die nächsten Wartungstermine für alle Geräte angezeigt
    current_date = datetime.now()
    next_maintenance_list = []

    # Annahme: 'maintenance_interval' ist in Tagen definiert
    for device in find_devices():
        loaded_device = Device.load_data_by_device_name(device)
        if loaded_device:
            next_maintenance_date = loaded_device.first_maintenance + timedelta(days=loaded_device.maintenance_interval)
            if next_maintenance_date >= current_date:
                next_maintenance_list.append({
                    "Gerät": device,
                    "Nächste Wartung": next_maintenance_date.strftime("%Y-%m-%d")
                })

    if next_maintenance_list:
        st.table(next_maintenance_list)
    else:
        st.info("Keine bevorstehenden Wartungen.")

    # System zeigt Wartungskosten pro Quartal an
    st.write("Wartungskosten pro Quartal")

    # Annahme: Hier werden die Wartungskosten pro Quartal für alle Geräte angezeigt
    quarterly_costs_list = []

    for device in find_devices():
        loaded_device = Device.load_data_by_device_name(device)
        if loaded_device:
            quarterly_cost = loaded_device.maintenance_cost * 4  # Annahme: Wartungskosten pro Quartal
            quarterly_costs_list.append({
                "Gerät": device,
                "Wartungskosten pro Quartal": quarterly_cost
            })

    if quarterly_costs_list:
        st.table(quarterly_costs_list)
    else:
        st.info("Keine Wartungskosten für Geräte vorhanden.")        
