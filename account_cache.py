from market_data import get_paper_account
import asyncio


paper_cache= {
    'account': None,
    'is_updating': False,
    'last_error':None
}
async def refresh_paper_account():
    paper_cache['is_updating']= True
    try: 
        paper_cache['account']= await get_paper_account()
        paper_cache['last_error']= None
    except Exception as error:
        paper_cache['last_error']= str(error)
    finally:
        paper_cache['is_updating']= False

async def run_paper_refresh_loop():
    while True:
        await refresh_paper_account()
        await asyncio.sleep(30)

