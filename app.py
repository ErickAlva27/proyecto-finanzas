import streamlit as st
import pandas as pd
import numpy_financial as npf
import math

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sistema Financiero Pro", layout="wide", page_icon="📊")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #2c3e50; font-family: 'Segoe UI', sans-serif; }
    .metric-card {
        background-color: #ffffff;
        border-left: 5px solid #2980b9;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-card h3 { margin: 0; font-size: 22px; color: #2c3e50; }
    .metric-card p { margin: 0; font-size: 14px; color: #7f8c8d; }
    .highlight-table { background-color: white; padding: 10px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Sistema de Gestión Financiera y Presupuestal")

# --- NAVEGACIÓN ---
st.sidebar.title("Menú Principal")
modulo = st.sidebar.radio("Ir a:", [
    "Inicio",
    "1. Presupuestos",
    "2. Razones Financieras",
    "3. Evaluación de Proyectos"
])

# ==========================================
#        INICIO
# ==========================================
if modulo == "Inicio":
    st.markdown("### Bienvenido al Sistema Financiero")
    st.info("Seleccione un módulo en el menú lateral para comenzar.")
    
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='metric-card'><h3>Presupuestos</h3><p>Maestros y Operativos</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='metric-card'><h3>Ratios</h3><p>Liquidez y Rentabilidad</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='metric-card'><h3>Proyectos</h3><p>VAN, TIR y Reemplazo</p></div>", unsafe_allow_html=True)

# ==========================================
#        1. PRESUPUESTOS (RESUMIDO)
# ==========================================
elif modulo == "1. Presupuestos":
    st.header("Generador de Presupuestos")
    tabs = st.tabs(["Ventas", "Producción", "Materiales"])
    
    with tabs[0]:
        c1, c2 = st.columns(2)
        u = c1.number_input("Unidades", 1000)
        p = c2.number_input("Precio", 50.0)
        st.metric("Ventas Totales", f"${u*p:,.2f}")
    
    with tabs[1]:
        st.write("Cálculo de Producción Requerida")
        vp = st.number_input("Ventas (Unidades)", value=u)
        inv_f = st.number_input("Inventario Final", 200)
        inv_i = st.number_input("Inventario Inicial", 100)
        prod = vp + inv_f - inv_i
        st.success(f"Producción Requerida: **{prod}** unidades")

    with tabs[2]:
        st.info("Módulo de materiales disponible en versión completa.")

# ==========================================
#        2. RAZONES FINANCIERAS
# ==========================================
elif modulo == "2. Razones Financieras":
    st.header("Análisis de Ratios")
    ac = st.number_input("Activo Circulante", 10000.0)
    pc = st.number_input("Pasivo Circulante", 5000.0)
    if pc > 0:
        st.metric("Razón Circulante", f"{ac/pc:.2f}")

# ==========================================
#        3. EVALUACIÓN DE PROYECTOS (ACTUALIZADO)
# ==========================================
elif modulo == "3. Evaluación de Proyectos":
    st.header("🚀 Evaluación Financiera de Inversiones")
    
    tipo_eval = st.radio("Seleccione el Tipo de Análisis:", 
                         ["Proyecto Nuevo (Simple)", "Análisis de Reemplazo (Avanzado)"], 
                         horizontal=True)
    
    st.markdown("---")

    # ---------------------------------------
    # MODO 1: PROYECTO SIMPLE (VAN/TIR Básico)
    # ---------------------------------------
    if tipo_eval == "Proyecto Nuevo (Simple)":
        c1, c2 = st.columns(2)
        inv = c1.number_input("Inversión Inicial", value=-100000.0, step=1000.0)
        tasa = c2.number_input("Tasa de Descuento (%)", value=12.0) / 100
        anios = st.slider("Años", 1, 10, 5)
        
        flujos = []
        cols = st.columns(anios)
        for i in range(anios):
            flujos.append(cols[i].number_input(f"Año {i+1}", value=30000.0, key=f"s_{i}"))
            
        if st.button("Calcular Indicadores"):
            fc = [inv] + flujos
            van = npf.npv(tasa, fc)
            tir = npf.irr(fc) * 100
            st.metric("VAN", f"${van:,.2f}")
            st.metric("TIR", f"{tir:.2f}%")

    # ---------------------------------------
    # MODO 2: ANÁLISIS DE REEMPLAZO (EL DEL EXCEL)
    # ---------------------------------------
    else:
        st.subheader("🏭 Análisis de Reemplazo de Activo")
        st.markdown("Calcula flujos incrementales, depreciación y recuperación exacta.")

        # --- SECCIÓN A: DATOS DE LOS ACTIVOS ---
        col1, col2 = st.columns(2)
        
        # ACTIVO VIEJO
        with col1:
            st.markdown("### 📉 Activo Actual (Viejo)")
            v_costo = st.number_input("Costo Original", value=2600000.0)
            v_vida = st.number_input("Vida Útil Total (Años)", value=10)
            v_edad = st.number_input("Años ya depreciados", value=5)
            v_desecho = st.number_input("Valor de Desecho (Libros)", value=200000.0)
            st.markdown("---")
            v_venta_hoy = st.number_input("Valor de Venta HOY (Mercado)", value=1000000.0, help="En cuánto puedes vender la máquina vieja hoy")
        
        # ACTIVO NUEVO
        with col2:
            st.markdown("### 📈 Activo Nuevo (Propuesto)")
            n_costo = st.number_input("Costo del Activo Nuevo", value=3100000.0)
            n_install = st.number_input("Gastos de Instalación", value=200000.0)
            n_vida = st.number_input("Vida Útil (Años)", value=5)
            n_desecho = st.number_input("Valor de Desecho (Final)", value=300000.0)
            
        st.markdown("---")
        
        # --- SECCIÓN B: DATOS FINANCIEROS Y OPERATIVOS ---
        st.markdown("### 💰 Datos Operativos y Financieros")
        c1, c2, c3 = st.columns(3)
        tax_rate = c1.number_input("Tasa de Impuestos (%)", value=30.0) / 100
        wacc = c2.number_input("Costo de Capital (WACC/TREMA) %", value=20.0) / 100
        horizonte = c3.number_input("Horizonte de Evaluación (Años)", value=5, min_value=1, max_value=10)

        st.info("Ingresa los incrementos en Ventas y Costos (Diferencia entre Nuevo y Viejo)")
        
        # Tabla editable para flujos anuales
        default_data = {
            "Año": [i+1 for i in range(horizonte)],
            "Inc. Ventas": [1000000.0 if i < 2 else 900000.0 for i in range(horizonte)],
            "Inc. Costos (Ahorros)": [140000.0 if i < 3 else 100000.0 for i in range(horizonte)]
        }
        df_inputs = pd.DataFrame(default_data)
        edited_df = st.data_editor(df_inputs, hide_index=True, num_rows="fixed")
        
        # --- CÁLCULOS ---
        if st.button("CALCULAR REEMPLAZO"):
            st.write("---")
            
            # 1. CÁLCULO DE DEPRECIACIONES
            # Viejo
            dep_anual_viejo = (v_costo - v_desecho) / v_vida
            dep_acum_viejo = dep_anual_viejo * v_edad
            valor_libros_viejo = v_costo - dep_acum_viejo
            
            # Nuevo (Base depreciable incluye instalación usualmente)
            base_dep_nueva = n_costo + n_install
            dep_anual_nueva = (base_dep_nueva - n_desecho) / n_vida
            
            diff_dep = dep_anual_nueva - dep_anual_viejo
            
            # 2. CÁLCULO DE INVERSIÓN INICIAL NETA
            # Venta Viejo vs Libros
            ganancia_venta = v_venta_hoy - valor_libros_viejo
            efecto_fiscal = ganancia_venta * tax_rate # Si es pérdida (negativo), es ahorro fiscal
            
            # Inversión Inicial = (Costo Nuevo + Instalación) - (Venta Viejo) + (Impuesto pagado o - Ahorro)
            # NOTA: En tu Excel a veces ignoran la instalación en el flujo de caja inicial, pero lo correcto es incluirla.
            # Aquí la incluimos para ser exactos.
            inv_inicial = (n_costo + n_install) - v_venta_hoy + efecto_fiscal
            
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.markdown("#### 1. Análisis de Inversión Inicial")
                st.write(f"Valor Libros Activo Viejo: **${valor_libros_viejo:,.2f}**")
                st.write(f"Ganancia/Pérdida en Venta: **${ganancia_venta:,.2f}**")
                st.write(f"Efecto Fiscal (Impuesto/Ahorro): **${efecto_fiscal:,.2f}**")
                st.markdown(f"<div class='metric-card'><h3>${inv_inicial:,.2f}</h3><p>Inversión Inicial Neta</p></div>", unsafe_allow_html=True)

            with col_res2:
                st.markdown("#### 2. Análisis de Depreciación")
                st.write(f"Depreciación Anual Nueva: **${dep_anual_nueva:,.2f}**")
                st.write(f"Depreciación Anual Vieja: **${dep_anual_viejo:,.2f}**")
                st.success(f"Beneficio Fiscal por Depreciación Extra: **${diff_dep:,.2f}/año**")

            # 3. CONSTRUCCIÓN DE FLUJOS DE EFECTIVO
            flujos_netos = []
            tabla_resultados = []
            
            for index, row in edited_df.iterrows():
                inc_ventas = row["Inc. Ventas"]
                inc_costos = row["Inc. Costos (Ahorros)"]
                
                # UAI (Utilidad Antes de Impuestos)
                # Formula: (Ventas - Costos) - Diferencia Depreciación
                uai = (inc_ventas - inc_costos) - diff_dep # Ojo: en tu excel restan costos. Si son ahorros, suman. Asumimos son Costos Operativos del nuevo.
                # Si el input es "Ahorro", debería sumar. Asumiremos estructura del excel: Ventas - Costos.
                
                impuestos = uai * tax_rate
                udi = uai - impuestos # Utilidad Despues Impuestos
                flujo_op = udi + diff_dep # Sumamos depreciación de nuevo
                
                # Ajuste del último año (Valor de Desecho del Nuevo)
                es_ultimo = (index == len(edited_df) - 1)
                if es_ultimo:
                    flujo_final = flujo_op + n_desecho
                else:
                    flujo_final = flujo_op
                
                flujos_netos.append(flujo_final)
                
                tabla_resultados.append({
                    "Año": row["Año"],
                    "UAI": uai,
                    "Impuestos": impuestos,
                    "UDI": udi,
                    "Flujo Operativo": flujo_op,
                    "Flujo Total": flujo_final
                })

            st.markdown("#### 3. Tabla de Flujos de Efectivo")
            st.dataframe(pd.DataFrame(tabla_resultados).style.format("${:,.2f}"))

            # 4. INDICADORES (VAN, TIR, PAYBACK)
            flujos_caja_total = [-inv_inicial] + flujos_netos
            
            van = npf.npv(wacc, flujos_caja_total)
            tir = npf.irr(flujos_caja_total) * 100
            
            # Cálculo de Payback Exacto (Años, Meses, Días)
            acumulado = -inv_inicial
            payback_str = "No recupera"
            
            for i, f in enumerate(flujos_netos):
                prev_acumulado = acumulado
                acumulado += f
                if acumulado >= 0:
                    # Se recuperó en este año "i+1"
                    # Fracción pendiente / Flujo del año
                    pendiente = abs(prev_acumulado)
                    fraccion_anio = pendiente / f
                    
                    meses_total = fraccion_anio * 12
                    meses = int(meses_total)
                    dias = (meses_total - meses) * 30
                    
                    payback_str = f"{i} Años, {meses} Meses, {int(dias)} Días"
                    break
            
            st.markdown("#### 4. Resultados Finales")
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"<div class='metric-card'><h3>${van:,.2f}</h3><p>Valor Actual Neto (VAN)</p></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><h3>{tir:.2f}%</h3><p>Tasa Interna de Retorno (TIR)</p></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='metric-card'><h3>{payback_str}</h3><p>Periodo de Recuperación</p></div>", unsafe_allow_html=True)