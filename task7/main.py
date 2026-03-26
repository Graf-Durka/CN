from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import get_db, GameModel
from parser import run_steam_parser


app = FastAPI(title="Steam Parser API")

@app.get("/parse")
def parse_and_save(url: str, db: Session = Depends(get_db)):
    scraped_data = run_steam_parser(url)
        
    for item in scraped_data:
        db_game = GameModel(**item)
        db.add(db_game)
    
    db.commit()
    return (f"games parsed : {len(scraped_data)}")

@app.get("/data")
def get_stored_data(db: Session = Depends(get_db)):
    games = db.query(GameModel).all()

    return [
        {
            "id": game.id,
            "name": game.name,
            "release_date": game.release_date,
            "discount": game.discount,
            "original_price": game.original_price,
            "discount_price": game.discount_price
        } 
        for game in games
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)