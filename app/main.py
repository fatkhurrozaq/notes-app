from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Notes App")

# In-memory storage
notes = {}
counter = {"id": 0}


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


@app.get("/")
def root():
    return {"message": "Notes App is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    counter["id"] += 1
    note_id = counter["id"]
    notes[note_id] = {"id": note_id, "title": note.title, "content": note.content}
    return notes[note_id]


@app.get("/notes")
def get_notes():
    return list(notes.values())


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    return notes[note_id]


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    del notes[note_id]
    return {"message": "Note deleted"}