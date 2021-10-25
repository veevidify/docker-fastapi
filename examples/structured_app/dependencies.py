from fastapi import Header, HTTPException, status

async def get_token_header(x_token: str = Header(...)):
    if (x_token != "some_token"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Token header invalid."
        )

async def get_query_token(token: str):
    if (token != "some_other_token"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No token provided."
        )