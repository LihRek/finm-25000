import time
import random

class Message:
    def __init__(self, sending_time: int,sequence_number: int):
        self.__sending_time = sending_time
        self.__sequence_number = sequence_number
    @property
    def sending_time(self):
        return self.__sending_time
    @sending_time.setter
    def sending_time(self, x):
        self.__sending_time = x
    @property
    def sequence_number(self):
        return self.__sequence_number
    @sequence_number.setter
    def sequence_number(self, x):
        self.__sequence_number = x

class AddModifyOrderMessage(Message):
    def __init__(self,sending_time,sequence_number,price:int,quantity:int,side:str,order_id:int):
        super().__init__(sending_time, sequence_number)
        self.__price = price
        self.__quantity = quantity
        self.__side = side
        self.__order_id = order_id
        
    @property
    def order_id(self):
        return self.__order_id
    @order_id.setter
    def order_id(self, x):
        self.__order_id = x
    @property
    def price(self):
        return self.__price
    @price.setter
    def price(self, x):
        self.__price = x
    @property
    def side(self):
        return self.__side
    @side.setter
    def side(self, x):
        self.__side = x
    @property
    def quantity(self):
        return self.__quantity
    @quantity.setter
    def quantity(self, x):
        self.__quantity = x

class DeleteOrderMessage(Message):
    def __init__(self,sending_time,sequence_number, side:str,order_id:int):
        super().__init__(sending_time, sequence_number)
        self.__side = side
        self.__order_id = order_id
    @property
    def order_id(self):
        return self.__order_id
    @order_id.setter
    def order_id(self, x):
        self.__order_id = x
    @property
    def side(self):
        return self.__side
    @side.setter
    def side(self, x):
        self.__side = x

class TradeMessage(Message):
    def __init__(self, sending_time, sequence_number, side:str,trade_id:int,trade_quantity:int):
        super().__init__(sending_time, sequence_number)
        self.__side = side
        self.trade_id = trade_id
        self.trade_quantity = trade_quantity
    @property
    def side(self):
        return self.__side
    @side.setter
    def side(self, x):
        self.__side = x
    @property
    def trade_id(self):
        return self.__trade_id
    @trade_id.setter
    def trade_id(self, x):
        self.__trade_id = x
    @property
    def trade_quantity(self):
        return self.__trade_quantity
    @trade_quantity.setter
    def trade_quantity(self, x):
        self.__trade_quantity = x       
import time
import random

def message_constructor_and_getters(checkDecorators):
    sending_time = time.time()
    sequence_number = random.randint(0, 50)

    message = Message(sending_time, sequence_number)

    if checkDecorators:
        assert(message.sending_time == sending_time)
        assert(message.sequence_number == sequence_number)

    else:
        assert(message.getSendingTime() == sending_time)
        assert(message.getSequenceNumber() == sequence_number)

def message_setters_and_getters(checkDecorators):
    message = Message(0, 0)

    sending_time = time.time()
    sequence_number = random.randint(0, 50)

    if checkDecorators:
        message.sending_time = sending_time
        message.sequence_number = sequence_number

        assert(message.sending_time == sending_time)
        assert(message.sequence_number == sequence_number)

    else:
        message.setSendingTime(sending_time)
        message.setSequenceNumber(sequence_number)

        assert(message.getSendingTime() == sending_time)
        assert(message.getSequenceNumber() == sequence_number)

def add_message_constructor_and_getters(checkDecorators):
    sending_time = time.time()
    sequence_number = random.randint(0, 50)
    price = random.randint(100, 200)
    quantity = random.randint(1, 10)
    side = random.choice(["Sell", "Buy"])
    order_id = random.randint(1000, 9999)

    message = AddModifyOrderMessage(sending_time, sequence_number, price, quantity, side, order_id)

    if checkDecorators:
        assert(message.sending_time == sending_time)
        assert(message.sequence_number == sequence_number)
        assert(message.price == price)
        assert(message.quantity == quantity)
        assert(message.side == side)
        assert(message.order_id == order_id)

    else:
        assert(message.getSendingTime() == sending_time)
        assert(message.getSequenceNumber() == sequence_number)
        assert(message.getPrice() == price)
        assert(message.getQuantity() == quantity)
        assert(message.getSide() == side)
        assert(message.getOrderId() == order_id)

