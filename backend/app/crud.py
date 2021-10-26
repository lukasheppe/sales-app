from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import CreateSale, Sale


def delete_sales_rows(db: Session):
    """
    Delete all rows of the "sales" table.
    :param db: sql_alchemy session
    :return: number of deleted rows
    """
    try:
        num_rows_deleted = db.query(Sale).delete()
        db.commit()
    except:
        num_rows_deleted = 0
        db.rollback()
    return num_rows_deleted


def get_number_of_sales(db: Session):
    """
    Returns the row count the "sale" tables.
    :param db: sql_alchemy session
    :return: rows in the sale table
    """
    return db.query(Sale.amount).count()


def get_sales_volume(db: Session):
    """
    Returns the total sale volume in the "sale" table.
    :param db: sql_alchemy session
    :return: sum(sale.amount) in sale table
    """
    sales_volume = db.query(func.sum(Sale.amount).label('total_sales_volume')).scalar()
    if sales_volume is None:
        return 0.0

    return sales_volume


def create_sale_in_db(db: Session, create_sale: CreateSale):
    """
    Insert a new sale into the sale table.
    :param db: sql_alchemy session
    :param create_sale: object representation for row
    :return:
    """

    # Create sale database representation
    db_sale = Sale(product=create_sale.product,
                   date=create_sale.created,
                   amount=create_sale.amount)
    # Add object to database
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale
