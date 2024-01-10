### Erste Streamlit App

import streamlit as st
from queries import find_devices
from devices import Device

# Eine Überschrift der ersten Ebene
st.write("# Gerätemanagement")

#Tabs mit den Use Cases
tab1, tab2, tab3, tab4 = st.tabs(["Geräte Verwaltung", "Nutzer Verwaltung", "Reservierungssystem", "Wartungs-Management"])

with tab1:
    st.header("Geräte Verwaltung")
    st.write("Hier können Sie Geräte verwalten")
    
    # Eine Auswahlbox mit hard-gecoded Optionen, das Ergebnis wird in current_device_example gespeichert
    current_device = st.selectbox(
        'Aktion auswählen',
        options = ["Gerät anlegen", "Gerät ändern"], key="sbDevice_example")
    
    if current_device == "Gerät anlegen":
        st.subheader("Gerät anlegen")
        device_name = st.text_input("Gerätename eingeben", key="device_name_input")
        if st.button("Gerät anlegen"):
            st.success(f"Sie haben ein Gerät mit dem Namen '{device_name}' angelegt.")

    elif current_device == "Gerät ändern":
        st.write("Gerät ändern")


with tab2:
    st.header("Nutzer Verwaltung")
    st.write("Hier können Sie einen neuen Nutzer anlegen")
    
    nutzer_anlegen = st.text_input("Nutzername eingeben", key="nutzer_name_input")
    if st.button("Nutzer anlegen"):
        st.success(f"Sie haben einen Nutzer mit dem Namen '{nutzer_anlegen}' angelegt.")

with tab3:
    st.header("Reservierungssystem")
    auswahl_reservierungssystem = st.selectbox(
        'Aktion auswählen',
        options = ["Reservierung anzeigen", "Reservierung ein/austragen"], key="sbReservierungssystem")
    
    if auswahl_reservierungssystem == "Reservierung anzeigen":
        st.subheader("Reservierung anzeigen")
        st.write("Hier können Sie Reservierungen anzeigen")
    elif auswahl_reservierungssystem == "Reservierung ein/austragen":
        st.subheader("Reservierung ein/austragen")
        st.write("Hier können Sie Reservierungen ein/austragen")
    
    
with tab4:
    st.header("Wartungs-Management")
    auswahl_wartungsmanagement = st.selectbox(
        'Aktion auswählen',
        options = ["Wartung anzeigen", "Wartungskosten anzeigen"], key="sbWartungsmanagement")
    
    if auswahl_wartungsmanagement == "Wartung anzeigen":
        st.subheader("Wartung anzeigen")
        st.write("Hier können Sie Wartungen anzeigen")
    elif auswahl_wartungsmanagement == "Wartungskosten anzeigen":
        st.subheader("Wartungskosten anzeigen")
        st.write("Hier können Sie Wartungskosten anzeigen")