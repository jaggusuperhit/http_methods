from fastapi import FastAPI, Path, Query, HTTPException
from typing import Annotated, Any, Dict, List
import json

app = FastAPI()

def load_data() -> Dict[str, Dict[str, Any]]:
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

data = load_data()  # Load data once when the application starts

@app.get("/")
def hello() -> Dict[str, str]:
    return {'message':'Patient Management System API'}

@app.get('/about')
def about() -> Dict[str, str]:
    return {'message': 'A fully functional API to manage your patient records'}

@app.get('/view')
def view() -> Dict[str, Dict[str, Any]]:
    return data

@app.get('/search/{patient_id}')
def search(
    patient_id: Annotated[
        str, 
        Path(..., title='Patient ID', description='ID of the patient')
    ]
) -> Dict[str, Any]:
    """Get patient by ID.

    Examples:
    - patient_id: P001
    """
    patient = data.get(patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail='Patient not found')
    return patient

@app.get('/query')
def query(
    name: Annotated[str | None, Query(title='Patient Name', description='Name of the patient')] = None,
    age: Annotated[int | None, Query(title='Patient Age', description='Age of the patient')] = None,
    city: Annotated[str | None, Query(title='Patient City', description='City of the patient')] = None,
    sort_by: Annotated[str | None, Query(title='Sort By', description='Field to sort by (name, age, or city)')] = None,
    order: Annotated[str | None, Query(title='Order', description='Order of sorting (asc or desc)')] = None
) -> List[Dict[str, Any]]:
    """Query patients by name, age, or city.

    Examples:
    - name: Ananya Sharma
    - age: 30
    - city: Guwahati
    - sort_by: name
    - order: asc
    """
    results: List[Dict[str, Any]] = []
    for patient_id, patient in data.items():
        if (name is None or patient.get('name') == name) and (age is None or patient.get('age') == age) and (city is None or patient.get('city') == city):
            results.append(patient)

    if sort_by:
        if sort_by not in ['name', 'age', 'city']:
            raise HTTPException(status_code=400, detail='Invalid sort_by field')
        if order and order not in ['asc', 'desc']:
            raise HTTPException(status_code=400, detail='Invalid order')
        reverse = order == 'desc'
        results.sort(key=lambda x: str(x.get(sort_by, '')), reverse=reverse)

    if not results:
        raise HTTPException(status_code=404, detail='No patients found matching the query')
    return results