from fastapi import APIRouter,status,HTTPException,Depends
from schemas import OrderModel,LoginModel,OrderModelUpdate
from db.database import Session,engine,Base
from models import User,Order
import utils.oauth2 as oauth2
import json
from sqlalchemy import delete

from fastapi.encoders import jsonable_encoder
order_router = APIRouter(
    prefix="/order",
    tags = ["ORDERS"]
)

session = Session(bind= engine)

@order_router.post("/placeorder",status_code=status.HTTP_200_OK)
async def place_order(request : OrderModel,current_user : LoginModel = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()


    new_order = Order(
        quantity = request.quantity,
        pizza_size = request.pizza_size,
    )

    new_order.user = user
  
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    response = {
        "Pizza Quantity" : new_order.quantity,
        "Pizza Size" : new_order.pizza_size,
        "Id" : new_order.id,
        "Order Status" : new_order.order_status
    }

    return jsonable_encoder(response)


@order_router.get("/allorders",status_code=status.HTTP_201_CREATED)
def show_all_orders(current_user : LoginModel = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()
    
    if user.is_staff:
        orders = session.query(Order).all()
        return jsonable_encoder(orders)
    else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@order_router.get("/allorders/{order_id}",status_code=status.HTTP_201_CREATED)
def show_order_by_id(order_id,current_user : LoginModel = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()
    
    if user.is_staff:
        orders = session.query(Order).filter(Order.id == order_id).first()
        return jsonable_encoder(orders)
    else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You are not a SUPERUSER !!!")

@order_router.get("/user",status_code=status.HTTP_201_CREATED)
def user_orders(current_user : LoginModel = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()
    if user :
        return jsonable_encoder(user.orders)
    else :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@order_router.get("/update/{order_id}",status_code=status.HTTP_201_CREATED)
def update_order_by_id(order_id,request :OrderModel,current_user : LoginModel = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()

    if user:
        orders = session.query(Order).filter(Order.id == order_id).first()

        
        orders.quantity = request.quantity
        orders.pizza_size = request.pizza_size

        session.commit()

        res = {
            "Order Updated":{
            "Order Quantity" : orders.quantity,
            "Pizza Size" : orders.pizza_size
        }
        }

        return jsonable_encoder(res)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)



        

@order_router.patch("/orderstatus/{order_id}",status_code=status.HTTP_201_CREATED)
def update_order_status_by_id(order_id,request : OrderModelUpdate,current_user : LoginModel = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()
    
    if user.is_staff:
        order_to_update = session.query(Order).filter(Order.id == order_id).first()

        order_to_update.order_status = request.order_status
        session.commit()

        res = {"Order Status" : request.order_status}
        return jsonable_encoder(res)
    else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You are not a SUPERUSER !!!")

@order_router.delete("/delete/{order_id}",status_code=status.HTTP_201_CREATED)
def delete_order_by_id(order_id,current_user : LoginModel = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()
    
    # order_to_delete = session.query(Order).filter(Order.id == id).first()
    if user:
        order_to_delete = session.query(Order).filter(Order.id == order_id).first()
        session.delete(order_to_delete)
        session.commit()

        res = {"Order":"Deleted"}
        return jsonable_encoder(res)
    


