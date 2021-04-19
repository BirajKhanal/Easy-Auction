from fastapi import APIRouter

router = APIRouter()


@router.post('/')
def create_auction():
    pass


@router.get('/')
def get_auctions():
    pass


@router.get('/{id}')
def get_auction():
    pass


@router.put('/{id}')
def update_auction():
    pass


@router.post('/{id}/bid')
def bid_in_auction():
    pass


@router.get('/{id}/bid')
def get_auction_bids():
    pass
