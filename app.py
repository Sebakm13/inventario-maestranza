import streamlit as st
import pandas as pd


st.set_page_config(page_title="Maestranzas Unidos S.A. - Inventario", layout="wide")

st.title("⚙️ Sistema de Control de Inventarios - Maestranzas Unidos S.A.")
st.subheader("Ambiente de Pruebas y Desarrollo - Versión MVP (6 Meses)")


if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame([
        {"ID": 1, "Pieza": "Motor Hidráulico Rexroth", "N° Serie": "MH-9921", "Ubicación": "Estante A-3", "Stock": 5, "Stock Mínimo": 3},
        {"ID": 2, "Pieza": "Filtro de Aceite Pesado", "N° Serie": "FA-1102", "Ubicación": "Estante B-1", "Stock": 2, "Stock Mínimo": 10},
        {"ID": 3, "Pieza": "Rodamiento de Rodillos", "N° Serie": "RR-5541", "Ubicación": "Estante C-2", "Stock": 12, "Stock Mínimo": 5},
        {"ID": 4, "Pieza": "Lubricante Alta Temperatura (Lote Vence 12/26)", "N° Serie": "LUB-440", "Ubicación": "Zona Químicos Q1", "Stock": 15, "Stock Mínimo": 8},
    ])


st.sidebar.header("📥 Registrar Nueva Pieza")
with st.sidebar.form("formulario_registro"):
    nueva_pieza = st.text_input("Nombre de la Pieza/Componente (Ej: Rodamiento)")
    nuevo_serie = st.text_input("Número de Serie (Único)")
    nueva_ubica = st.text_input("Ubicación Física (Ej: Estante A-1)")
    nuevo_stock = st.number_input("Cantidad Inicial", min_value=0, value=10)
    nuevo_minimo = st.number_input("Stock Mínimo (Alerta)", min_value=1, value=5)
    
    boton_guardar = st.form_submit_button("Registrar en Sistema")
    
    if boton_guardar:
        if nueva_pieza and nuevo_serie and nueva_ubica:
            nuevo_id = len(st.session_state.inventario) + 1
            nueva_fila = {
                "ID": nuevo_id, "Pieza": nueva_pieza, "N° Serie": nuevo_serie, 
                "Ubicación": nueva_ubica, "Stock": nuevo_stock, "Stock Mínimo": nuevo_minimo
            }
            st.session_state.inventario = pd.concat([st.session_state.inventario, pd.DataFrame([nueva_fila])], ignore_index=True)
            st.sidebar.success("✅ Pieza registrada con éxito.")
        else:
            st.sidebar.error("❌ Por favor, rellena todos los campos obligatorios.")


st.header("🚨 Alertas de Reposición Urgente")

alertas = st.session_state.inventario[st.session_state.inventario['Stock'] <= st.session_state.inventario['Stock Mínimo']]

if not alertas.empty:
    for idx, row in alertas.iterrows():
        st.error(f"⚠️ **STOCK CRÍTICO:** Quedan solo **{row['Stock']}** unidades de '{row['Pieza']}' (Stock Mínimo: {row['Stock Mínimo']}). Ubicación: {row['Ubicación']}")
else:
    st.success("✅ Todos los niveles de stock están estables y sobre el mínimo.")


st.header("📦 Inventario General de la Maestranza")


buscar = st.text_input("🔍 Buscar pieza por Nombre o Número de Serie:")
df_mostrar = st.session_state.inventario
if buscar:
    df_mostrar = df_mostrar[df_mostrar['Pieza'].str.contains(buscar, case=False) | df_mostrar['N° Serie'].str.contains(buscar, case=False)]

st.dataframe(df_mostrar, use_container_width=True)


st.subheader("🔄 Registrar Consumo / Retiro de Pieza para Proyecto")
col1, col2 = st.columns(2)

with col1:
    pieza_seleccionada = st.selectbox("Seleccione la pieza que va a salir:", st.session_state.inventario['Pieza'].tolist())
with col2:
    cantidad_retirar = st.number_input("Cantidad a retirar para uso en faena:", min_value=1, value=1)

if st.button("Confirmar Transacción y Descontar"):
    idx_pieza = st.session_state.inventario[st.session_state.inventario['Pieza'] == pieza_seleccionada].index[0]
    stock_actual = st.session_state.inventario.at[idx_pieza, 'Stock']
    
    if stock_actual >= cantidad_retirar:
        st.session_state.inventario.at[idx_pieza, 'Stock'] = stock_actual - cantidad_retirar
        st.success(f"✔️ Éxito: Se retiraron {cantidad_retirar} unidades de '{pieza_seleccionada}'. Stock actualizado en tiempo real.")
        st.rerun()
    else:
        st.error("❌ Error: No hay suficiente stock disponible para realizar este retiro.")
