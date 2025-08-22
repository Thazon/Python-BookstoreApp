from services.crud.crud_service import crud

name = "exchange_rates"

create = """INSERT INTO exchange_rates (currency_from, currency_to, rate, last_updated)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (currency_from, currency_to)
            DO UPDATE SET rate = EXCLUDED.rate, last_updated = CURRENT_TIMESTAMP;"""

read_all = """SELECT id, currency_from, currency_to, rate, last_updated
              FROM exchange_rates;"""

read_one = """SELECT id, currency_from, currency_to, rate, last_updated
              FROM exchange_rates
              WHERE id = %s;"""

read_one_pair = """SELECT id, currency_from, currency_to, rate, last_updated
                   FROM exchange_rates
                   WHERE currency_from = %s AND currency_to = %s;"""

read_last_updated ="""SELECT MIN(last_updated)
                FROM exchange_rates;"""

update_select = """SELECT currency_from, currency_to, rate
                   FROM exchange_rates
                   WHERE id = %s;"""

update = """UPDATE exchange_rates
            SET currency_from = %s, currency_to = %s, rate = %s, last_updated = CURRENT_TIMESTAMP
            WHERE id = %s;"""

delete = """DELETE FROM exchange_rates
            WHERE id = %s;"""

def create_exchange_rate(currency_from, currency_to, rate) -> bool:
    return crud("create", create, name, (currency_from, currency_to, rate))

def read_all_exchange_rates():
    return crud("read_all", read_all, name)

def read_exchange_rate(rate_id):
    return crud("read_one", read_one, name, (rate_id,))

def read_exchange_rate_pair(currency_from, currency_to):
    return crud("read_one", read_one_pair, name, (currency_from, currency_to))

def read_last_updated_exchange_rate():
    return crud("read_last_updated", read_one, name)

def update_exchange_rate(currency_from, currency_to, rate, rate_id) -> bool:
    return crud("update", update, name, (currency_from, currency_to, rate, rate_id), update_select)

def delete_exchange_rate(rate_id) -> bool:
    return crud("delete", delete, name, (rate_id,))
