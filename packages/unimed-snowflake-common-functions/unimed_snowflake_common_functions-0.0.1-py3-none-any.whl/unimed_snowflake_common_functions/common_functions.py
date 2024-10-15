def execute_and_return(sql, session):
    result_sql = session.sql(sql).collect()

    return result_sql[0][0]

def execute_and_log(sql, procedure_name, database_name, schema_name, session):

    print(f"Executing {procedure_name}")
    
    result_sql = session.sql(sql)
    # Get the query ID (equivalent of getQueryId in JS)
    query_id = session.sql("select last_query_id()").collect()[0][0]

    column_name = result_sql.schema.names[0]  # Name of the first column

    # Collect the result set
    result_rows = result_sql.collect()

    if result_rows:
        column_value = result_rows[0][0]  # Value of the first column
        
        # Prepare the result message similar to JavaScript example
        step_result = f"{column_name}: {column_value}"
    else:
        step_result = "No result returned"
    
    # Log the step output in the audit table
    session.sql(f"""
        INSERT INTO {database_name}.{schema_name}.audit_table (procedure_name, sql_step, step_result, audit_timestamp)
        VALUES ('{procedure_name}', '{query_id}', '{step_result}', CURRENT_TIMESTAMP)
    """).collect()

def log_error(err, procedure_name, errordate, database_name, schema_name, session):

    print(f"Executing log_error -> {procedure_name}")

    import json

    if err.error_code is None:
        err.error_code = 0
    
    result = session.sql(f"""
        INSERT INTO {database_name}.{schema_name}.ERROR_TABLE 
        (
            PROCEDURE_NAME,
            ERROR_CODE,
            ERROR_MESSAGE,
            ERROR_TIMESTAMP
        )
        VALUES (
            ?, ?, ?, ?
        )
    """, 
        params=[procedure_name, int(err.error_code), err.message, errordate]
        ).collect()

    print(f"log_error result: {result}")

    error_entry = {
        "PROCEDURE_NAME" : {procedure_name},
        "ERROR_CODE" : {int(err.error_code)},
        "ERROR_MESSAGE" : {err.message},
        "ERROR_TIMESTAMP" : {errordate}
    }

    print(json.dumps(error_entry, indent=1, default=str))

    # error_entry = session.sql(f"""
    #     SELECT * FROM {database_name}.{schema_name}.ERROR_TABLE
    #     WHERE PROCEDURE_NAME = ?
    #     AND ERROR_CODE = ?
    #     AND ERROR_MESSAGE = ?
    #     AND ERROR_TIMESTAMP = ?
    # """, 
    #     params=[procedure_name, int(err.error_code), err.message, errordate]
    #     ).collect()

    # print(error_entry)

    return error_entry