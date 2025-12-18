import streamlit as st
import pandas as pd
import numpy_financial as npf

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sistema de Gestión Financiera", layout="wide")

# --- ESTILOS CSS PROFESIONALES (CORPORATE THEME) ---
st.markdown("""
    <style>
    /* Estilo General */
    .main {
        background-color: #f8f9fa; /* Gris muy claro para el fondo */
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2c3e50;
        font-weight: 600;
    }
    h1 { font-size: 2.2rem; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
    h2 { font-size: 1.5rem; margin-top: 20px; color: #34495e; }
    
    /* Estilo de Tarjetas de Métricas */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-left: 5px solid #2980b9; /* Borde lateral azul profesional */
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-card h3 {
        color: #2c3e50 !important;
        font-size: 28px;
        margin: 0;
        font-weight: 700;
    }
    .metric-card p {
        color: #7f8c8d !important;
        font-size: 14px;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Botones */
    .stButton>button {
        background-color: #2980b9; /* Azul Corporativo */
        color: white;
        border-radius: 4px;
        border: none;
        height: 3em;
        font-weight: 500;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1a5276; /* Azul más oscuro al pasar mouse */
    }
    
    /* Formulas */
    .formula {
        background-color: #e8f6f3;
        padding: 10px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        color: #16a085;
        font-size: 0.9rem;
        border: 1px solid #d1f2eb;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Sistema de Gestión Financiera y Presupuestal")

# --- NAVEGACIÓN LATERAL ---
st.sidebar.markdown("### Menú Principal")
modulo = st.sidebar.radio("Seleccione Módulo:", [
    "Inicio", 
    "1. Presupuestos", 
    "2. Razones Financieras", 
    "3. Evaluación de Proyectos"
])
st.sidebar.markdown("---")
st.sidebar.info("Sistema v1.0")

# ==========================================
#        INICIO
# ==========================================
if modulo == "Inicio":
    st.markdown("#### Panel de Control")
    st.write("Bienvenido al sistema. Utilice el menú lateral para acceder a las herramientas de cálculo.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card" style="border-left: 5px solid #27ae60;">
            <h3>Módulo 1</h3>
            <p>Presupuestos Maestros</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card" style="border-left: 5px solid #f39c12;">
            <h3>Módulo 2</h3>
            <p>Análisis Financiero</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card" style="border-left: 5px solid #c0392b;">
            <h3>Módulo 3</h3>
            <p>Evaluación de Inversión</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
#        1. PRESUPUESTOS
# ==========================================
elif modulo == "1. Presupuestos":
    st.header("Generador de Presupuestos")
    
    tabs = st.tabs(["Ventas", "Producción", "Materiales", "Mano de Obra", "Costo Unitario"])
    
    # --- VENTAS ---
    with tabs[0]:
        st.subheader("Presupuesto de Ventas")
        c1, c2 = st.columns(2)
        unidades = c1.number_input("Unidades a vender", 0, 100000, 1000, key="v_uni")
        precio = c2.number_input("Precio Unitario ($)", 0.0, 10000.0, 50.0, key="v_precio")
        
        ingreso_total = unidades * precio
        st.session_state['pres_ventas_unidades'] = unidades
        
        st.markdown(f"""<div class='metric-card'><h3>${ingreso_total:,.2f}</h3><p>Ingresos Totales Estimados</p></div>""", unsafe_allow_html=True)

    # --- PRODUCCIÓN ---
    with tabs[1]:
        st.subheader("Presupuesto de Producción")
        st.markdown("<div class='formula'>Producción = Ventas + Inv. Final - Inv. Inicial</div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        p_ventas = c1.number_input("Ventas Proyectadas", value=st.session_state.get('pres_ventas_unidades', 1000), key="p_ventas")
        inv_fin = c2.number_input("Inventario Final Deseado", value=200, key="p_if")
        inv_ini = c3.number_input("Inventario Inicial", value=100, key="p_ii")
        
        produccion = p_ventas + inv_fin - inv_ini
        st.session_state['pres_prod_unidades'] = produccion
        
        st.write("")
        if st.button("Calcular Producción"):
            st.markdown(f"""<div class='metric-card'><h3>{produccion:,.0f}</h3><p>Unidades a Producir</p></div>""", unsafe_allow_html=True)

    # --- MATERIALES ---
    with tabs[2]:
        st.subheader("Presupuesto de Materiales")
        
        st.markdown("**A. Requerimiento de Materia Prima**")
        colA, colB = st.columns(2)
        prod_req = colA.number_input("Producción Requerida", value=st.session_state.get('pres_prod_unidades', 1100), key="mat_prod")
        mat_unit = colB.number_input("Material por unidad (Cantidad)", value=1.5, key="mat_unit")
        total_mat_req = prod_req * mat_unit
        st.info(f"Requerimiento Total: {total_mat_req:,.2f} unidades de material")
        
        st.markdown("---")
        st.markdown("**B. Presupuesto de Compras**")
        c1, c2, c3 = st.columns(3)
        mat_if = c1.number_input("Inv. Final Material", value=500.0, key="mc_if")
        mat_ii = c2.number_input("Inv. Inicial Material", value=200.0, key="mc_ii")
        costo_mat = c3.number_input("Costo unitario material ($)", value=10.0, key="mc_costo")
        
        compras_unidades = total_mat_req + mat_if - mat_ii
        costo_compras = compras_unidades * costo_mat
        
        st.markdown(f"""<div class='metric-card'><h3>${costo_compras:,.2f}</h3><p>Costo Total de Compras</p></div>""", unsafe_allow_html=True)

    # --- MANO DE OBRA ---
    with tabs[3]:
        st.subheader("Presupuesto de Mano de Obra Directa (MOD)")
        c1, c2, c3 = st.columns(3)
        mod_prod = c1.number_input("Producción Requerida", value=st.session_state.get('pres_prod_unidades', 1100), key="mod_prod")
        hrs_unit = c2.number_input("Horas por unidad", value=2.0, key="mod_hrs")
        cuota_hr = c3.number_input("Costo por Hora ($)", value=25.0, key="mod_costo")
        
        costo_mod = mod_prod * hrs_unit * cuota_hr
        st.markdown(f"""<div class='metric-card'><h3>${costo_mod:,.2f}</h3><p>Costo Total MOD</p></div>""", unsafe_allow_html=True)

    # --- VALUACIÓN ---
    with tabs[4]:
        st.subheader("Costo Unitario de Producción")
        c1, c2, c3 = st.columns(3)
        c_mat = c1.number_input("Costo Material Directo", value=15.0, key="val_mat")
        c_mod = c2.number_input("Costo MOD", value=50.0, key="val_mod")
        c_gif = c3.number_input("Gastos Ind. Fab. (GIF)", value=10.0, key="val_gif")
        
        unitario = c_mat + c_mod + c_gif
        st.markdown(f"""<div class='metric-card'><h3>${unitario:,.2f}</h3><p>Costo por Unidad</p></div>""", unsafe_allow_html=True)

# ==========================================
#        2. RAZONES FINANCIERAS
# ==========================================
elif modulo == "2. Razones Financieras":
    st.header("Análisis de Ratios Financieros")
    
    tabs = st.tabs(["Liquidez", "Apalancamiento", "Actividad", "Rentabilidad", "Flujos"])
    
    # --- LIQUIDEZ ---
    with tabs[0]:
        st.subheader("Liquidez")
        ac = st.number_input("Activo Circulante", 10000.0, key="l_ac")
        pc = st.number_input("Pasivo Circulante", 5000.0, key="l_pc")
        inv = st.number_input("Inventarios", 2000.0, key="l_inv")
        
        if pc > 0:
            rc = ac / pc
            pa = (ac - inv) / pc
            c1, c2 = st.columns(2)
            c1.markdown(f"<div class='metric-card'><h3>{rc:.2f}</h3><p>Razón Circulante</p></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><h3>{pa:.2f}</h3><p>Prueba Ácida</p></div>", unsafe_allow_html=True)

    # --- APALANCAMIENTO ---
    with tabs[1]:
        st.subheader("Apalancamiento")
        pasivo_total = st.number_input("Pasivo Total", 40000.0, key="a_pt")
        activo_total = st.number_input("Activo Total", 100000.0, key="a_at")
        capital_contable = st.number_input("Capital Contable", 60000.0, key="a_cc")
        
        if activo_total > 0 and capital_contable > 0:
            endeu = pasivo_total / activo_total
            d_c = pasivo_total / capital_contable
            
            st.write(f"Endeudamiento (Pasivo/Activo): **{endeu*100:.2f}%**")
            st.write(f"Apalancamiento (Pasivo/Capital): **{d_c:.2f}**")

    # --- ACTIVIDAD ---
    with tabs[2]:
        st.subheader("Actividad")
        costo_ventas = st.number_input("Costo de Ventas", 50000.0, key="act_cv")
        prom_inv = st.number_input("Inventario Promedio", 5000.0, key="act_inv")
        ventas_credito = st.number_input("Ventas a Crédito", 80000.0, key="act_vc")
        prom_cxc = st.number_input("Promedio Cuentas por Cobrar", 8000.0, key="act_cxc")
        
        c1, c2 = st.columns(2)
        if prom_inv > 0:
            rot_inv = costo_ventas / prom_inv
            c1.metric("Rotación Inventarios", f"{rot_inv:.2f} veces")
        if prom_cxc > 0:
            rot_cxc = ventas_credito / prom_cxc
            c2.metric("Rotación Cuentas por Cobrar", f"{rot_cxc:.2f} veces")

    # --- RENTABILIDAD ---
    with tabs[3]:
        st.subheader("Rentabilidad")
        utilidad_neta = st.number_input("Utilidad Neta", 15000.0, key="r_un")
        ventas_netas = st.number_input("Ventas Netas", 100000.0, key="r_vn")
        act_tot = st.number_input("Activo Total", 200000.0, key="r_at")
        
        if ventas_netas > 0 and act_tot > 0:
            margen = utilidad_neta / ventas_netas
            roa = utilidad_neta / act_tot
            
            c1, c2 = st.columns(2)
            c1.markdown(f"<div class='metric-card'><h3>{margen*100:.2f}%</h3><p>Margen Neto</p></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><h3>{roa*100:.2f}%</h3><p>ROA</p></div>", unsafe_allow_html=True)

    # --- FLUJOS ---
    with tabs[4]:
        st.subheader("Dividendos y Flujo")
        utilidad = st.number_input("Utilidad Neta", 10000.0, key="d_un")
        dividendos = st.number_input("Dividendos Pagados", 2000.0, key="d_div")
        depreciacion = st.number_input("Depreciación", 5000.0, key="d_dep")
        
        if utilidad > 0:
            payout = dividendos / utilidad
            st.metric("Payout Ratio", f"{payout*100:.2f}%")
        
        flujo_op = utilidad + depreciacion
        st.markdown(f"<div class='metric-card'><h3>${flujo_op:,.2f}</h3><p>Flujo de Efectivo Operativo</p></div>", unsafe_allow_html=True)


# ==========================================
#        3. EVALUACIÓN DE PROYECTOS
# ==========================================
elif modulo == "3. Evaluación de Proyectos":
    st.header("Evaluación de Inversión")
    
    tabs = st.tabs(["Valor en Libros", "WACC", "Indicadores (VAN/TIR)"])
    
    # --- VALOR EN LIBROS ---
    with tabs[0]:
        st.subheader("Valor en Libros")
        activos = st.number_input("Total Activos", 150000.0, key="vl_a")
        pasivos = st.number_input("Total Pasivos", 50000.0, key="vl_p")
        acciones = st.number_input("Número de Acciones", 1000.0, key="vl_acc")
        
        valor_libros = activos - pasivos
        c1, c2 = st.columns(2)
        c1.metric("Valor en Libros Total", f"${valor_libros:,.2f}")
        if acciones > 0:
            c2.metric("Valor en Libros por Acción", f"${valor_libros/acciones:,.2f}")
            
    # --- WACC ---
    with tabs[1]:
        st.subheader("Costo Promedio Ponderado de Capital (WACC)")
        st.markdown("<div class='formula'>WACC = (E/V * Ke) + (D/V * Kd * (1-t))</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            peso_e = st.slider("% Capital Propio (Equity)", 0, 100, 60) / 100
            costo_e = st.number_input("Costo del Equity (Ke) %", 0.0, 100.0, 12.0) / 100
        with c2:
            peso_d = 1 - peso_e
            st.write(f"% Deuda: {peso_d*100:.0f}%")
            costo_d = st.number_input("Costo de la Deuda (Kd) %", 0.0, 100.0, 8.0) / 100
            tax = st.number_input("Tasa Impositiva (Tax) %", 0.0, 100.0, 30.0) / 100
            
        wacc = (peso_e * costo_e) + (peso_d * costo_d * (1 - tax))
        st.markdown(f"""<div class='metric-card'><h3>{wacc*100:.2f}%</h3><p>WACC Calculado</p></div>""", unsafe_allow_html=True)

    # --- INDICADORES ---
    with tabs[2]:
        st.subheader("Indicadores de Rentabilidad")
        
        inversion = st.number_input("Inversión Inicial (Negativo)", value=-100000.0, max_value=0.0, step=1000.0, key="eval_inv")
        tasa = st.number_input("Tasa de Descuento %", 0.0, 100.0, 10.0, key="eval_tasa") / 100
        n_anios = st.slider("Horizonte de tiempo (años)", 1, 10, 5)
        
        flujos = []
        st.write("Flujos de Efectivo Netos:")
        cols = st.columns(n_anios)
        for i in range(n_anios):
            f = cols[i].number_input(f"Año {i+1}", value=30000.0, key=f"f_{i}")
            flujos.append(f)
            
        flujos_caja = [inversion] + flujos
        
        st.markdown("---")
        if st.button("Calcular Resultados"):
            # Cálculos
            van = npf.npv(tasa, flujos_caja)
            try:
                tir = npf.irr(flujos_caja) * 100
            except:
                tir = 0.0
            
            # Payback
            acumulado = 0
            payback = "No recuperado en el periodo"
            for i, flujo in enumerate(flujos_caja):
                acumulado += flujo
                if acumulado >= 0:
                    payback = f"{i} años aprox."
                    break
            
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"<div class='metric-card'><h3>${van:,.2f}</h3><p>Valor Actual Neto (VAN)</p></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><h3>{tir:.2f}%</h3><p>Tasa Interna de Retorno (TIR)</p></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='metric-card'><h3>{payback}</h3><p>Periodo de Recuperación</p></div>", unsafe_allow_html=True)
            
            if van > 0:
                st.success("Resultado: El proyecto es financieramente VIABLE.")
            else:
                st.error("Resultado: El proyecto NO es financieramente viable.")