TABLE_PROBLEM_CATEGORIES = "problem_categories"

# Lista todas as categorias de problemas cadastradas, incluindo o nome,
# a descrição detalhada e o nível de complexidade base para triagem.
LIST_PROBLEM_CATEGORIES_SQL = f"""
    SELECT id, name, descript as description, base_complexity FROM problem_categories
"""

# Obtém o nível de competência técnica (required_level) exigido para
# atender um chamado de uma categoria específica.
SHOW_PROBLEM_CATE_SPECIFY_SQL = f"""
SELECT required_level FROM problem_categories WHERE id = (%s)
"""
