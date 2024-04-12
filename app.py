from fastapi import FastAPI, Query,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Connect to MongoDB
connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
database = client["Flora"]
floral_d = database["Floral Distribution"]
conserve_s = database["conserve status"]
species_s = database["species"]
loc=database["location"]
soil=database["soil"]
dataset=database["dataset"]



@app.get("/showall")
async def show(search_term: str = Query(None)):
    result_1 = list(floral_d.find({}, {"_id": 0}))
    result_2 = list(conserve_s.find({}, {"_id": 0}))
    result_3 = list(species_s.find({}, {"_id": 0}))
    result_4 = list(loc.find({}, {"_id": 0}))
    result_5 = list(soil.find({}, {"_id": 0}))
    result_6 = list(dataset.find({}, {"_id": 0}))




    response_data = {
        "result_1": result_1,
        "result_2": result_2,
        "result_3": result_3,
        "result_4":result_4,
        "result_5":result_5,
        "result_6": result_6,

    }

    if search_term:
        for key, value in response_data.items():
            response_data[key] = [row for row in value if any(search_term.lower() in str(val).lower() for val in row.values())]

    return JSONResponse(content=response_data)

@app.post("/create")
async def create_floral_data(data: dict):
    try:
        table_data = data.get("data")
        result = floral_d.insert_one(table_data)
        return JSONResponse(content={"success": True, "inserted_id": str(result.inserted_id)})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.delete("/delete_conserve")
async def delete_conserve_status(scientific_name_id: str):
    try:
        # Check if the scientific_name_id exists in the "conserve status" table
        existing_conserve = conserve_s.find_one({"scientificNameID": scientific_name_id})
        if not existing_conserve:
            raise HTTPException(status_code=404, detail=f"Conserve status with scientificNameID {scientific_name_id} not found")

        # Delete the conserve status based on scientificNameID
        result = conserve_s.delete_one({"scientificNameID": scientific_name_id})

        if result.deleted_count > 0:
            return JSONResponse(content={"success": True, "deleted_scientific_name_id": str(scientific_name_id)})
        else:
            return JSONResponse(content={"success": False, "message": "No matching record found for delete"})

    except Exception as e:
        return JSONResponse(content={"error": str(e)})

@app.delete("/delete_floral")
async def delete_floral_data(occurrence_id: str):
    try:
        # Check if the occurrence_id exists in the "Floral Distribution" table
        existing_floral = floral_d.find_one({"occurrenceID": occurrence_id})
        if not existing_floral:
            raise HTTPException(status_code=404, detail=f"Floral Distribution with occurrenceID {occurrence_id} not found")

        # Delete the Floral Distribution data based on occurrenceID
        result = floral_d.delete_one({"occurrenceID": occurrence_id})

        if result.deleted_count > 0:
            return JSONResponse(content={"success": True, "deleted_occurrence_id": str(occurrence_id)})
        else:
            return JSONResponse(content={"success": False, "message": "No matching record found for delete"})

    except Exception as e:
        return JSONResponse(content={"error": str(e)})

@app.put("/update_floral")
async def update_floral_data(occurrence_id: str, updated_data: dict):
    try:
        # Check if the occurrence_id exists in the "Floral Distribution" table
        existing_floral = floral_d.find_one({"occurrenceID": occurrence_id})
        if not existing_floral:
            raise HTTPException(status_code=404, detail=f"Floral Distribution with occurrenceID {occurrence_id} not found")

        # Update the Floral Distribution data based on occurrenceID
        result = floral_d.update_one({"occurrenceID": occurrence_id}, {"$set": updated_data})

        if result.modified_count > 0:
            return JSONResponse(content={"success": True, "updated_occurrence_id": str(occurrence_id)})
        else:
            return JSONResponse(content={"success": False, "message": "No matching record found for update"})

    except Exception as e:
        return JSONResponse(content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
