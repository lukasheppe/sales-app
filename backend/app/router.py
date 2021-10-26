from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import create_sale_in_db, get_number_of_sales, get_sales_volume, delete_sales_rows
from app.database import get_db
from app.models import BuyProductRequest, CreateSale, ProductType, SalesOverviewResponse, BuyProductResponse, DeleteSalesResponse

# Router to group sales endpoints
router = APIRouter()


def price_lookup(product_type: ProductType):
    """
    Utility function to lookup product prices.
    Starter = 500.0€
    Professional = 500.0€
    Enterprise = 500.0€

    :param product_type:
    :return: Price of the product in €
    """
    if product_type == product_type.STARTER:
        return 500.0
    elif product_type == product_type.PROFESSIONAL:
        return 1500.0
    elif product_type == product_type.ENTERPRISE:
        return 5000.0
    else:
        raise RuntimeError('Invalid enum value.')


@router.get('/get_current_money')
def get_current_money(db: Session = Depends(get_db)) -> SalesOverviewResponse:
    """
    Returns the total revenue as well as number of sales.
    :param db: sql alchemy session, provided via dependency injection
    :return: number of sales, total revenue
    """
    return SalesOverviewResponse(
        number_of_sales=get_number_of_sales(db),
        volume=get_sales_volume(db)
    )


@router.post('/buy_mpi/')
def buy_mpi(request: BuyProductRequest,
            db: Session = Depends(get_db)):
    """
    Endpoint to buy products. The request contains the product type.
    We lookup the price for the given id and create a new sale in the "sales" table of our database.
    A confirmation will be given to the user, indicating the price, date as well as a

    :param request: request containing the product type
    :param db: sql alchemy session, provided via dependency injection
    :return: confirmation response
    """

    # Lookup price
    product_price = price_lookup(request.product_type)

    # Write to database
    ret = create_sale_in_db(db, CreateSale(
        product=request.product_type,
        amount=product_price
    ))

    # Return response
    return BuyProductResponse(
        product_type=request.product_type,
        successful=ret is not None,
        price=product_price,
        buy_date=ret.date
    )


@router.delete('/sales')
def delete_sales(db: Session = Depends(get_db)):
    """
    Endpoint to delete all records of the "sales" table.
    :param db: sql alchemy session, provided via dependency injection
    :return: number of deleted rows.
    """
    num_rows_deleted = delete_sales_rows(db)
    return DeleteSalesResponse(num_rows_deleted=num_rows_deleted)
