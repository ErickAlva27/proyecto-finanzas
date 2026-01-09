import streamlit as st
import pandas as pd
import math
import numpy_financial as npf

# --- CONFIGURACIÓN GLOBAL ---
st.set_page_config(page_title="Sistema Integral de Finanzas", layout="wide")

# --- ESTILOS CSS PREMIUM (MEJORADO) ---
st.markdown("""
    <style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Configuración global */
    .main { 
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Títulos principales */
    h1 { 
        font-family: 'Inter', sans-serif;
        color: #1e293b;
        font-size: 2.2rem;
        font-weight: 800;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 20px;
        margin-bottom: 30px;
        letter-spacing: -0.5px;
    }
    
    h2 { 
        font-family: 'Inter', sans-serif;
        color: #334155;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    h3 { 
        font-family: 'Inter', sans-serif;
        color: #475569;
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 20px;
    }
    
    /* Tarjetas métricas mejoradas */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        text-align: center;
        margin-bottom: 20px;
        transition: transform 0.2s;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card h3 { 
        color: #0f172a;
        font-size: 24px;
        margin: 5px 0;
        font-weight: 800;
    }
    
    .metric-card p { 
        color: #64748b;
        font-size: 13px;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    /* Variantes de tarjetas */
    .metric-success::before { background: linear-gradient(90deg, #10b981, #34d399); }
    .metric-success h3 { color: #059669; }
    
    .metric-warning::before { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .metric-warning h3 { color: #d97706; }
    
    .metric-danger::before { background: linear-gradient(90deg, #ef4444, #f87171); }
    .metric-danger h3 { color: #dc2626; }
    
    /* Botones mejorados */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border-radius: 8px;
        border: none;
        height: 3em;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        transition: all 0.2s;
    }
    
    .stButton>button:hover { 
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-1px);
    }
    
    /* DataFrames y Tablas */
    .stDataFrame { 
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Cajas de información */
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 8px 8px 0;
        color: #1e3a8a;
    }
    
    .warning-box {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 8px 8px 0;
        color: #92400e;
    }
    
    .success-box {
        background: #ecfdf5;
        border-left: 4px solid #10b981;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 8px 8px 0;
        color: #065f46;
    }

    /* Sidebar personalizado */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Sistema Integral de Finanzas Pro - 6NM62")

# --- MENÚ LATERAL ---
st.sidebar.header("Navegación")
modulo = st.sidebar.radio("Seleccione Módulo:", [
    "Inicio",
    "1. Presupuestos Operativos",
    "2. Análisis Financiero (Razones)",
    "3. Evaluación de Inversión"
])
st.sidebar.markdown("---")
st.sidebar.info("Versión Integrada 4.0")

# ==============================================================================
#        MÓDULO 0: INICIO
# ==============================================================================
if modulo == "Inicio":
    st.markdown("#### Panel de Control Principal")
    st.write("Bienvenido al sistema. Seleccione una opción del menú lateral para proceder.")
    
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='metric-card'><h3>Módulo 1</h3><p>Presupuestos Maestros</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='metric-card'><h3>Módulo 2</h3><p>Ratios Financieros</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='metric-card'><h3>Módulo 3</h3><p>Proyectos & Reemplazo</p></div>", unsafe_allow_html=True)

# ==============================================================================
#        MÓDULO 1: PRESUPUESTOS OPERATIVOS
# ==============================================================================
elif modulo == "1. Presupuestos Operativos":
    st.header("Generador de Presupuestos Maestros")
    
    # Inicializar variables de sesión si no existen
    if 'datos_inicializados' not in st.session_state:
        st.session_state['datos_inicializados'] = True
        st.session_state['metodo_valuacion'] = 'UEPS'
    
    # Selector de método de valuación
    with st.expander("Configuración del Sistema (Valuación)", expanded=False):
        st.session_state['metodo_valuacion'] = st.radio(
            "Método de Valuación de Inventarios:",
            ['UEPS', 'PEPS', 'Promedio Ponderado'],
            horizontal=True
        )
        st.info(f"Método seleccionado: **{st.session_state['metodo_valuacion']}**")
    
    tabs = st.tabs([
        "1. Ventas", "2. Producción", "3. Materiales", "4. Mano de Obra", 
        "5. GIF", "6. Costo Prod.", "7. Costo Ventas", "8. Estado Resultados"
    ])
    
    # ==================== TAB 1: VENTAS ====================
    with tabs[0]:
        st.subheader("Presupuesto de Ventas")
        c1, c2 = st.columns(2)
        unidades = c1.number_input("Unidades a vender", 0, 1000000, 63000, key="pv_uni")
        precio = c2.number_input("Precio Unitario ($)", 0.0, 100000.0, 420.0, key="pv_precio")
        
        ingreso = unidades * precio
        st.session_state['ventas_unidades'] = unidades
        st.session_state['ventas_ingresos'] = ingreso
        
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<div class='metric-card metric-success'><h3>{unidades:,}</h3><p>Unidades</p></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-card'><h3>${precio:,.2f}</h3><p>Precio Unitario</p></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric-card metric-success'><h3>${ingreso:,.2f}</h3><p>Ingresos Totales</p></div>", unsafe_allow_html=True)

    # ==================== TAB 2: PRODUCCIÓN ====================
    with tabs[1]:
        st.subheader("Presupuesto de Producción")
        col1, col2, col3 = st.columns(3)
        v_est = col1.number_input("Ventas Estimadas", value=st.session_state.get('ventas_unidades', 63000), key="pp_ventas")
        if_des = col2.number_input("Inventario Final Deseado", value=6000, key="pp_if")
        ii_est = col3.number_input("Inventario Inicial", value=5000, key="pp_ii")
        
        prod_req = v_est + if_des - ii_est
        st.session_state['prod_unidades'] = prod_req
        st.session_state['prod_inv_inicial_pt'] = ii_est
        st.session_state['prod_inv_final_pt'] = if_des
        
        st.markdown(f"<div class='metric-card metric-success'><h3>{prod_req:,}</h3><p>Unidades a Producir</p></div>", unsafe_allow_html=True)

    # ==================== TAB 3: MATERIALES (CON VALUACIÓN) ====================
    with tabs[2]:
        st.subheader("Presupuesto de Materiales")
        
        # Lógica de cálculo (resumida para visualización limpia)
        prod = st.session_state.get('prod_unidades', 64000)
        
        # --- INPUTS MATERIAL A ---
        st.markdown("**Material A**")
        c1, c2, c3, c4 = st.columns(4)
        std_a = c1.number_input("Piezas/Unidad (A)", 7.0, key="std_a")
        ii_a = c2.number_input("Inv. Inicial (A)", 40000.0, key="ii_a")
        if_a = c3.number_input("Inv. Final (A)", 35000.0, key="if_a")
        costo_a = c4.number_input("Costo Compra (A)", 6.0, key="c_a")
        precio_ii_a = 5.0 # Valor fijo o input extra si se desea
        
        req_a = prod * std_a
        compra_a = req_a + if_a - ii_a
        costo_compra_a = compra_a * costo_a
        
        # --- INPUTS MATERIAL B ---
        st.markdown("**Material B**")
        d1, d2, d3, d4 = st.columns(4)
        std_b = d1.number_input("Piezas/Unidad (B)", 3.0, key="std_b")
        ii_b = d2.number_input("Inv. Inicial (B)", 15000.0, key="ii_b")
        if_b = d3.number_input("Inv. Final (B)", 12000.0, key="if_b")
        costo_b = d4.number_input("Costo Compra (B)", 12.0, key="c_b")
        precio_ii_b = 11.0
        
        req_b = prod * std_b
        compra_b = req_b + if_b - ii_b
        
        # --- VALUACIÓN ---
        def valuar(ii, p_ii, compras, p_compras, consumo, metodo):
            total = ii + compras
            if metodo == 'UEPS':
                if consumo <= compras:
                    return consumo * p_compras
                else:
                    return (compras * p_compras) + ((consumo - compras) * p_ii)
            elif metodo == 'PEPS':
                if consumo <= ii:
                    return consumo * p_ii
                else:
                    return (ii * p_ii) + ((consumo - ii) * p_compras)
            else: # Promedio
                valor_total = (ii * p_ii) + (compras * p_compras)
                prom = valor_total / total
                return consumo * prom

        costo_uso_a = valuar(ii_a, precio_ii_a, compra_a, costo_a, req_a, st.session_state['metodo_valuacion'])
        costo_uso_b = valuar(ii_b, precio_ii_b, compra_b, costo_b, req_b, st.session_state['metodo_valuacion'])
        
        st.session_state['mp_total_produccion'] = costo_uso_a + costo_uso_b
        
        c1, c2 = st.columns(2)
        c1.markdown(f"<div class='metric-card'><h3>${costo_uso_a:,.2f}</h3><p>Costo Uso Material A</p></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><h3>${costo_uso_b:,.2f}</h3><p>Costo Uso Material B</p></div>", unsafe_allow_html=True)

    # ==================== TAB 4: MANO DE OBRA ====================
    with tabs[3]:
        st.subheader("Mano de Obra Directa")
        c1, c2, c3 = st.columns(3)
        mod_prod = c1.number_input("Producción", value=st.session_state.get('prod_unidades', 64000), key="mod_p", disabled=True)
        hrs = c2.number_input("Horas/Unidad", 13.0, key="mod_h")
        cuota = c3.number_input("Tarifa/Hora", 9.0, key="mod_c")
        
        costo_mod = mod_prod * hrs * cuota
        st.session_state['mod_costo_total'] = costo_mod
        st.markdown(f"<div class='metric-card metric-success'><h3>${costo_mod:,.2f}</h3><p>Costo Total MOD</p></div>", unsafe_allow_html=True)

    # ==================== TAB 5: GIF ====================
    with tabs[4]:
        st.subheader("Gastos Indirectos (GIF)")
        c1, c2 = st.columns(2)
        with c1:
            g1 = st.number_input("Material Indirecto", 1320000.0)
            g2 = st.number_input("Mano Obra Ind.", 2130000.0)
            g3 = st.number_input("Renta", 360000.0)
        with c2:
            g4 = st.number_input("Energía", 464000.0)
            g5 = st.number_input("Mantenimiento", 674000.0)
            g6 = st.number_input("Varios", 500000.0)
            
        total_gif = g1 + g2 + g3 + g4 + g5 + g6
        st.session_state['gif_total'] = total_gif
        st.markdown(f"<div class='metric-card'><h3>${total_gif:,.2f}</h3><p>Total GIF</p></div>", unsafe_allow_html=True)

    # ==================== TAB 6: COSTO PRODUCCIÓN ====================
    with tabs[5]:
        st.subheader("Costo de Producción")
        mp = st.session_state.get('mp_total_produccion', 0)
        mod = st.session_state.get('mod_costo_total', 0)
        gif = st.session_state.get('gif_total', 0)
        unidades = st.session_state.get('prod_unidades', 1)
        
        total = mp + mod + gif
        unitario = total / unidades if unidades > 0 else 0
        st.session_state['costo_unitario'] = unitario
        
        c1, c2 = st.columns(2)
        c1.markdown(f"<div class='metric-card metric-success'><h3>${total:,.2f}</h3><p>Costo Total</p></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><h3>${unitario:,.2f}</h3><p>Costo Unitario</p></div>", unsafe_allow_html=True)

    # ==================== TAB 7: COSTO VENTAS ====================
    with tabs[6]:
        st.subheader("Costo de Ventas")
        metodo = st.session_state['metodo_valuacion']
        st.info(f"Aplicando método: {metodo}")
        
        ii_pt = st.number_input("Inv. Inicial PT (unidades)", value=5000)
        costo_ii = st.number_input("Costo Unit. Inv. Inicial", value=250.0)
        
        unidades_ven = st.session_state.get('ventas_unidades', 63000)
        unidades_prod = st.session_state.get('prod_unidades', 64000)
        costo_prod = st.session_state.get('costo_unitario', 0)
        
        # Lógica simplificada de valuación PT
        costo_ventas = 0
        if metodo == 'UEPS':
            if unidades_ven <= unidades_prod:
                costo_ventas = unidades_ven * costo_prod
            else:
                costo_ventas = (unidades_prod * costo_prod) + ((unidades_ven - unidades_prod) * costo_ii)
        elif metodo == 'PEPS':
            if unidades_ven <= ii_pt:
                costo_ventas = unidades_ven * costo_ii
            else:
                costo_ventas = (ii_pt * costo_ii) + ((unidades_ven - ii_pt) * costo_prod)
        else: # Promedio
            total_val = (ii_pt * costo_ii) + (unidades_prod * costo_prod)
            total_uni = ii_pt + unidades_prod
            prom = total_val / total_uni if total_uni > 0 else 0
            costo_ventas = unidades_ven * prom
            
        st.session_state['costo_ventas'] = costo_ventas
        st.markdown(f"<div class='metric-card metric-danger'><h3>${costo_ventas:,.2f}</h3><p>Costo de Ventas</p></div>", unsafe_allow_html=True)

    # ==================== TAB 8: ESTADO RESULTADOS ====================
    with tabs[7]:
        st.subheader("Estado de Resultados")
        
        st.markdown("##### Gastos Operativos")
        go = st.number_input("Total Gastos Operación (Venta/Admin)", value=7020000.0)
        
        ingresos = st.session_state.get('ventas_ingresos', 0)
        cv = st.session_state.get('costo_ventas', 0)
        
        ub = ingresos - cv
        uo = ub - go
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='metric-card metric-success'><h3>${ingresos:,.2f}</h3><p>Ventas</p></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card metric-warning'><h3>${ub:,.2f}</h3><p>Utilidad Bruta</p></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='metric-card metric-success'><h3>${uo:,.2f}</h3><p>Utilidad Operativa</p></div>", unsafe_allow_html=True)

# ==============================================================================
#        MÓDULO 2: ANÁLISIS FINANCIERO (RESTAURADO CON NUEVO ESTILO)
# ==============================================================================
elif modulo == "2. Análisis Financiero (Razones)":
    st.header("Análisis de Indicadores Financieros")
    
    tabs = st.tabs(["Liquidez", "Apalancamiento", "Actividad", "Rentabilidad"])
    
    # --- LIQUIDEZ ---
    with tabs[0]:
        st.subheader("Razones de Liquidez")
        c1, c2, c3 = st.columns(3)
        ac = c1.number_input("Activo Circulante", 15000.0, key="l_ac")
        pc = c2.number_input("Pasivo Circulante", 5000.0, key="l_pc")
        inv = c3.number_input("Inventarios", 3000.0, key="l_inv")
        
        if pc > 0:
            rc = ac / pc
            pa = (ac - inv) / pc
            
            st.markdown("---")
            k1, k2 = st.columns(2)
            k1.markdown(f"<div class='metric-card'><h3>{rc:.2f}</h3><p>Razón Circulante</p></div>", unsafe_allow_html=True)
            k2.markdown(f"<div class='metric-card'><h3>{pa:.2f}</h3><p>Prueba Ácida</p></div>", unsafe_allow_html=True)

    # --- APALANCAMIENTO ---
    with tabs[1]:
        st.subheader("Estructura de Capital")
        c1, c2, c3 = st.columns(3)
        pt = c1.number_input("Pasivo Total", 40000.0, key="a_pt")
        at = c2.number_input("Activo Total", 100000.0, key="a_at")
        cc = c3.number_input("Capital Contable", 60000.0, key="a_cc")
        
        if at > 0 and cc > 0:
            st.markdown("---")
            k1, k2 = st.columns(2)
            k1.markdown(f"<div class='metric-card metric-warning'><h3>{pt/at*100:.2f}%</h3><p>Endeudamiento</p></div>", unsafe_allow_html=True)
            k2.markdown(f"<div class='metric-card'><h3>{pt/cc:.2f}</h3><p>Apalancamiento</p></div>", unsafe_allow_html=True)

    # --- ACTIVIDAD ---
    with tabs[2]:
        st.subheader("Eficiencia Operativa")
        c1, c2 = st.columns(2)
        cv = c1.number_input("Costo de Ventas", 50000.0, key="act_cv")
        inv_prom = c2.number_input("Inventario Promedio", 5000.0, key="act_inv")
        
        if inv_prom > 0:
            st.markdown("---")
            st.markdown(f"<div class='metric-card'><h3>{cv/inv_prom:.2f} veces</h3><p>Rotación Inventarios</p></div>", unsafe_allow_html=True)

    # --- RENTABILIDAD ---
    with tabs[3]:
        st.subheader("Rentabilidad")
        c1, c2, c3 = st.columns(3)
        un = c1.number_input("Utilidad Neta", 15000.0, key="r_un")
        vn = c2.number_input("Ventas Netas", 100000.0, key="r_vn")
        at_r = c3.number_input("Activo Total", 200000.0, key="r_at")
        
        if vn > 0 and at_r > 0:
            st.markdown("---")
            k1, k2 = st.columns(2)
            k1.markdown(f"<div class='metric-card metric-success'><h3>{un/vn*100:.2f}%</h3><p>Margen Neto</p></div>", unsafe_allow_html=True)
            k2.markdown(f"<div class='metric-card metric-success'><h3>{un/at_r*100:.2f}%</h3><p>ROA</p></div>", unsafe_allow_html=True)

# ==============================================================================
#        MÓDULO 3: EVALUACIÓN DE INVERSIÓN (RESTAURADO CON NUEVO ESTILO)
# ==============================================================================
elif modulo == "3. Evaluación de Inversión":
    st.header("Evaluación de Proyectos de Inversión")
    
    tipo_eval = st.radio("Tipo de Evaluación:", ["Proyecto Nuevo", "Reemplazo de Activos (Avanzado)"], horizontal=True)
    st.markdown("---")

    if tipo_eval == "Proyecto Nuevo":
        c1, c2 = st.columns(2)
        inv = c1.number_input("Inversión Inicial (-)", value=-100000.0, step=1000.0)
        tasa = c2.number_input("Tasa Descuento (%)", value=12.0) / 100
        n = st.slider("Años", 1, 10, 5)
        
        flujos = []
        cols = st.columns(n)
        for i in range(n):
            flujos.append(cols[i].number_input(f"F{i+1}", 30000.0, key=f"f{i}"))
            
        if st.button("Calcular"):
            fc = [inv] + flujos
            van = npf.npv(tasa, fc)
            tir = npf.irr(fc) * 100
            
            k1, k2 = st.columns(2)
            k1.markdown(f"<div class='metric-card metric-success'><h3>${van:,.2f}</h3><p>VAN</p></div>", unsafe_allow_html=True)
            k2.markdown(f"<div class='metric-card'><h3>{tir:.2f}%</h3><p>TIR</p></div>", unsafe_allow_html=True)

    else:
        st.subheader("Análisis de Reemplazo (Excel Logic)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='info-box'><b>Activo Viejo</b></div>", unsafe_allow_html=True)
            v_venta = st.number_input("Precio Venta Hoy", 1000000.0)
            v_libros = st.number_input("Valor en Libros Hoy", 1400000.0)
            
        with col2:
            st.markdown("<div class='success-box'><b>Activo Nuevo</b></div>", unsafe_allow_html=True)
            n_costo = st.number_input("Costo Nuevo + Instalación", 3300000.0)
            n_vida = st.number_input("Vida Útil Nuevo", 5)
        
        tax = st.number_input("Impuestos (%)", 30.0) / 100
        wacc = st.number_input("WACC (%)", 20.0) / 100
        
        if st.button("Calcular Reemplazo"):
            # 1. Inversión Neta
            utilidad_vta = v_venta - v_libros
            efecto_fiscal = utilidad_vta * tax
            inv_inicial = n_costo - v_venta + efecto_fiscal
            
            st.markdown(f"<div class='metric-card metric-warning'><h3>${inv_inicial:,.2f}</h3><p>Inversión Inicial Neta</p></div>", unsafe_allow_html=True)
            
            st.info("Simulación de flujos (Ejemplo base): Incremento $906,000 anual")
            flujos_netos = [906000.0] * n_vida
            flujos_totales = [-inv_inicial] + flujos_netos
            
            van = npf.npv(wacc, flujos_totales)
            tir = npf.irr(flujos_totales) * 100
            
            k1, k2 = st.columns(2)
            k1.markdown(f"<div class='metric-card metric-success'><h3>${van:,.2f}</h3><p>VAN Incremental</p></div>", unsafe_allow_html=True)
            k2.markdown(f"<div class='metric-card'><h3>{tir:.2f}%</h3><p>TIR</p></div>", unsafe_allow_html=True)