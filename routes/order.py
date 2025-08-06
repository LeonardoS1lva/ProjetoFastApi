from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas.schemas import OrderSchema, OrderItemSchema, ResponseOrderSchema
from models.models import Order, User, OrderItem
from typing import List

order_router = APIRouter(prefix="/orders", tags=["Orders"], dependencies=[Depends(verify_token)])

@order_router.get("/")
async def orders():
    """
    This route returns a list of orders.
    """
    return {"message": "You accessed the orders route"}

@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user=order_schema.id_user)
    session.add(new_order)
    session.commit()
    return { "message": f"Order created. Order ID: {new_order.id}"}

@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):

    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You don't have permissions to cancel this order")
    order.status = "CANCELLED"
    session.commit()
    return {
        "message": f"Order numeber: {order_id} canceled with successful"
    }
    
@order_router.get("/list")
async def list_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if not user.admin:
        raise  HTTPException(status_code=401, detail="You don't have permissions to view this list")
    else:
        orders = session.query(Order).all()
        return {
            "orders": orders
        }

@order_router.post("/order/add/{order_id}")
async def add_order_item(order_id: int, 
                         order_item_schema: OrderItemSchema, 
                         session: Session = Depends(get_session), 
                         user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You don't have permissions")
    order_item = OrderItem(order_item_schema.count, 
                           order_item_schema.flavor, 
                           order_item_schema.size, 
                           order_item_schema.unit_price,
                           order_id)
    session.add(order_item)
    order.calc_price()
    session.commit()
    return {
        "message": "Created item with successful",
        "item_id": order_item.id,
        "order_price": order.price
    }

@order_router.post("/order/remove/{item_order_id}")
async def remove_order_item(item_order_id: int,
                         session: Session = Depends(get_session), 
                         user: User = Depends(verify_token)):
    item_order = session.query(OrderItem).filter(OrderItem.id==item_order_id).first()
    order = session.query(Order).filter(Order.id==item_order.order).first()
    if not item_order:
        raise HTTPException(status_code=400, detail="Order Item not found")
    if not user.admin and user.id != item_order.order.user:
        raise HTTPException(status_code=401, detail="You don't have permissions")
    session.delete(item_order)
    order.calc_price()
    session.commit()
    return {
        "message": "Removed item with successful",
        "order": item_order.order
    }

@order_router.post("/order/finish/{order_id}")
async def finish_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You don't have permissions to access this order")
    order.status = "COMPLETED"
    session.commit()
    return {
        "message": f"Order numeber: {order_id} finalized with successful"
    }

@order_router.get("/order/{order_id}")
async def order_view(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You don't have permissions to view this order")
    return {
        "order_items_count": len(order.items),
        "order": order
    }

@order_router.get("/list/orders-user", response_model=List[ResponseOrderSchema])
async def list_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    orders = session.query(Order).filter(Order.user==user.id).all()
    return orders
    