def add_message_setters_and_getters(checkDecorators):
    message = AddModifyOrderMessage(0, 0, 0, 0, "", 0)

    sending_time = time.time()
    sequence_number = random.randint(0, 50)
    price = random.randint(100, 200)
    quantity = random.randint(1, 10)
    side = random.choice(["Sell", "Buy"])
    order_id = random.randint(1000, 9999)

    if checkDecorators:
        message.sending_time = sending_time
        message.sequence_number = sequence_number
        message.price = price
        message.quantity = quantity
        message.side = side
        message.order_id = order_id

        assert(message.sending_time == sending_time)
        assert(message.sequence_number == sequence_number)
        assert(message.price == price)
        assert(message.quantity == quantity)
        assert(message.side == side)
        assert(message.order_id == order_id)

    else:
        message.setSendingTime(sending_time)
        message.setSequenceNumber(sequence_number)
        message.setPrice(price)
        message.setQuantity(quantity)
        message.setSide(side)
        message.setOrderId(order_id)

        assert(message.getSendingTime() == sending_time)
        assert(message.getSequenceNumber() == sequence_number)
        assert(message.getPrice() == price)
        assert(message.getQuantity() == quantity)
        assert(message.getSide() == side)
        assert(message.getOrderId() == order_id)

def delete_message_constructor_and_getters(checkDecorators):
    sending_time = time.time()
    sequence_number = random.randint(0, 50)
    side = random.choice(["Sell", "Buy"])
    order_id = random.randint(1000, 9999)

    message = DeleteOrderMessage(sending_time, sequence_number, side, order_id)

    if checkDecorators:
        assert(message.sending_time == sending_time)
        assert(message.sequence_number == sequence_number)
        assert(message.side == side)
        assert(message.order_id == order_id)

    else:
        assert(message.getSendingTime() == sending_time)
        assert(message.getSequenceNumber() == sequence_number)
        assert(message.getSide() == side)
        assert(message.getOrderId() == order_id)

def delete_message_setters_and_getters(checkDecorators):
    message = DeleteOrderMessage(0, 0, "", 0)

    sending_time = time.time()
    sequence_number = random.randint(0, 50)
    side = random.choice(["Sell", "Buy"])
    order_id = random.randint(1000, 9999)

    if checkDecorators:
        message.sending_time = sending_time
        message.sequence_number = sequence_number
        message.side = side
        message.order_id = order_id

        assert(message.sending_time == sending_time)
        assert(message.sequence_number == sequence_number)
        assert(message.side == side)
        assert(message.order_id == order_id)

    else:
        message.setSendingTime(sending_time)
        message.setSequenceNumber(sequence_number)
        message.setSide(side)
        message.setOrderId(order_id)

        assert(message.getSendingTime() == sending_time)
        assert(message.getSequenceNumber() == sequence_number)
        assert(message.getSide() == side)
        assert(message.getOrderId() == order_id)

def trade_message_constructor_and_getters(checkDecorators):
    sending_time = time.time()
    sequence_number = random.randint(0, 50)
    side = random.choice(["Sell", "Buy"])
    trade_id = random.randint(1000, 9999)
    trade_quantity = random.randint(1, 10)

    message = TradeMessage(sending_time, sequence_number, side, trade_id, trade_quantity)

    if checkDecorators:
        assert(message.sending_time == sending_time)
        assert(message.sequence_number == sequence_number)
        assert(message.side == side)
        assert(message.trade_id == trade_id)
        assert(message.trade_quantity == trade_quantity)

    else:
        assert(message.getSendingTime() == sending_time)
        assert(message.getSequenceNumber() == sequence_number)
        assert(message.getSide() == side)
        assert(message.getTradeId() == trade_id)
        assert(message.getTradeQuantity() == trade_quantity)

