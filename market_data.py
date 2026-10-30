from ib_async import IB,Stock
from secrets import randbelow
import asyncio
import math
async def get_stock_quote(symbol):
    ib=IB()
    stock=Stock(symbol,'SMART','USD')
    client_id= 50000+ randbelow(40000)
    try:
        await ib.client.connectAsync(
            '127.0.0.1',
            4002,
            clientId=client_id,
            timeout=8
        )
        contracts= await ib.qualifyContractsAsync(stock)
        if not contracts or contracts[0] is None:
            raise ValueError(f'stock not found: {symbol}')
        qualifed_stock= contracts[0]
        ib.reqMarketDataType(3)
        ticker= ib.reqMktData(qualifed_stock)
        async with asyncio.timeout(10):
            while not math.isfinite(ticker.last):
                await ticker.updateEvent
        return{
            'symbol':symbol,
            'price':str(ticker.last),
            'market_data_type':ticker.marketDataType
        }
    finally:
        ib.client.disconnect()
async def get_paper_account():
    ib=IB()
    client_id=50000+ randbelow(40000)
    try:
        await ib.client.connectAsync(
            '127.0.0.1',
             4002,
             clientId=client_id,
             timeout=8
        )
        accounts= ib.client.getAccounts()
        if len(accounts) !=1 or not accounts[0].startswith('DU'):
            raise ValueError('excepted one paper account')
        account_id= accounts[0]
        await ib.reqAccountUpdatesAsync(account_id)
        positions= ib.portfolio(account_id)
        holding=[]
        for position in positions:
            holding.append({    'symbol':position.contract.symbol,
                                'quantity': str(position.position),
                                'average_cost': str(position.averageCost),
                                'currency': position.contract.currency,
                                'market_price': str(position.marketPrice),
                                'market_value': str(position.marketValue),
                                'unrealized_pnl': str(position.unrealizedPNL),
                                'realized_pnl': str(position.realizedPNL)})
        account_values= await ib.accountSummaryAsync()
        netvalue= None
        cash= None
        for value in account_values:
            if value.currency== 'USD':
                if value.tag== 'NetLiquidation':
                    netvalue= value.value
                if value.tag== 'TotalCashValue':
                    cash= value.value
        if netvalue is None:
            raise ValueError('usd net liquidation not available')
        return{
            'account_id': 'ibkr_paper',
            'name': 'IBKR Paper',
            'source': 'IBKR',
            'account_type': 'paper',
            'netvalue': netvalue,
            'cash': cash,
            'currency': 'USD',
            'holding':holding
        }

    
    finally:
        ib.client.disconnect()