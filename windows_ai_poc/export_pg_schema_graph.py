#!/usr/bin/env python
import psycopg2
import graphviz
import os
from psycopg2 import sql

def connect_to_postgres(dbname, user, password, host, port):
    """Connect to PostgreSQL database and return connection object."""
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Successfully connected to PostgreSQL database.")
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None

def get_schema_info(conn):
    """Get schema information from the database."""
    schemas = {}
    
    with conn.cursor() as cursor:
        # Get all schemas
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
            ORDER BY schema_name
        """)
        schema_rows = cursor.fetchall()
        
        for schema_row in schema_rows:
            schema_name = schema_row[0]
            schemas[schema_name] = {'tables': {}}
            
            # Get tables in this schema
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = %s
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """, (schema_name,))
            
            table_rows = cursor.fetchall()
            
            for table_row in table_rows:
                table_name = table_row[0]
                schemas[schema_name]['tables'][table_name] = {'columns': [], 'foreign_keys': []}
                
                # Get columns for this table
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default 
                    FROM information_schema.columns 
                    WHERE table_schema = %s AND table_name = %s
                    ORDER BY ordinal_position
                """, (schema_name, table_name))
                
                column_rows = cursor.fetchall()
                for column_row in column_rows:
                    column_name, data_type, is_nullable, column_default = column_row
                    schemas[schema_name]['tables'][table_name]['columns'].append({
                        'name': column_name,
                        'type': data_type,
                        'nullable': is_nullable,
                        'default': column_default
                    })
                
                # Get primary key info
                cursor.execute("""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu 
                        ON tc.constraint_name = kcu.constraint_name 
                        AND tc.table_schema = kcu.table_schema
                    WHERE tc.constraint_type = 'PRIMARY KEY' 
                        AND tc.table_schema = %s
                        AND tc.table_name = %s
                    ORDER BY kcu.ordinal_position
                """, (schema_name, table_name))
                
                pk_rows = cursor.fetchall()
                pk_columns = [row[0] for row in pk_rows]
                
                for column in schemas[schema_name]['tables'][table_name]['columns']:
                    if column['name'] in pk_columns:
                        column['primary_key'] = True
                    else:
                        column['primary_key'] = False
                
                # Get foreign key info
                cursor.execute("""
                    SELECT 
                        kcu.column_name,
                        ccu.table_schema AS foreign_table_schema,
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        AND tc.constraint_schema = kcu.constraint_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                        AND ccu.constraint_schema = tc.constraint_schema
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                        AND tc.table_schema = %s
                        AND tc.table_name = %s
                """, (schema_name, table_name))
                
                fk_rows = cursor.fetchall()
                for fk_row in fk_rows:
                    column, fk_schema, fk_table, fk_column = fk_row
                    schemas[schema_name]['tables'][table_name]['foreign_keys'].append({
                        'column': column,
                        'references': {
                            'schema': fk_schema,
                            'table': fk_table,
                            'column': fk_column
                        }
                    })
    
    return schemas

def export_schema_to_text(schemas, output_file):
    """Export database schema to a text file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for schema_name, schema_data in schemas.items():
            f.write(f"Schema: {schema_name}\n")
            f.write("=" * 80 + "\n\n")
            
            for table_name, table_data in schema_data['tables'].items():
                f.write(f"Table: {schema_name}.{table_name}\n")
                f.write("-" * 80 + "\n")
                
                # Write columns
                f.write("Columns:\n")
                for column in table_data['columns']:
                    pk_marker = "PK" if column.get('primary_key', False) else "  "
                    nullable = "NULL" if column['nullable'] == "YES" else "NOT NULL"
                    default = f" DEFAULT {column['default']}" if column['default'] else ""
                    f.write(f"  [{pk_marker}] {column['name']} {column['type']} {nullable}{default}\n")
                
                # Write foreign keys
                if table_data['foreign_keys']:
                    f.write("\nForeign Keys:\n")
                    for fk in table_data['foreign_keys']:
                        f.write(f"  {fk['column']} -> {fk['references']['schema']}.{fk['references']['table']}.{fk['references']['column']}\n")
                
                f.write("\n")
    
    print(f"Schema exported to {output_file}")

def create_graphviz_diagram(schemas, output_file):
    """Generate a Graphviz diagram of the database schema."""
    dot = graphviz.Digraph(comment='Database Schema', format='png')
    dot.attr('graph', rankdir='LR', splines='ortho')
    dot.attr('node', shape='record', fontsize='10')
    
    # Add tables as nodes
    for schema_name, schema_data in schemas.items():
        for table_name, table_data in schema_data['tables'].items():
            table_label = f"{table_name}|"
            
            # Add columns to the table label
            columns_text = []
            for column in table_data['columns']:
                pk_marker = "🔑 " if column.get('primary_key', False) else ""
                columns_text.append(f"{pk_marker}{column['name']}: {column['type']}")
            
            table_label += "\\l".join(columns_text) + "\\l"
            
            # Create a node for the table
            node_id = f"{schema_name}_{table_name}"
            dot.node(node_id, f"{{{table_label}}}")
    
    # Add relationships as edges
    for schema_name, schema_data in schemas.items():
        for table_name, table_data in schema_data['tables'].items():
            for fk in table_data['foreign_keys']:
                from_node = f"{schema_name}_{table_name}"
                to_node = f"{fk['references']['schema']}_{fk['references']['table']}"
                dot.edge(from_node, to_node, label=f"  {fk['column']} -> {fk['references']['column']}  ", fontsize='8')
    
    # Save the diagram
    dot.render(output_file, cleanup=True)
    print(f"Graphviz diagram saved to {output_file}.png")

def main():
    # Database connection parameters
    db_params = {
        "dbname": "hulunotepro",
        "user": "postgrest",
        "password": "123456",
        "host": "localhost",
        "port": 5432
    }
    
    # Connect to the database
    conn = connect_to_postgres(**db_params)
    if not conn:
        return
    
    try:
        # Get schema information
        schemas = get_schema_info(conn)
        
        # Export schema to text file
        export_schema_to_text(schemas, "database_schema.txt")
        
        # Create Graphviz diagram
        create_graphviz_diagram(schemas, "database_diagram")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()

