from fastapi import APIRouter

router = APIRouter()


# @router.get("/{client_id}}/{organization_id}/locations", response_model=List[Location])
# async def read_locations(client_id: int, organization_id: int, db: Session = Depends(get_db)):
#     locations = db.query(Location).filter(Location.client_id == client_id, Location.organization_id == organization_id).all()
#     return locations
#
# @router.get("/{client_id}}/{organization_id}/locations/{location_id}", response_model=Location)
# async def read_location(client_id: int, organization_id: int, location_id: int, db: Session = Depends(get_db)):
#     location = db.query(Location).filter(Location.client_id == client_id, Location.organization_id == organization_id, Location.id == location_id).first()
#     if location is None:
#         raise HTTPException(status_code=404, detail="Location not found")
#     return location
#
# @router.post("/{client_id}}/{organization_id}/locations", response_model=Location)
# async def create_location(client_id: int, organization_id: int, location: Location, db: Session = Depends(get_db)):
#     db_location = Location(client_id=client_id, organization_id=organization_id, **location.dict())
#     db.add(db_location)
#     db.commit()
#     db.refresh(db_location)
#     return db_location
#
# @router.put("/{client_id}}/{organization_id}/locations/{location_id}", response_model=Location)
# async def update_location(client_id: int, organization_id: int, location_id: int, location: Location, db: Session = Depends(get_db)):
#     db_location = db.query(Location).filter(Location.client_id == client_id, Location.organization_id == organization_id, Location.id == location_id).first()
#     if db_location is None:
#         raise HTTPException(status_code=404, detail="Location not found")
#     update_data = location.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_location, key, value)
#     db.commit()
#     db.refresh(db_location)
#     return db_location
#
# @router.delete("/{client_id}}/{organization_id}/locations/{location_id}", response_model=Location)
# async def delete_location(client_id: int, organization_id: int, location_id: int, db: Session = Depends(get_db)):
#     location = db.query(Location).filter(Location.client_id == client_id, Location.organization_id == organization_id, Location.id == location_id).first()
#     if location is None:
#         raise HTTPException(status_code=404, detail="Location not found")
#     db.delete(location)
#     db.commit()
#     return location