def trade_message_setters_and_getters(checkDecorators):
    message = TradeMessage(0, 0, "", 0, 0)

    sending_time = time.time()
    sequence_number = random.randint(0, 50)
    side = random.choice(["Sell", "Buy"])
    trade_id = random.randint(1000, 9999)
    trade_quantity = random.randint(1, 10)

    if checkDecorators:
        message.sending_time = sending_time
        message.sequence_number = sequence_number
        message.side = side
        message.trade_id = trade_id
        message.trade_quantity = trade_quantity

        assert(message.sending_time == sending_time)
        assert(message.sequence_number == sequence_number)
        assert(message.side == side)
        assert(message.trade_id == trade_id)
        assert(message.trade_quantity == trade_quantity)

    else:
        message.setSendingTime(sending_time)
        message.setSequenceNumber(sequence_number)
        message.setSide(side)
        message.setTradeId(trade_id)
        message.setTradeQuantity(trade_quantity)

        assert(message.getSendingTime() == sending_time)
        assert(message.getSequenceNumber() == sequence_number)
        assert(message.getSide() == side)
        assert(message.getTradeId() == trade_id)
        assert(message.getTradeQuantity() == trade_quantity)

def inheritance_check():
    sending_time = time.time()
    sequence_number = random.randint(0, 50)
    price = random.randint(100, 200)
    quantity = random.randint(1, 10)
    side = random.choice(["Sell", "Buy"])
    order_trade_id = random.randint(1000, 9999)

    message1 = AddModifyOrderMessage(sending_time, sequence_number, price, quantity, side, order_trade_id)
    message2 = DeleteOrderMessage(sending_time, sequence_number, side, order_trade_id)
    message3 = TradeMessage(sending_time, sequence_number, side, order_trade_id, quantity)

    assert(issubclass(AddModifyOrderMessage, Message))
    assert(issubclass(DeleteOrderMessage, Message))
    assert(issubclass(TradeMessage, Message))

    assert(message1.__dict__ == {'_AddModifyOrderMessage__price': price, '_AddModifyOrderMessage__quantity': quantity, '_AddModifyOrderMessage__side': side, '_AddModifyOrderMessage__order_id': order_trade_id, '_Message__sending_time': sending_time, '_Message__sequence_number': sequence_number})
    assert(message2.__dict__ == {'_DeleteOrderMessage__side': side, '_DeleteOrderMessage__order_id': order_trade_id, '_Message__sending_time': sending_time, '_Message__sequence_number': sequence_number})
    assert(message3.__dict__ == {'_TradeMessage__side': side, '_TradeMessage__trade_id': order_trade_id, '_TradeMessage__trade_quantity': quantity, '_Message__sending_time': sending_time, '_Message__sequence_number': sequence_number})

def get_writeable_properties(cls):
    return [attr for attr, value in vars(cls).items()
                 if isinstance(value, property) and value.fset is not None]


def test1():
    props0 = get_writeable_properties(Message)
    assert(len(props0) == 0 or len(props0) == 2), "You must either use getter/setter methods or decorators, but not both"
    if len(props0) == 0:
        assert("getSendingTime" in dir(Message))
        assert("getSequenceNumber" in dir(Message))

        assert("setSendingTime" in dir(Message))
        assert("setSequenceNumber" in dir(Message))

