import streamlit as st
import pandas as pd
import numpy_financial as npf
import math

# --- CONFIGURACIÓN GLOBAL ---
st.set_page_config(page_title="Sistema de Gestión Financiera", layout="wide")

# --- ESTILOS CSS CORPORATIVOS ---
st.markdown("""
    <style>
    /* Fondo y fuentes */
    .main { background-color: #f4f6f9; }
    h1, h2, h3 { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #2c3e50; }
    h1 { font-size: 2.2rem; border-bottom: 2px solid #2c3e50; padding-bottom: 15px; }
    
    /* Tarjetas de Métricas */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        border-left: 5px solid #2c3e50; /* Azul oscuro corporativo */
        padding: 20px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-card h3 { color: #2c3e50; font-size: 24px; margin: 0; font-weight: 700; }
    .metric-card p { color: #7f8c8d; font-size: 13px; margin-top: 5px; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* Botones */
    .stButton>button {
        background-color: #34495e;
        color: white;
        border-radius: 4px;
        border: none;
        height: 3em;
        font-weight: 600;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #2c3e50; }
    
    /* Tablas */
    .stDataFrame { border: 1px solid #ddd; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

st.title("Sistema Integral de Presupuestos y Finanzas Alvarez Olvera Erick 6NM62")

# --- MENÚ LATERAL ---
st.sidebar.header("Navegación")
modulo = st.sidebar.radio("Seleccione Módulo:", [
    "Inicio",
    "1. Presupuestos Operativos",
    "2. Análisis Financiero (Razones)",
    "3. Evaluación de Inversión"
])
st.sidebar.markdown("---")
st.sidebar.info("Versión Profesional 2.0")

# ==============================================================================
#        MÓDULO 0: INICIO
# ==============================================================================
if modulo == "Inicio":
    st.markdown("#### Panel de Control Principal")
    st.write("Bienvenido al sistema. Seleccione una opción del menú lateral para proceder.")
    
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='metric-card'><h3>Módulo 1</h3><p>Presupuestos Maestros</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='metric-card'><h3>Módulo 2</h3><p>Ratios Financieros</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='metric-card'><h3>Módulo 3</h3><p>Evaluación de Proyectos</p></div>", unsafe_allow_html=True)

# ==============================================================================
#        MÓDULO 1: PRESUPUESTOS (COMPLETO)
# ==============================================================================
elif modulo == "1. Presupuestos Operativos":
    st.header("Generador de Presupuestos")
    tabs = st.tabs(["1. Ventas", "2. Producción", "3. Materiales", "4. Mano de Obra", "5. Costo Unitario"])
    
    # --- 1. VENTAS ---
    with tabs[0]:
        st.subheader("Presupuesto de Ventas")
        c1, c2 = st.columns(2)
        unidades = c1.number_input("Unidades a vender", 0, 1000000, 1000, key="pv_uni")
        precio = c2.number_input("Precio Unitario ($)", 0.0, 100000.0, 50.0, key="pv_precio")
        
        ingreso = unidades * precio
        st.session_state['pres_uni'] = unidades  # Guardar para otros tabs
        
        st.markdown(f"<div class='metric-card'><h3>${ingreso:,.2f}</h3><p>Ingresos Totales Presupuestados</p></div>", unsafe_allow_html=True)

    # --- 2. PRODUCCIÓN ---
    with tabs[1]:
        st.subheader("Presupuesto de Producción")
        col1, col2, col3 = st.columns(3)
        v_est = col1.number_input("Ventas Estimadas", value=st.session_state.get('pres_uni', 1000), key="pp_ventas")
        if_des = col2.number_input("Inventario Final Deseado", value=200, key="pp_if")
        ii_est = col3.number_input("Inventario Inicial", value=100, key="pp_ii")
        
        prod_req = v_est + if_des - ii_est
        st.session_state['pres_prod'] = prod_req
        
        if st.button("Calcular Producción"):
            st.markdown(f"<div class='metric-card'><h3>{prod_req:,.0f}</h3><p>Unidades a Producir</p></div>", unsafe_allow_html=True)

    # --- 3. MATERIALES ---
    with tabs[2]:
        st.subheader("Presupuesto de Materiales")
        st.write("Requerimiento de Materia Prima y Compras")
        
        c1, c2 = st.columns(2)
        prod = c1.number_input("Producción Requerida", value=st.session_state.get('pres_prod', 1100), key="pm_prod")
        std_mat = c2.number_input("Estándar Material por Unidad", value=1.5, key="pm_std")
        
        req_total = prod * std_mat
        st.info(f"Requerimiento Total para Producción: {req_total:,.2f} unidades de material")
        
        st.markdown("---")
        st.write("**Presupuesto de Compras**")
        k1, k2, k3 = st.columns(3)
        if_mat = k1.number_input("Inv. Final Materiales", value=500.0, key="pm_if")
        ii_mat = k2.number_input("Inv. Inicial Materiales", value=200.0, key="pm_ii")
        costo_mat = k3.number_input("Costo por Unidad de Material ($)", value=10.0, key="pm_costo")
        
        compras_uni = req_total + if_mat - ii_mat
        costo_compras = compras_uni * costo_mat
        
        st.markdown(f"<div class='metric-card'><h3>${costo_compras:,.2f}</h3><p>Presupuesto de Compras</p></div>", unsafe_allow_html=True)

    # --- 4. MANO DE OBRA ---
    with tabs[3]:
        st.subheader("Presupuesto de Mano de Obra Directa (MOD)")
        c1, c2, c3 = st.columns(3)
        mod_prod = c1.number_input("Producción Requerida", value=st.session_state.get('pres_prod', 1100), key="mod_prod")
        hrs_unit = c2.number_input("Horas por unidad", value=2.0, key="mod_hrs")
        cuota_hr = c3.number_input("Cuota por Hora ($)", value=25.0, key="mod_costo")
        
        costo_mod = mod_prod * hrs_unit * cuota_hr
        st.markdown(f"<div class='metric-card'><h3>${costo_mod:,.2f}</h3><p>Costo Total MOD</p></div>", unsafe_allow_html=True)

    # --- 5. COSTO UNITARIO ---
    with tabs[4]:
        st.subheader("Cédula de Costo Unitario")
        c1, c2, c3 = st.columns(3)
        c_mat = c1.number_input("Costo Material Directo (Unitario)", value=15.0, key="cu_mat")
        c_mod = c2.number_input("Costo MOD (Unitario)", value=50.0, key="cu_mod")
        c_gif = c3.number_input("Gastos Ind. Fab. (Unitario)", value=10.0, key="cu_gif")
        
        unitario = c_mat + c_mod + c_gif
        st.markdown(f"<div class='metric-card'><h3>${unitario:,.2f}</h3><p>Costo de Producción Unitario</p></div>", unsafe_allow_html=True)

# ==============================================================================
#        MÓDULO 2: RAZONES FINANCIERAS (COMPLETO)
# ==============================================================================
elif modulo == "2. Análisis Financiero (Razones)":
    st.header("Análisis de Indicadores Financieros")
    tabs = st.tabs(["Liquidez", "Apalancamiento", "Actividad", "Rentabilidad"])
    
    # --- LIQUIDEZ ---
    with tabs[0]:
        st.subheader("Razones de Liquidez")
        ac = st.number_input("Activo Circulante", 15000.0, key="l_ac")
        pc = st.number_input("Pasivo Circulante", 5000.0, key="l_pc")
        inv = st.number_input("Inventarios", 3000.0, key="l_inv")
        
        if pc > 0:
            c1, c2 = st.columns(2)
            c1.markdown(f"<div class='metric-card'><h3>{ac/pc:.2f}</h3><p>Razón Circulante</p></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><h3>{(ac-inv)/pc:.2f}</h3><p>Prueba Ácida</p></div>", unsafe_allow_html=True)

    # --- APALANCAMIENTO ---
    with tabs[1]:
        st.subheader("Estructura de Capital")
        pt = st.number_input("Pasivo Total", 40000.0, key="a_pt")
        at = st.number_input("Activo Total", 100000.0, key="a_at")
        cc = st.number_input("Capital Contable", 60000.0, key="a_cc")
        
        if at > 0 and cc > 0:
            st.markdown(f"**Endeudamiento (Pasivo/Activo):** {pt/at*100:.2f}%")
            st.markdown(f"**Apalancamiento (Pasivo/Capital):** {pt/cc:.2f}")

    # --- ACTIVIDAD ---
    with tabs[2]:
        st.subheader("Eficiencia Operativa")
        cv = st.number_input("Costo de Ventas", 50000.0, key="act_cv")
        inv_prom = st.number_input("Inventario Promedio", 5000.0, key="act_inv")
        ventas_cred = st.number_input("Ventas a Crédito", 80000.0, key="act_vc")
        cxc_prom = st.number_input("Promedio Cuentas por Cobrar", 8000.0, key="act_cxc")
        
        c1, c2 = st.columns(2)
        if inv_prom > 0:
            c1.metric("Rotación Inventarios", f"{cv/inv_prom:.2f} veces")
        if cxc_prom > 0:
            c2.metric("Rotación CxC", f"{ventas_cred/cxc_prom:.2f} veces")

    # --- RENTABILIDAD ---
    with tabs[3]:
        st.subheader("Márgenes de Rentabilidad")
        un = st.number_input("Utilidad Neta", 15000.0, key="r_un")
        vn = st.number_input("Ventas Netas", 100000.0, key="r_vn")
        at_r = st.number_input("Activo Total", 200000.0, key="r_at")
        
        if vn > 0 and at_r > 0:
            c1, c2 = st.columns(2)
            c1.markdown(f"<div class='metric-card'><h3>{un/vn*100:.2f}%</h3><p>Margen Neto</p></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><h3>{un/at_r*100:.2f}%</h3><p>ROA (Retorno sobre Activos)</p></div>", unsafe_allow_html=True)

# ==============================================================================
#        MÓDULO 3: EVALUACIÓN DE PROYECTOS (AVANZADO/SIMPLE)
# ==============================================================================
elif modulo == "3. Evaluación de Inversión":
    st.header("Evaluación Financiera de Proyectos")
    
    # Selector de Modo
    modo = st.radio("Tipo de Evaluación:", ["Proyecto Nuevo (Estándar)", "Reemplazo de Activos (Avanzado)"], horizontal=True)
    st.markdown("---")

    # ------------------------------------------------------------------
    # OPCIÓN A: PROYECTO ESTÁNDAR (VAN/TIR SIMPLE)
    # ------------------------------------------------------------------
    if modo == "Proyecto Nuevo (Estándar)":
        c1, c2 = st.columns(2)
        inv = c1.number_input("Inversión Inicial (Negativo)", value=-100000.0, step=1000.0)
        tasa = c2.number_input("Tasa de Descuento (%)", value=10.0) / 100
        n = st.slider("Años", 1, 10, 5)
        
        flujos = []
        cols = st.columns(n)
        for i in range(n):
            flujos.append(cols[i].number_input(f"Flujo {i+1}", 10000.0, key=f"simp_{i}"))
            
        if st.button("Calcular Indicadores Básicos"):
            fc = [inv] + flujos
            van = npf.npv(tasa, fc)
            tir = npf.irr(fc) * 100
            st.markdown(f"<div class='metric-card'><h3>${van:,.2f}</h3><p>Valor Actual Neto (VAN)</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-card'><h3>{tir:.2f}%</h3><p>Tasa Interna de Retorno (TIR)</p></div>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # OPCIÓN B: REEMPLAZO DE ACTIVOS (LÓGICA DEL EXCEL)
    # ------------------------------------------------------------------
    else:
        st.subheader("Análisis de Reemplazo (Flujos Incrementales)")
        
        # 1. DATOS DE ENTRADA
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Activo Actual (Viejo)")
            v_costo = st.number_input("Costo Original", value=2600000.0)
            v_vida = st.number_input("Vida Útil Total", value=10)
            v_edad = st.number_input("Años Depreciados", value=5)
            v_desecho_libros = st.number_input("Valor Desecho (Libros)", value=200000.0)
            st.markdown("---")
            v_venta_hoy = st.number_input("Precio Venta Hoy (Mercado)", value=1000000.0)

        with col2:
            st.markdown("##### Activo Nuevo (Propuesto)")
            n_costo = st.number_input("Costo Activo Nuevo", value=3100000.0)
            n_instalacion = st.number_input("Gastos Instalación", value=200000.0)
            n_vida = st.number_input("Vida Útil Nuevo", value=5)
            n_desecho_final = st.number_input("Valor Desecho Final", value=300000.0)

        st.markdown("##### Parámetros Financieros")
        c1, c2, c3 = st.columns(3)
        tax = c1.number_input("Tasa Impuestos (%)", value=30.0) / 100
        wacc = c2.number_input("WACC / Tasa Descuento (%)", value=20.0) / 100
        anios_eval = c3.number_input("Horizonte Evaluación", value=5, min_value=1)

        st.write("Ingrese los **incrementos** anuales (Diferencia Nuevo vs Viejo):")
        # Tabla editable
        data_default = {
            "Año": list(range(1, int(anios_eval)+1)),
            "Inc. Ventas": [1000000.0]*2 + [900000.0]*(int(anios_eval)-2),
            "Ahorro Costos": [140000.0]*3 + [100000.0]*(int(anios_eval)-3)
        }
        df_edit = st.data_editor(pd.DataFrame(data_default), hide_index=True)

        if st.button("Ejecutar Análisis Completo"):
            st.markdown("---")
            
            # A. CÁLCULO DE INVERSIÓN INICIAL NETA
            # 1. Valor en libros actual
            dep_anual_v = (v_costo - v_desecho_libros) / v_vida
            dep_acum_v = dep_anual_v * v_edad
            vl_viejo = v_costo - dep_acum_v
            
            # 2. Efecto Fiscal Venta
            utilidad_venta = v_venta_hoy - vl_viejo
            impuesto_venta = utilidad_venta * tax # Si es negativo, es ahorro
            
            # 3. Inversión Neta
            inv_total_nueva = n_costo + n_instalacion
            inv_neta = inv_total_nueva - v_venta_hoy + impuesto_venta
            
            c1, c2 = st.columns(2)
            c1.markdown(f"""
            <div class='metric-card'>
                <h3>${inv_neta:,.2f}</h3>
                <p>Inversión Inicial Neta</p>
                <small>Costo Nuevo + Inst - Venta Viejo + Efecto Fiscal</small>
            </div>""", unsafe_allow_html=True)
            
            # B. CÁLCULO DE FLUJOS OPERATIVOS
            base_dep_n = n_costo + n_instalacion
            dep_anual_n = (base_dep_n - n_desecho_final) / n_vida
            dif_depreciacion = dep_anual_n - dep_anual_v
            
            c2.markdown(f"""
            <div class='metric-card'>
                <h3>${dif_depreciacion:,.2f}</h3>
                <p>Diferencia de Depreciación</p>
                <small>Beneficio fiscal anual</small>
            </div>""", unsafe_allow_html=True)

            flujos_netos = []
            
            for idx, row in df_edit.iterrows():
                inc_ventas = row["Inc. Ventas"]
                ahorro_costos = row["Ahorro Costos"]
                
                # UAI = (Ventas + Ahorros) - Diferencia Depreciación
                # Nota: En tu excel restaban costos, aquí asumimos ahorros positivos suman a la utilidad
                uai = (inc_ventas + ahorro_costos) - dif_depreciacion
                
                impuestos = uai * tax
                udi = uai - impuestos
                flujo = udi + dif_depreciacion
                
                # Sumar valor desecho en ultimo año
                if idx == len(df_edit) - 1:
                    flujo += n_desecho_final
                
                flujos_netos.append(flujo)
            
            # C. RESULTADOS FINALES (VAN, TIR, PAYBACK EXACTO)
            flujos_totales = [-inv_neta] + flujos_netos
            van = npf.npv(wacc, flujos_totales)
            try:
                tir = npf.irr(flujos_totales) * 100
            except:
                tir = 0.0
            
            # Payback (Años, Meses, Días)
            saldo = -inv_neta
            payback_texto = "No recupera"
            
            for i, f in enumerate(flujos_netos):
                saldo_anterior = saldo
                saldo += f
                if saldo >= 0:
                    # Recuperó en el año i+1
                    pendiente = abs(saldo_anterior)
                    fraccion = pendiente / f
                    
                    meses_float = fraccion * 12
                    meses = int(meses_float)
                    dias = (meses_float - meses) * 30
                    
                    payback_texto = f"{i} Años, {meses} Meses, {int(dias)} Días"
                    break
            
            # Mostrar tabla y métricas
            st.write("**Tabla de Flujos de Efectivo**")
            df_res = pd.DataFrame({"Año": df_edit["Año"], "Flujo Neto": flujos_netos})
            st.dataframe(df_res.style.format({"Flujo Neto": "${:,.2f}"}))
            
            k1, k2, k3 = st.columns(3)
            k1.markdown(f"<div class='metric-card'><h3>${van:,.2f}</h3><p>VAN</p></div>", unsafe_allow_html=True)
            k2.markdown(f"<div class='metric-card'><h3>{tir:.2f}%</h3><p>TIR</p></div>", unsafe_allow_html=True)
            k3.markdown(f"<div class='metric-card'><h3>{payback_texto}</h3><p>Periodo de Recuperación</p></div>", unsafe_allow_html=True)