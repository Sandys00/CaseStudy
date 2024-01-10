import
streamlit
as
st
# Eine Überschrift der ersten Ebene
st.write(
"# Gerätemanagement"
)
# Eine Überschrift der zweiten Ebene
st.write(
"## Geräteauswahl"
)
# Eine Auswahlbox mit hard-gecoded Optionen, das Ergebnis
# wird in current_device_example gespeichert
current_device_example = st.selectbox(
'Gerät auswählen'
, options = [
"Gerät_A"
,
"Gerät_B"
], key=
"sbDevice_example"
)st.write(
F"Das ausgewählte Gerät ist
{current_device_example}
"
)