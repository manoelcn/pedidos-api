from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session
from models import Order
from schemas import OrderSchema

order_router = APIRouter(prefix='/orders', tags=['order'])

@order_router.get('/')
async def orders():
    return {'message': 'orders'}


@order_router.post('/create')
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user=order_schema.user_id)
    session.add(new_order)
    session.commit()
    return {'message': f'Order {new_order.id} created successfully'}
