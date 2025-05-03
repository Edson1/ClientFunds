from fastapi import APIRouter
from app.controllers import fondo_controller

router = APIRouter()

@router.post("/fondos/{fondo_id}/suscribir")
def suscribir(fondo_id: int, usuario_id: int, metodo_notificacion: str):
    return fondo_controller.suscribirse(fondo_id, usuario_id, metodo_notificacion)

@router.post("/fondos/{fondo_id}/cancelar")
def cancelar(fondo_id: int, usuario_id: int):
    return fondo_controller.cancelar(fondo_id, usuario_id)

@router.get("/transacciones")
def ver_historial(usuario_id: int):
    return fondo_controller.historial(usuario_id)