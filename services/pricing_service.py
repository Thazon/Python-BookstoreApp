from services.crud.book_discount_service import read_all_current_discounts_for_book
from services.crud.book_service import read_price_book
from services.crud.genre_discount_service import read_all_current_genre_book_discounts

#Apply a discount to the given price.
def apply_discount(price, discount):
    discount_type = discount[2]  # "fixed" or "percent"
    value = discount[3]

    if discount_type == "fixed":
        return max(price - value, 0)
    elif discount_type == "percent":
        return max(price * (1 - value / 100), 0)
    return price

#Calculate final price of a book after applying active discounts.
def get_final_price(book_id):
    # get base price
    book = read_price_book(book_id)
    if not book:
        print(f"Book {book_id} not found.")
        return None

    base_price = book[0]
    final_price = base_price

    # fetch book-specific discounts
    book_discounts = read_all_current_discounts_for_book(book_id) or []
    # fetch genre-level discounts
    genre_discounts = read_all_current_genre_book_discounts(book_id) or []

    # merge both
    all_discounts = book_discounts + genre_discounts

    # apply them one by one
    for discount in all_discounts:
        final_price = apply_discount(final_price, discount)

    return round(final_price, 2)
