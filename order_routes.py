from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from models import Order, User, Item
from schemas import OrderSchema, ItemSchema

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


@order_router.post('/finalize/{order_id}')
async def finalize_order(order_id: int, session: Session = Depends(get_session)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail='order not found')
    order.status = 'FINALIZADO'
    session.commit()
    return {
        'message': f'Order {order.id} finalized',
        'order_status': order.status
    }


@order_router.get('/list')
async def list_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if not user.admin:
        raise HTTPException(status_code=401, detail='you dont have permission')
    else:
        orders = session.query(Order).all()
        return {
            'orders': orders
        }


@order_router.get('/{order_id}/detail')
async def detail_order(order_id: int, session: Session = Depends(get_session)):
    order = session.query(Order).filter(Order.id==order_id).first()
    order.items
    if not order:
        raise HTTPException(status_code=400, detail='order not found')
    return {
        'order': order
    }


@order_router.post('/{order_id}/add/item')
async def add_item_to_order(order_id: int, item_schema: ItemSchema, session: Session = Depends(get_session)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail='order not found')
    item = Item(item_schema.quantity, item_schema.flavor, item_schema.size, item_schema.unit_price, order_id)
    session.add(item)
    order.calculate_price()
    session.commit()
    return {
        'message': 'item created successfully',
        'item_id': item.id,
        'order_price': order.price
    }


@order_router.post('/{order_id}/remove/item/{item_id}')
async def remove_item_to_order(order_id: int, item_id: int, session: Session = Depends(get_session)):
    item = session.query(Item).filter(Item.id==item_id).first()
    order = session.query(Order).filter(Order.id==item.order).first()
    if not order:
        raise HTTPException(status_code=400, detail='order not found')
    session.delete(item)
    order.calculate_price()
    session.commit()
    return {
        'message': 'item successfully removed',
        'quantity_items_order': len(order.items),
        'order': order
    }
