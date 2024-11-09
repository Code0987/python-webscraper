from fastapi import APIRouter, Depends, HTTPException
from ..schemas.scape_request import ScrapeRequest
from ..producers.scrapper_producer import push_scrape_request
from ..utils.auth_utils import TokenBearer

router = APIRouter(dependencies=[Depends(TokenBearer(auto_error=False))])


@router.post("/scrape/")
def create(payload: ScrapeRequest):
    try:
        push_scrape_request(scrape_request=payload)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "ok"}
