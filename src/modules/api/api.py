from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.model import Product
from modules.api.methods import get_async_session
from modules.api.schemes import ProductModel, NewProduct, UpdateProduct

app = FastAPI()


@app.post("/products", status_code=201)
async def create_product(product: NewProduct, session: Annotated[AsyncSession, Depends(get_async_session)]):
    request = (
        insert(Product)
        .values(
            slug=product.url.removeprefix('https://www.maxidom.ru/catalog/').removesuffix('/'),
            name=product.name,
            price=product.price
        )
    )

    response = await session.execute(
        request
        .on_conflict_do_update(
            index_elements=[Product.slug],
            set_=dict(name=request.excluded.name, price=request.excluded.price)
        )
        .returning(Product.id)
    )
    await session.commit()

    return {"message": "Продукт добавлен", "id": response.first()[0]}


@app.get("/products")
async def get_products(session: Annotated[AsyncSession, Depends(get_async_session)]):
    response = await session.execute(
        select(Product.id, Product.slug, Product.name, Product.price)
        .order_by(Product.name)
    )

    return [
        ProductModel(
            id=product_id,
            name=name,
            price=price,
            url=f'https://www.maxidom.ru/catalog/{slug}/'
        ) for product_id, slug, name, price in response.all()
    ]


@app.delete("/products")
async def delete_products(session: Annotated[AsyncSession, Depends(get_async_session)]):
    await session.execute(delete(Product))
    await session.commit()

    return {"message": "Все данные удалены"}


@app.get("/products/{product_id}")
async def get_product(product_id: int, session: Annotated[AsyncSession, Depends(get_async_session)]):
    response = await session.execute(
        select(Product.id, Product.slug, Product.name, Product.price)
        .where(product_id == Product.id)
    )

    result = response.first()

    if not result:
        return {"message": "Продукт не найден"}

    return ProductModel(
        id=result[0],
        name=result[2],
        price=result[3],
        url=f'https://www.maxidom.ru/catalog/{result[1]}/'
    )


@app.put("/products/{product_id}")
async def update_product(
    product_id: int,
    product: UpdateProduct,
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    response = await session.execute(
        select(Product.id, Product.slug, Product.name, Product.price)
        .where(product_id == Product.id)
    )

    result = response.first()

    if not result:
        return {"message": "Продукт не найден"}

    await session.execute(
        update(Product)
        .values(
            slug=product.url.removeprefix('https://www.maxidom.ru/catalog/').removesuffix('/') if product.url else result[1],
            name=product.name or result[2],
            price=product.price or result[3]
        )
        .where(product_id == Product.id)
    )
    await session.commit()

    return {"message": "Продукт обновлен", "id": product_id}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int, session: Annotated[AsyncSession, Depends(get_async_session)]):
    response = await session.execute(
        select(Product.id)
        .where(product_id == Product.id)
    )

    if not response.first():
        return {"message": "Продукт не найден"}

    await session.execute(delete(Product).where(product_id == Product.id))
    await session.commit()

    return {"message": "Продукт удален"}
