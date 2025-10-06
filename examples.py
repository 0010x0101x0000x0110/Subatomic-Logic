"""
Ejemplos de uso del Probador de Teoremas de Lógica Subatómica
"""

from logic import (
    parse, TableauProver,
    AtomicTerm, Universal, Particular,
    Conjunction, Disjunction, Conditional,
    Negation, Existential, Complement, Privation
)

def ejemplo_parser():
    """Ejemplo de cómo usar el parser"""
    print("="*60)
    print("EJEMPLO 1: PARSER DE FÓRMULAS")
    print("="*60)
    
    formulas = [
        "[A]B",                    # Todo A es B
        "<A>B",                    # Algún A es B
        "-[A]B",                   # No todo A es B
        "[~A]^B",                  # Todo no-A es in-B
        "([A]B & [B]C) -> [A]C",  # Barbara
    ]
    
    for f in formulas:
        parsed = parse(f)
        print(f"Input:  {f}")
        print(f"Parsed: {parsed}")
        print()


def ejemplo_barbara():
    """Ejemplo del silogismo Barbara"""
    print("="*60)
    print("EJEMPLO 2: SILOGISMO BARBARA")
    print("="*60)
    print("Premisas:")
    print("  1. Todo A es B")
    print("  2. Todo B es C")
    print("Conclusión:")
    print("  Todo A es C")
    print()
    
    # Opción 1: Usando el parser
    print("--- Usando el parser ---")
    premise1 = parse("[A]B")
    premise2 = parse("[B]C")
    conclusion = parse("[A]C")
    
    prover = TableauProver()
    result = prover.prove_argument([premise1, premise2], conclusion, verbose=False)
    
    print(f"Resultado: Barbara es {'VÁLIDO' if result else 'INVÁLIDO'}")
    print()
    
    # Opción 2: Construyendo directamente
    print("--- Construyendo directamente ---")
    A = AtomicTerm('A')
    B = AtomicTerm('B')
    C = AtomicTerm('C')
    
    premise1 = Universal(A, B)
    premise2 = Universal(B, C)
    conclusion = Universal(A, C)
    
    prover = TableauProver()
    result = prover.prove_argument([premise1, premise2], conclusion, verbose=True)


def ejemplo_celarent():
    """Ejemplo del silogismo Celarent"""
    print("\n" + "="*60)
    print("EJEMPLO 3: SILOGISMO CELARENT")
    print("="*60)
    print("Premisas:")
    print("  1. Ningún M es P (-<M>P)")
    print("  2. Todo S es M ([S]M)")
    print("Conclusión:")
    print("  Ningún S es P (-<S>P)")
    print()
    
    premise1 = parse("-<M>P")
    premise2 = parse("[S]M")
    conclusion = parse("-<S>P")
    
    prover = TableauProver()
    result = prover.prove_argument([premise1, premise2], conclusion, verbose=False)
    
    print(f"Resultado: Celarent es {'VÁLIDO' if result else 'INVÁLIDO'}")


def ejemplo_darii():
    """Ejemplo del silogismo Darii"""
    print("\n" + "="*60)
    print("EJEMPLO 4: SILOGISMO DARII")
    print("="*60)
    print("Premisas:")
    print("  1. Todo M es P ([M]P)")
    print("  2. Algún S es M (<S>M)")
    print("Conclusión:")
    print("  Algún S es P (<S>P)")
    print()
    
    premise1 = parse("[M]P")
    premise2 = parse("<S>M")
    conclusion = parse("<S>P
