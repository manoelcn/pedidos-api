from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from models import Order, User
from schemas import OrderSchema

order_router = APIRouter(prefix='/orders', tags=['order'], dependencies=[Depends(verify_token)])

@order_router.get('/')
async def orders():
    return {'message': 'orders'}


@order_router.post('/create')
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user=order_schema.user_id)
    session.add(new_order)
    session.commit()
    return {'message': f'Order {new_order.id} created successfully'}


@order_router.post('/cancel/{order_id}')
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail='order not found')
    if not user.admin and user.id != order.id:
        raise HTTPException(status_code=401, detail='you dont have permission')
    order.status = 'CANCELADO'
    session.commit()
    return {
        'message': f'Order {order.id} cancelled',
        'order': order
    }
