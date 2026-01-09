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
    
    /* Cajas de alerta estilo profesional */
    .stAlert { background-color: #ffffff; border: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

st.title("Sistema Integral de Presupuestos y Finanzas - 6NM62")

# --- MENÚ LATERAL ---
st.sidebar.header("Navegación")
modulo = st.sidebar.radio("Seleccione Módulo:", [
    "Inicio",
    "1. Presupuestos Operativos",
    "2. Análisis Financiero (Razones)",
    "3. Evaluación de Inversión"
])
st.sidebar.markdown("---")
st.sidebar.info("Versión Profesional Final")

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
#        MÓDULO 1: PRESUPUESTOS (COMPLETO E INTEGRADO)
# ==============================================================================
elif modulo == "1. Presupuestos Operativos":
    st.header("Generador de Presupuestos")
    
    # Configuración de Valuación
    with st.expander("Configuración de Inventarios", expanded=False):
        st.session_state['metodo_valuacion'] = st.radio(
            "Método de Valuación:", ['UEPS', 'PEPS', 'Promedio Ponderado'], horizontal=True
        )

    tabs = st.tabs([
        "1. Ventas", "2. Producción", "3. Materiales", "4. Mano de Obra", 
        "5. GIF", "6. Costo Prod.", "7. Costo Ventas", "8. Estado Resultados"
    ])
    
    # --- 1. VENTAS ---
    with tabs[0]:
        st.subheader("Presupuesto de Ventas")
        c1, c2 = st.columns(2)
        unidades = c1.number_input("Unidades a vender", 0, 1000000, 0, key="pv_uni")
        precio = c2.number_input("Precio Unitario ($)", 0.0, 100000.0, 0.0, key="pv_precio")
        
        ingreso = unidades * precio
        st.session_state['pres_uni'] = unidades
        st.session_state['pres_ingreso'] = ingreso
        st.session_state['pres_precio'] = precio
        
        st.markdown(f"<div class='metric-card'><h3>${ingreso:,.2f}</h3><p>Ingresos Totales Presupuestados</p></div>", unsafe_allow_html=True)

    # --- 2. PRODUCCIÓN ---
    with tabs[1]:
        st.subheader("Presupuesto de Producción")
        col1, col2, col3 = st.columns(3)
        v_est = col1.number_input("Ventas Estimadas", value=st.session_state.get('pres_uni', 0), key="pp_ventas")
        if_des = col2.number_input("Inventario Final Deseado", value=0, key="pp_if")
        ii_est = col3.number_input("Inventario Inicial", value=0, key="pp_ii")
        
        prod_req = v_est + if_des - ii_est
        st.session_state['pres_prod'] = prod_req
        st.session_state['pp_if'] = if_des 
        st.session_state['pp_ii'] = ii_est
        
        st.markdown(f"<div class='metric-card'><h3>{prod_req:,.0f}</h3><p>Unidades a Producir</p></div>", unsafe_allow_html=True)

    # --- 3. MATERIALES ---
    with tabs[2]:
        st.subheader("Presupuesto de Materiales")
        
        c1, c2 = st.columns(2)
        prod = c1.number_input("Producción Requerida", value=st.session_state.get('pres_prod', 0), key="pm_prod")
        std_mat = c2.number_input("Estándar Material por Unidad", value=0.0, key="pm_std")
        
        req_total = prod * std_mat
        st.info(f"Requerimiento Total: {req_total:,.2f} unidades de material")
        
        st.markdown("---")
        st.write("**Presupuesto de Compras**")
        k1, k2, k3 = st.columns(3)
        if_mat = k1.number_input("Inv. Final Materiales", value=0.0, key="pm_if")
        ii_mat = k2.number_input("Inv. Inicial Materiales", value=0.0, key="pm_ii")
        costo_mat = k3.number_input("Costo por Unidad de Material ($)", value=0.0, key="pm_costo")
        
        compras_uni = req_total + if_mat - ii_mat
        costo_compras = compras_uni * costo_mat
        
        # Guardar costo total de materiales para costo de producción (Simplificado: Consumo * Costo)
        # Para ser más exactos usamos la valuación, pero aquí usaremos el costo de reposición para el ejemplo simple
        st.session_state['costo_mat_total'] = req_total * costo_mat 

        st.markdown(f"<div class='metric-card'><h3>${costo_compras:,.2f}</h3><p>Presupuesto de Compras</p></div>", unsafe_allow_html=True)

    # --- 4. MANO DE OBRA ---
    with tabs[3]:
        st.subheader("Presupuesto de Mano de Obra Directa (MOD)")
        c1, c2, c3 = st.columns(3)
        mod_prod = c1.number_input("Producción Requerida", value=st.session_state.get('pres_prod', 0), key="mod_prod")
        hrs_unit = c2.number_input("Horas por unidad", value=0.0, key="mod_hrs")
        cuota_hr = c3.number_input("Cuota por Hora ($)", value=0.0, key="mod_costo")
        
        costo_mod = mod_prod * hrs_unit * cuota_hr
        st.session_state['costo_mod_total'] = costo_mod
        
        st.markdown(f"<div class='metric-card'><h3>${costo_mod:,.2f}</h3><p>Costo Total MOD</p></div>", unsafe_allow_html=True)

    # --- 5. GIF ---
    with tabs[4]:
        st.subheader("Gastos Indirectos de Fabricación (GIF)")
        c1, c2 = st.columns(2)
        with c1:
            g1 = st.number_input("Material Indirecto", 0.0)
            g2 = st.number_input("Mano Obra Ind.", 0.0)
            g3 = st.number_input("Renta Fabrica", 0.0)
        with c2:
            g4 = st.number_input("Energía", 0.0)
            g5 = st.number_input("Mantenimiento", 0.0)
            g6 = st.number_input("Varios", 0.0)
        
        total_gif = g1 + g2 + g3 + g4 + g5 + g6
        st.session_state['costo_gif_total'] = total_gif
        st.markdown(f"<div class='metric-card'><h3>${total_gif:,.2f}</h3><p>Total GIF</p></div>", unsafe_allow_html=True)

    # --- 6. COSTO UNITARIO ---
    with tabs[5]:
        st.subheader("Cédula de Costo de Producción")
        # Recuperamos totales
        mat = st.session_state.get('costo_mat_total', 0)
        mod = st.session_state.get('costo_mod_total', 0)
        gif = st.session_state.get('costo_gif_total', 0)
        prod_units = st.session_state.get('pres_prod', 1)
        
        costo_total_prod = mat + mod + gif
        costo_unitario = costo_total_prod / prod_units if prod_units > 0 else 0
        st.session_state['costo_unitario_calc'] = costo_unitario
        
        c1, c2 = st.columns(2)
        c1.markdown(f"<div class='metric-card'><h3>${costo_total_prod:,.2f}</h3><p>Costo Total Producción</p></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><h3>${costo_unitario:,.2f}</h3><p>Costo Unitario</p></div>", unsafe_allow_html=True)

    # --- 7. COSTO DE VENTAS ---
    with tabs[6]:
        st.subheader("Presupuesto de Costo de Ventas")
        metodo = st.session_state.get('metodo_valuacion', 'UEPS')
        st.info(f"Método aplicado: {metodo}")
        
        c1, c2 = st.columns(2)
        ii_pt_units = st.number_input("Inv. Inicial PT (unidades)", value=0, key="cv_ii_u")
        ii_pt_cost = st.number_input("Costo Unitario Inv. Inicial", value=0.0, key="cv_ii_c")
        
        ventas_units = st.session_state.get('pres_uni', 0)
        prod_units = st.session_state.get('pres_prod', 0)
        costo_prod = st.session_state.get('costo_unitario_calc', 0)
        
        costo_ventas = 0.0
        
        if ventas_units > 0:
            if metodo == 'UEPS':
                if ventas_units <= prod_units:
                    costo_ventas = ventas_units * costo_prod
                else:
                    costo_ventas = (prod_units * costo_prod) + ((ventas_units - prod_units) * ii_pt_cost)
            elif metodo == 'PEPS':
                if ventas_units <= ii_pt_units:
                    costo_ventas = ventas_units * ii_pt_cost
                else:
                    costo_ventas = (ii_pt_units * ii_pt_cost) + ((ventas_units - ii_pt_units) * costo_prod)
            else: # Promedio
                total_val = (ii_pt_units * ii_pt_cost) + (prod_units * costo_prod)
                total_uni = ii_pt_units + prod_units
                promedio = total_val / total_uni if total_uni > 0 else 0
                costo_ventas = ventas_units * promedio
                
        st.session_state['costo_ventas_calc'] = costo_ventas
        st.markdown(f"<div class='metric-card'><h3>${costo_ventas:,.2f}</h3><p>Costo de Ventas</p></div>", unsafe_allow_html=True)

    # --- 8. ESTADO DE RESULTADOS ---
    with tabs[7]:
        st.subheader("Estado de Resultados Proforma")
        go = st.number_input("Gastos Operativos (Venta y Admin)", value=0.0)
        
        ingresos = st.session_state.get('pres_ingreso', 0)
        cv = st.session_state.get('costo_ventas_calc', 0)
        
        utilidad_bruta = ingresos - cv
        utilidad_operativa = utilidad_bruta - go
        
        st.markdown("---")
        k1, k2, k3 = st.columns(3)
        k1.markdown(f"<div class='metric-card'><h3>${ingresos:,.2f}</h3><p>Ventas</p></div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='metric-card'><h3>${utilidad_bruta:,.2f}</h3><p>Utilidad Bruta</p></div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='metric-card'><h3>${utilidad_operativa:,.2f}</h3><p>Utilidad Operativa</p></div>", unsafe_allow_html=True)


# ==============================================================================
#        MÓDULO 2: RAZONES FINANCIERAS
# ==============================================================================
elif modulo == "2. Análisis Financiero (Razones)":
    st.header("Análisis de Indicadores Financieros")
    tabs = st.tabs(["Liquidez", "Apalancamiento", "Actividad", "Rentabilidad"])
    
    # --- LIQUIDEZ ---
    with tabs[0]:
        st.subheader("Razones de Liquidez")
        ac = st.number_input("Activo Circulante", 0.0, key="l_ac")
        pc = st.number_input("Pasivo Circulante", 0.0, key="l_pc")
        inv = st.number_input("Inventarios", 0.0, key="l_inv")
        
        if pc > 0:
            c1, c2 = st.columns(2)
            c1.markdown(f"<div class='metric-card'><h3>{ac/pc:.2f}</h3><p>Razón Circulante</p></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><h3>{(ac-inv)/pc:.2f}</h3><p>Prueba Ácida</p></div>", unsafe_allow_html=True)

    # --- APALANCAMIENTO ---
    with tabs[1]:
        st.subheader("Estructura de Capital")
        pt = st.number_input("Pasivo Total", 0.0, key="a_pt")
        at = st.number_input("Activo Total", 0.0, key="a_at")
        cc = st.number_input("Capital Contable", 0.0, key="a_cc")
        
        if at > 0 and cc > 0:
            st.markdown(f"**Endeudamiento:** {pt/at*100:.2f}%")
            st.markdown(f"**Apalancamiento:** {pt/cc:.2f}")

    # --- ACTIVIDAD ---
    with tabs[2]:
        st.subheader("Eficiencia Operativa")
        cv = st.number_input("Costo de Ventas", 0.0, key="act_cv")
        inv_prom = st.number_input("Inventario Promedio", 0.0, key="act_inv")
        
        if inv_prom > 0:
            st.metric("Rotación Inventarios", f"{cv/inv_prom:.2f} veces")

    # --- RENTABILIDAD ---
    with tabs[3]:
        st.subheader("Márgenes de Rentabilidad")
        un = st.number_input("Utilidad Neta", 0.0, key="r_un")
        vn = st.number_input("Ventas Netas", 0.0, key="r_vn")
        at_r = st.number_input("Activo Total", 0.0, key="r_at")
        
        if vn > 0 and at_r > 0:
            c1, c2 = st.columns(2)
            c1.markdown(f"<div class='metric-card'><h3>{un/vn*100:.2f}%</h3><p>Margen Neto</p></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><h3>{un/at_r*100:.2f}%</h3><p>ROA</p></div>", unsafe_allow_html=True)

# ==============================================================================
#        MÓDULO 3: EVALUACIÓN DE PROYECTOS
# ==============================================================================
elif modulo == "3. Evaluación de Inversión":
    st.header("Evaluación Financiera de Proyectos")
    
    # Selector de Modo
    modo = st.radio("Tipo de Evaluación:", ["Proyecto Nuevo (Estándar)", "Reemplazo de Activos (Avanzado)"], horizontal=True)
    st.markdown("---")

    # ------------------------------------------------------------------
    # OPCIÓN A: PROYECTO ESTÁNDAR
    # ------------------------------------------------------------------
    if modo == "Proyecto Nuevo (Estándar)":
        c1, c2 = st.columns(2)
        inv = c1.number_input("Inversión Inicial (Negativo)", value=0.0, step=1000.0)
        tasa = c2.number_input("Tasa de Descuento (%)", value=0.0) / 100
        n = st.slider("Años", 1, 10, 5)
        
        flujos = []
        cols = st.columns(n)
        for i in range(n):
            flujos.append(cols[i].number_input(f"Flujo {i+1}", 0.0, key=f"simp_{i}"))
            
        if st.button("Calcular Indicadores Básicos"):
            fc = [inv] + flujos
            # Manejo de error si los flujos son todos 0
            try:
                van = npf.npv(tasa, fc)
                tir = npf.irr(fc) * 100
                if math.isnan(tir): tir = 0.0
            except:
                van = 0.0
                tir = 0.0

            st.markdown(f"<div class='metric-card'><h3>${van:,.2f}</h3><p>Valor Actual Neto (VAN)</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-card'><h3>{tir:.2f}%</h3><p>Tasa Interna de Retorno (TIR)</p></div>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # OPCIÓN B: REEMPLAZO DE ACTIVOS (LÓGICA EXCEL)
    # ------------------------------------------------------------------
    else:
        st.subheader("Análisis de Reemplazo (Flujos Incrementales)")
        
        # 1. DATOS DE ENTRADA
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Activo Actual (Viejo)")
            v_costo = st.number_input("Costo Original", value=0.0)
            v_vida = st.number_input("Vida Útil Total", value=0)
            v_edad = st.number_input("Años Depreciados", value=0)
            v_desecho_libros = st.number_input("Valor Desecho (Libros)", value=0.0)
            st.markdown("---")
            v_venta_hoy = st.number_input("Precio Venta Hoy (Mercado)", value=0.0)

        with col2:
            st.markdown("##### Activo Nuevo (Propuesto)")
            n_costo = st.number_input("Costo Activo Nuevo", value=0.0)
            n_instalacion = st.number_input("Gastos Instalación", value=0.0)
            n_vida = st.number_input("Vida Útil Nuevo", value=5)
            n_desecho_final = st.number_input("Valor Desecho Final", value=0.0)

        st.markdown("##### Parámetros Financieros")
        c1, c2, c3 = st.columns(3)
        tax = c1.number_input("Tasa Impuestos (%)", value=0.0) / 100
        wacc = c2.number_input("WACC / Tasa Descuento (%)", value=0.0) / 100
        anios_eval = c3.number_input("Horizonte Evaluación", value=5, min_value=1)

        st.write("Ingrese los **incrementos** anuales (Diferencia Nuevo vs Viejo):")
        
        # Generar tabla vacía o con 0s
        data_default = {
            "Año": list(range(1, int(anios_eval)+1)),
            "Inc. Ventas": [0.0] * int(anios_eval),
            "Ahorro Costos": [0.0] * int(anios_eval)
        }
        df_edit = st.data_editor(pd.DataFrame(data_default), hide_index=True)

        if st.button("Ejecutar Análisis Completo"):
            st.markdown("---")
            
            # Protección contra división por cero
            if v_vida == 0 or n_vida == 0:
                st.error("La vida útil no puede ser 0.")
            else:
                # A. CÁLCULO DE INVERSIÓN INICIAL NETA
                dep_anual_v = (v_costo - v_desecho_libros) / v_vida
                dep_acum_v = dep_anual_v * v_edad
                vl_viejo = v_costo - dep_acum_v
                
                utilidad_venta = v_venta_hoy - vl_viejo
                impuesto_venta = utilidad_venta * tax
                
                inv_total_nueva = n_costo + n_instalacion
                inv_neta = inv_total_nueva - v_venta_hoy + impuesto_venta
                
                c1, c2 = st.columns(2)
                c1.markdown(f"""
                <div class='metric-card'>
                    <h3>${inv_neta:,.2f}</h3>
                    <p>Inversión Inicial Neta</p>
                </div>""", unsafe_allow_html=True)
                
                # B. CÁLCULO DE FLUJOS OPERATIVOS
                base_dep_n = n_costo + n_instalacion
                dep_anual_n = (base_dep_n - n_desecho_final) / n_vida
                dif_depreciacion = dep_anual_n - dep_anual_v
                
                flujos_netos = []
                
                for idx, row in df_edit.iterrows():
                    inc_ventas = row["Inc. Ventas"]
                    ahorro_costos = row["Ahorro Costos"]
                    
                    uai = (inc_ventas + ahorro_costos) - dif_depreciacion
                    impuestos = uai * tax
                    udi = uai - impuestos
                    flujo = udi + dif_depreciacion
                    
                    if idx == len(df_edit) - 1:
                        flujo += n_desecho_final
                    
                    flujos_netos.append(flujo)
                
                # C. RESULTADOS FINALES
                flujos_totales = [-inv_neta] + flujos_netos
                
                # VAN
                van = npf.npv(wacc, flujos_totales)
                
                # TIR
                try:
                    tir = npf.irr(flujos_totales) * 100
                    if math.isnan(tir): tir = 0.0
                except:
                    tir = 0.0
                
                # PAYBACK
                saldo = -inv_neta
                payback_texto = "No recupera"
                
                for i, f in enumerate(flujos_netos):
                    saldo_anterior = saldo
                    saldo += f
                    if saldo >= 0 and f != 0:
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
                k3.markdown(f"<div class='metric-card'><h3>{payback_texto}</h3><p>Recuperación</p></div>", unsafe_allow_html=True)