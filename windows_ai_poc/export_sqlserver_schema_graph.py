import pyodbc
import os
from graphviz import Digraph

def connect_to_sqlserver(server, database, username=None, password=None, trusted_connection=False):
    """连接到SQL Server数据库"""
    if trusted_connection:
        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    else:
        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    return pyodbc.connect(connection_string)

def get_schema_info(conn):
    """获取数据库所有模式信息"""
    cursor = conn.cursor()
    cursor.execute("""
    SELECT SCHEMA_NAME, SCHEMA_ID FROM sys.schemas
    ORDER BY SCHEMA_NAME
    """)
    schemas = cursor.fetchall()
    cursor.close()
    return schemas

def get_tables_info(conn):
    """获取所有表的信息"""
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        t.name AS table_name,
        s.name AS schema_name,
        t.object_id
    FROM 
        sys.tables t
    JOIN 
        sys.schemas s ON t.schema_id = s.schema_id
    ORDER BY 
        s.name, t.name
    """)
    tables = cursor.fetchall()
    cursor.close()
    return tables

def get_columns_info(conn, table_object_id):
    """获取特定表的列信息"""
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        c.name AS column_name,
        t.name AS data_type,
        c.max_length,
        c.precision,
        c.scale,
        c.is_nullable,
        c.is_identity,
        c.column_id,
        CASE WHEN pk.column_id IS NOT NULL THEN 1 ELSE 0 END AS is_primary_key
    FROM 
        sys.columns c
    JOIN 
        sys.types t ON c.user_type_id = t.user_type_id
    LEFT JOIN 
        (SELECT ic.column_id, ic.object_id
         FROM sys.index_columns ic
         JOIN sys.indexes i ON ic.object_id = i.object_id AND ic.index_id = i.index_id
         WHERE i.is_primary_key = 1) pk 
        ON pk.column_id = c.column_id AND pk.object_id = c.object_id
    WHERE 
        c.object_id = ?
    ORDER BY 
        c.column_id
    """, table_object_id)
    columns = cursor.fetchall()
    cursor.close()
    return columns

def get_foreign_keys(conn):
    """获取所有外键关系信息"""
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        fk.name AS fk_name,
        tp.name AS parent_table,
        cp.name AS parent_column,
        ps.name AS parent_schema,
        tr.name AS referenced_table,
        cr.name AS referenced_column,
        rs.name AS referenced_schema
    FROM 
        sys.foreign_keys fk
    INNER JOIN 
        sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
    INNER JOIN 
        sys.tables tp ON fkc.parent_object_id = tp.object_id
    INNER JOIN 
        sys.columns cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
    INNER JOIN 
        sys.schemas ps ON tp.schema_id = ps.schema_id
    INNER JOIN 
        sys.tables tr ON fkc.referenced_object_id = tr.object_id
    INNER JOIN 
        sys.columns cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id
    INNER JOIN 
        sys.schemas rs ON tr.schema_id = rs.schema_id
    ORDER BY 
        tp.name, tr.name
    """)
    foreign_keys = cursor.fetchall()
    cursor.close()
    return foreign_keys

def export_schema_to_file(schemas, tables, table_columns, foreign_keys, output_dir):
    """导出数据库结构信息到文本文件"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(os.path.join(output_dir, "schema_info.txt"), "w", encoding="utf-8") as f:
        f.write("数据库Schema信息:\n")
        f.write("=" * 50 + "\n")
        for schema in schemas:
            f.write(f"Schema名: {schema.SCHEMA_NAME}, ID: {schema.SCHEMA_ID}\n")
        f.write("\n\n")

        f.write("表信息:\n")
        f.write("=" * 50 + "\n")
        for table in tables:
            f.write(f"表名: {table.schema_name}.{table.table_name}\n")
            f.write("-" * 30 + "\n")
            columns = table_columns.get((table.schema_name, table.table_name), [])
            for col in columns:
                pk_indicator = "PK" if col.is_primary_key else ""
                nullable = "NULL" if col.is_nullable else "NOT NULL"
                identity = "IDENTITY" if col.is_identity else ""
                data_type = col.data_type
                
                # 处理特定类型的长度、精度和小数位数
                if col.data_type in ('nvarchar', 'varchar', 'char', 'nchar'):
                    if col.max_length == -1:
                        data_type += "(MAX)"
                    else:
                        length = col.max_length
                        if col.data_type.startswith('n'):  # Unicode类型
                            length = length // 2
                        data_type += f"({length})"
                elif col.data_type in ('decimal', 'numeric'):
                    data_type += f"({col.precision}, {col.scale})"
                
                f.write(f"  {col.column_name} {data_type} {nullable} {identity} {pk_indicator}\n")
            f.write("\n")

        f.write("外键关系:\n")
        f.write("=" * 50 + "\n")
        for fk in foreign_keys:
            f.write(f"外键名: {fk.fk_name}\n")
            f.write(f"  {fk.parent_schema}.{fk.parent_table}.{fk.parent_column} -> {fk.referenced_schema}.{fk.referenced_table}.{fk.referenced_column}\n")
            f.write("\n")

def generate_graphviz(tables, foreign_keys, output_dir):
    """生成表关系的GraphViz图"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 创建有向图
    dot = Digraph(comment='数据库表关系图', format='png')
    dot.attr('graph', rankdir='LR', size='10,10', ratio='fill')
    dot.attr('node', shape='record', style='filled', fillcolor='lightblue')
    
    # 添加表节点
    for table in tables:
        table_id = f"{table.schema_name}.{table.table_name}"
        dot.node(table_id, f"{table_id}")
    
    # 添加外键关系
    for fk in foreign_keys:
        parent_id = f"{fk.parent_schema}.{fk.parent_table}"
        referenced_id = f"{fk.referenced_schema}.{fk.referenced_table}"
        dot.edge(parent_id, referenced_id, 
                 label=f"{fk.parent_column} -> {fk.referenced_column}",
                 fontsize='10')
    
    # 保存和渲染图
    dot_file = os.path.join(output_dir, "db_relationships")
    dot.render(dot_file, view=True)
    print(f"GraphViz图已生成: {dot_file}.png")

def main():
    # 数据库连接参数
    server = input("请输入SQL Server名称: ")
    database = input("请输入数据库名称: ")
    auth_choice = input("使用Windows身份验证? (y/n): ").lower()
    
    if auth_choice == 'y':
        conn = connect_to_sqlserver(server, database, trusted_connection=True)
    else:
        username = input("请输入用户名: ")
        password = input("请输入密码: ")
        conn = connect_to_sqlserver(server, database, username, password)
    
    try:
        print("正在连接到数据库...")
        
        # 获取数据库结构信息
        print("提取Schema信息...")
        schemas = get_schema_info(conn)
        
        print("提取表信息...")
        tables = get_tables_info(conn)
        
        print("提取列信息...")
        table_columns = {}
        for table in tables:
            columns = get_columns_info(conn, table.object_id)
            table_columns[(table.schema_name, table.table_name)] = columns
        
        print("提取外键关系...")
        foreign_keys = get_foreign_keys(conn)
        
        # 导出信息到文件
        output_dir = "db_schema_export"
        print(f"导出Schema信息到{output_dir}目录...")
        export_schema_to_file(schemas, tables, table_columns, foreign_keys, output_dir)
        
        # 生成GraphViz图
        print("生成表关系GraphViz图...")
        generate_graphviz(tables, foreign_keys, output_dir)
        
        print("操作完成!")
        
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        conn.close()
        print("数据库连接已关闭")

if __name__ == "__main__":
    main()

