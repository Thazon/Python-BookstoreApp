from db.connection import get_connection

#This function is used to manage the CRUD functionality of the program.
def crud(instruction_type, sql, name, parameters=None, update_select=None):
    #It has only a couple defined allowed types. If the type doesn't match, it immediately returns False.
    allowed_types = {"create", "read_one", "read_all", "update", "delete"}
    if instruction_type not in allowed_types:
        print(f"Invalid CRUD type: {instruction_type}!")
        return False

    #Once CRUD type validation is complete, it accesses the database and sends the SQL command alongside the necessary
    #parameters.
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:

                #If CRUD type is update, it first replaces any parameters left blank with the original row's.
                if instruction_type == "update":
                    existing = crud("read_one", update_select, name, (parameters[-1],))

                    #If no row is found, it immediately returns False.
                    if existing is None:
                        print(f"No details found for {name} ID {parameters[-1]}!")
                        return False

                    #The parameters are stored as tuple which is immutable. So we change it to a list first.
                    parameters = list(parameters)

                    #For every parameter in the existing row, it checks if the new one is None and, if so, replaces it.
                    for i in range(len(existing)):
                        if not parameters[i]:
                            parameters[i] = existing[i]

                    #It then casts the parameters back into a tuple.
                    parameters = tuple(parameters)

                cur.execute(sql, parameters or ())

                #If CRUD type is create, it commits the insertion, prints success and then returns True.
                if instruction_type == "create":
                    conn.commit()
                    print(f"Row successfully inserted in {name}!")
                    return True

                #If CRUD type is read_one, it returns the one row read or None if nothing was found.
                elif instruction_type == "read_one":
                    return cur.fetchone()

                #If CRUD type is read_all, it returns all the rows read or None if none were found.
                elif instruction_type == "read_all":
                    return cur.fetchall()

                #If CRUD type is update, it commits and then returns True if anything got changed or False if nothing.
                elif instruction_type == "update":
                    conn.commit()
                    return cur.rowcount > 0

                #If CRUD type is delete, it attempts the deletion, returns False if it fails or True if succeeds.
                elif instruction_type == "delete":
                    if cur.rowcount == 0:
                        print(f"No {name} found to delete.")
                        return False
                    conn.commit()
                    print(f"{name} deletion successful.")
                    return True

    #If at any point it encounters an exception, it logs all the information to the console and returns False.
    except Exception as e:
        print(f"Error during {instruction_type} on {name}: {e}!")
        if "read" in instruction_type:
            return None
        return False