"""
Lógica Subatómica - Probador de Teoremas
Aplicación Web con Streamlit

Para ejecutar:
    pip install streamlit
    streamlit run app.py
"""

import streamlit as st
from io import StringIO
import sys

# Importar el sistema de lógica
from logic import (
    parse, ParseError,
    TableauProver,
    AtomicTerm, Universal, Particular,
    Conjunction, Disjunction, Conditional, Biconditional,
    Negation, Existential
)

st.set_page_config(
    page_title="Lógica Subatómica - Probador de Teoremas",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS CSS
# ============================================================================

st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .formula-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        font-family: monospace;
    }
    .result-valid {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        color: #155724;
        font-weight: bold;
    }
    .result-invalid {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        color: #721c24;
        font-weight: bold;
    }
    .step-box {
        background-color: #fff3cd;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        margin: 0.5rem 0;
        font-family: monospace;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<div class="main-header">🔬 Lógica Subatómica</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Probador de Teoremas con Tableaux Semánticos</div>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - INFORMACIÓN Y AYUDA
# ============================================================================

with st.sidebar:
    st.header("📚 Guía de Sintaxis")
    
    st.markdown("""
    ### Términos
    - `A, B, C, ...` - Términos atómicos
    - `~A` - Complemento (no-A)
    - `^A` - Privación (in-A)
    
    ### Fórmulas Categoriales
    - `[A]B` - Universal (Todo A es B)
    - `<A>B` - Particular (Algún A es B)
    
    ### Conectivos
    - `&` - Conjunción (y)
    - `|` - Disyunción (o)
    - `->` - Condicional (si...entonces)
    - `<->` - Bicondicional (si y solo si)
    - `-` - Negación (no)
    - `( )` - Paréntesis
    
    ### Ejemplos
    ```
    [A]B              Todo A es B
    <A>B              Algún A es B
    -[A]B             No todo A es B
    [~A]^B            Todo no-A es in-B
    [A]B & [B]C       Premisas conjuntas
    A | -A            Tercero excluido
    ```
    """)
    
    st.divider()
    
    st.header("ℹ️ Acerca de")
    st.markdown("""
    Sistema de lógica subatómica con tableaux semánticos.
    
    **Características:**
    - Cuantificadores universales y particulares
    - Operadores de complemento y privación
    - Conectivos proposicionales clásicos
    - Relaciones Q (ternaria) y S (binaria)
    
    **Versión:** 1.0
    """)

# ============================================================================
# MAIN CONTENT
# ============================================================================

tab1, tab2, tab3 = st.tabs(["🧪 Probar Fórmula", "📜 Probar Argumento", "📚 Ejemplos"])

# ----------------------------------------------------------------------------
# TAB 1: PROBAR FÓRMULA INDIVIDUAL
# ----------------------------------------------------------------------------

with tab1:
    st.header("Probar Validez de una Fórmula")
    st.markdown("Ingresa una fórmula para verificar si es válida (tautología).")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        formula_input = st.text_input(
            "Fórmula:",
            value="A | -A",
            help="Escribe la fórmula usando la sintaxis de la guía"
        )
    
    with col2:
        prove_button = st.button("🔍 Probar", type="primary", use_container_width=True)
    
    show_steps = st.checkbox("Mostrar paso a paso", value=False)
    
    if prove_button and formula_input:
        try:
            # Parsear la fórmula
            parsed = parse(formula_input)
            
            st.markdown("### Fórmula Parseada")
            st.markdown(f'<div class="formula-box">{parsed}</div>', unsafe_allow_html=True)
            
            # Capturar salida verbose
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            # Probar la fórmula
            prover = TableauProver(max_iterations=50)
            result = prover.prove(parsed, verbose=show_steps)
            
            # Restaurar stdout
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            # Mostrar resultado
            st.markdown("### Resultado")
            
            if result:
                st.markdown(
                    '<div class="result-valid">✓ La fórmula es VÁLIDA (Tautología)</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="result-invalid">✗ La fórmula NO es válida</div>',
                    unsafe_allow_html=True
                )
            
            if show_steps and output:
                st.markdown("### Proceso del Tableau")
                with st.expander("Ver pasos detallados", expanded=True):
                    st.text(output)
        
        except ParseError as e:
            st.error(f"❌ Error al parsear la fórmula: {str(e)}")
            st.info("💡 Revisa la sintaxis en la guía de la barra lateral.")
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
            st.exception(e)

# ----------------------------------------------------------------------------
# TAB 2: PROBAR ARGUMENTO
# ----------------------------------------------------------------------------

with tab2:
    st.header("Probar Validez de un Argumento")
    st.markdown("Ingresa premisas y conclusión para verificar si el argumento es válido.")
    
    st.markdown("#### Premisas")
    
    num_premises = st.number_input("Número de premisas:", min_value=1, max_value=10, value=2)
    
    premises_input = []
    for i in range(num_premises):
        default_val = "[A]B" if i == 0 else "[B]C" if i == 1 else ""
        premise = st.text_input(f"Premisa {i+1}:", key=f"premise_{i}", value=default_val)
        premises_input.append(premise)
    
    st.markdown("#### Conclusión")
    conclusion_input = st.text_input("Conclusión:", value="[A]C")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        prove_arg_button = st.button("🔍 Probar Argumento", type="primary", use_container_width=True)
    
    show_steps_arg = st.checkbox("Mostrar paso a paso", value=False, key="show_steps_arg")
    
    if prove_arg_button:
        try:
            # Parsear premisas y conclusión
            parsed_premises = [parse(p) for p in premises_input if p.strip()]
            parsed_conclusion = parse(conclusion_input)
            
            st.markdown("### Argumento")
            
            st.markdown("**Premisas:**")
            for i, (p_str, p_parsed) in enumerate(zip(premises_input, parsed_premises), 1):
                st.markdown(f'{i}. <div class="formula-box">{p_parsed}</div>', unsafe_allow_html=True)
            
            st.markdown(f'**Conclusión:** <div class="formula-box">{parsed_conclusion}</div>', unsafe_allow_html=True)
            
            # Capturar salida
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            # Probar argumento
            prover = TableauProver(max_iterations=50)
            result = prover.prove_argument(parsed_premises, parsed_conclusion, verbose=show_steps_arg)
            
            # Restaurar stdout
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            st.markdown("### Resultado")
            
            if result:
                st.markdown(
                    '<div class="result-valid">✓ El argumento es VÁLIDO</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="result-invalid">✗ El argumento NO es válido</div>',
                    unsafe_allow_html=True
                )
            
            if show_steps_arg and output:
                st.markdown("### Proceso del Tableau")
                with st.expander("Ver pasos detallados", expanded=True):
                    st.text(output)
        
        except ParseError as e:
            st.error(f"❌ Error al parsear: {str(e)}")
            st.info("💡 Revisa la sintaxis en la guía.")
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
            st.exception(e)

# ----------------------------------------------------------------------------
# TAB 3: EJEMPLOS PREDEFINIDOS
# ----------------------------------------------------------------------------

with tab3:
    st.header("Ejemplos de Silogismos y Fórmulas")
    
    st.markdown("### Silogismos Clásicos")
    
    examples = {
        "Barbara": {
            "premises": ["[M]P", "[S]M"],
            "conclusion": "[S]P",
            "description": "Todo M es P, Todo S es M ⊢ Todo S es P"
        },
        "Celarent": {
            "premises": ["-<M>P", "[S]M"],
            "conclusion": "-<S>P",
            "description": "Ningún M es P, Todo S es M ⊢ Ningún S es P"
        },
        "Darii": {
            "premises": ["[M]P", "<S>M"],
            "conclusion": "<S>P",
            "description": "Todo M es P, Algún S es M ⊢ Algún S es P"
        },
        "Ferio": {
            "premises": ["-<M>P", "<S>M"],
            "conclusion": "<S>~P",
            "description": "Ningún M es P, Algún S es M ⊢ Algún S es no-P"
        },
    }
    
    for name, example in examples.items():
        with st.expander(f"**{name}** - {example['description']}"):
            st.markdown("**Premisas:**")
            for i, p in enumerate(example['premises'], 1):
                st.code(p, language=None)
            
            st.markdown("**Conclusión:**")
            st.code(example['conclusion'], language=None)
            
            if st.button(f"Probar {name}", key=f"example_{name}"):
                try:
                    parsed_premises = [parse(p) for p in example['premises']]
                    parsed_conclusion = parse(example['conclusion'])
                    
                    with st.spinner(f"Probando {name}..."):
                        prover = TableauProver(max_iterations=50)
                        result = prover.prove_argument(parsed_premises, parsed_conclusion, verbose=False)
                    
                    if result:
                        st.success(f"✓ {name} es VÁLIDO")
                    else:
                        st.warning(f"✗ {name} NO es válido en este sistema")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.divider()
    
    st.markdown("### Fórmulas Lógicas Clásicas")
    
    logic_examples = {
        "Ley del Tercero Excluido": "A | -A",
        "Ley de No Contradicción": "-(A & -A)",
        "Modus Ponens": "(A & (A -> B)) -> B",
        "Modus Tollens": "((A -> B) & -B) -> -A",
        "Silogismo Hipotético": "((A -> B) & (B -> C)) -> (A -> C)",
        "Dilema Constructivo": "((A -> B) & (C -> D) & (A | C)) -> (B | D)",
    }
    
    for name, formula in logic_examples.items():
        with st.expander(f"**{name}**"):
            st.code(formula, language=None)
            if st.button(f"Probar {name}", key=f"logic_{name}"):
                try:
                    parsed = parse(formula)
                    
                    with st.spinner(f"Probando {name}..."):
                        prover = TableauProver(max_iterations=50)
                        result = prover.prove(parsed, verbose=False)
                    
                    if result:
                        st.success(f"✓ {name} es VÁLIDO")
                    else:
                        st.warning(f"✗ {name} NO es válido")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    Lógica Subatómica - Probador de Teoremas | Versión 1.0<br>
    Sistema de tableaux semánticos para lógica con cuantificadores y operadores de término
</div>
""", unsafe_allow_html=True)
