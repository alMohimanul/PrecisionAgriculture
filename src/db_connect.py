from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import APIRouter
from Controller.V1.databaseController import get_db_connection

router = APIRouter()


def chk_conn(conn):
     try:
        conn.cursor()
        return True
     except Exception as ex:
        return False
     
@router.post("/checkConnection")     
async def check():
    try:
        conn = get_db_connection()
        print(chk_conn(conn)) 
        conn.close()
        return {"message": "Connection successful"}
    except Exception as e:
        return {"message": "Connection failed", "error": str(e)}
    

class diseases(BaseModel):
    disease_name: str
    description: str = None
    symptoms: str = None
    causes_of_disease: str = None
    prevention_method: str = None
    treatment: str = None
    risk_areas: str = None

class DiseaseRequest(BaseModel):
    disease_name: str
    
@router.post("/fetchData", response_model=diseases)
async def read_item(request: DiseaseRequest):
    disease_name = request.disease_name
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM crop_disease WHERE disease_name = ?', (disease_name,))
    item = c.fetchone()
    
    conn.close()
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item_data = {
        "disease_name": item['disease_name'],
        "description": item['description'],
        "symptoms": item['symptoms'],
        "causes_of_disease": item['causes_of_the_disease'],
        "prevention_method": item['prevention_method'],
        "treatment": item['treatment'],
        "risk_areas": item['risk_areas']
    }
    
    return diseases(**item_data)