def test2():
    props1 =  get_writeable_properties(AddModifyOrderMessage)
    assert(len(props1) == 0 or len(props1) == 4), "You must either use getter/setter methods or decorators, but not both"

    if len(props1) == 0:
        assert("getPrice" in dir(AddModifyOrderMessage))
        assert("getQuantity" in dir(AddModifyOrderMessage))
        assert("getSide" in dir(AddModifyOrderMessage))
        assert("getOrderId" in dir(AddModifyOrderMessage))

        assert("setPrice" in dir(AddModifyOrderMessage))
        assert("setQuantity" in dir(AddModifyOrderMessage))
        assert("setSide" in dir(AddModifyOrderMessage))
        assert("setOrderId" in dir(AddModifyOrderMessage))
    
def test3():
    props2 = get_writeable_properties(DeleteOrderMessage)
    assert(len(props2) == 0 or len(props2) == 2), "You must either use getter/setter methods or decorators, but not both"
    
    if len(props2) == 0:
        assert("getSide" in dir(DeleteOrderMessage))
        assert("getOrderId" in dir(DeleteOrderMessage))

        assert("setSide" in dir(DeleteOrderMessage))
        assert("setOrderId" in dir(DeleteOrderMessage))
    
def test4():
    props3 = get_writeable_properties(TradeMessage)
    assert(len(props3) == 0 or len(props3) == 3), "You must either use getter/setter methods or decorators, but not both"

    if len(props3) == 0:
        assert("getSide" in dir(TradeMessage))
        assert("getTradeId" in dir(TradeMessage))
        assert("getTradeQuantity" in dir(TradeMessage))

        assert("setSide" in dir(TradeMessage))
        assert("setTradeId" in dir(TradeMessage))
        assert("setTradeQuantity" in dir(TradeMessage))
    
def test5():
    props0 = get_writeable_properties(Message)
    checkDecorators0 = (len(props0) != 0)
    message_constructor_and_getters(checkDecorators0)
    
def test6():
    props0 = get_writeable_properties(Message)
    checkDecorators0 = (len(props0) != 0)
    message_setters_and_getters(checkDecorators0)

def test7():
    props1 = get_writeable_properties(AddModifyOrderMessage)
    assert(len(props1) == 0 or len(props1) == 4), "You must either use getter/setter methods or decorators, but not both"
    checkDecorators1 = (len(props1) != 0)
    add_message_constructor_and_getters(checkDecorators1)
    
def test8():
    props1 = get_writeable_properties(AddModifyOrderMessage)
    assert(len(props1) == 0 or len(props1) == 4), "You must either use getter/setter methods or decorators, but not both"
    checkDecorators1 = (len(props1) != 0)
    add_message_setters_and_getters(checkDecorators1)
 

def test9():
    props2 = get_writeable_properties(DeleteOrderMessage)
    assert(len(props2) == 0 or len(props2) == 2), "You must either use getter/setter methods or decorators, but not both"
    checkDecorators2 = (len(props2) != 0)
    delete_message_constructor_and_getters(checkDecorators2)

    
def test10():
    props2 = get_writeable_properties(DeleteOrderMessage)
    assert(len(props2) == 0 or len(props2) == 2), "You must either use getter/setter methods or decorators, but not both"
    checkDecorators2 = (len(props2) != 0)
    delete_message_setters_and_getters(checkDecorators2)

    
def test11():
    props3 = get_writeable_properties(TradeMessage)
    assert(len(props3) == 0 or len(props3) == 3), "You must either use getter/setter methods or decorators, but not both"
    checkDecorators3 = (len(props3) != 0)
    trade_message_constructor_and_getters(checkDecorators3) 

def test12():
    props3 = get_writeable_properties(TradeMessage)
    assert(len(props3) == 0 or len(props3) == 3), "You must either use getter/setter methods or decorators, but not both"
    checkDecorators3 = (len(props3) != 0)
    trade_message_setters_and_getters(checkDecorators3)
    
def test13():
    inheritance_check()
    
if __name__ == '__main__':
    func_name = input().strip()
    globals()[func_name]()
    
    


    
    
    
    
    
    

    
