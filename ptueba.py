query_companias = """
    SELECT DISTINCT c.expediente, c.nombre
    FROM bi_compania c
    JOIN bi_ranking r ON c.expediente = r.expediente
    WHERE r.anio = 2023 AND r.ciiu_n4 = 'C2910'
    ORDER BY c.nombre
"""
companias = pd.read_sql(query_companias, engine)
print(companias)