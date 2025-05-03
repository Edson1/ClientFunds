from fastapi import HTTPException
from app.models.usuario import Usuario
from app.models.fondo import Fondo
from app.models.transaccion import Transaccion
from app.services.sns_service import SNSService

def suscribirse(fondo_id: int, usuario_id: int, metodo_notificacion: str):
    fondo = Fondo.get_by_id(fondo_id)
    usuario = Usuario.get_by_id(usuario_id)

    if fondo.id in usuario.fondos:
        raise HTTPException(status_code=400, detail="Ya está suscrito al fondo")

    if usuario.saldo < fondo.monto_minimo:
        raise HTTPException(
            status_code=400,
            detail=f"No tiene saldo disponible para vincularse al fondo {fondo.nombre}"
        )

    usuario.saldo -= fondo.monto_minimo
    usuario.fondos.append(fondo.id)
    usuario.save()

    Transaccion.create("apertura", fondo_id, usuario_id, fondo.monto_minimo)
    SNSService.enviar_notificacion(usuario, metodo_notificacion, f"Suscripción exitosa al fondo {fondo.nombre}")
    return {"mensaje": "Suscripción realizada"}

def cancelar(fondo_id: int, usuario_id: int):
    usuario = Usuario.get_by_id(usuario_id)
    fondo = Fondo.get_by_id(fondo_id)

    if fondo.id not in usuario.fondos:
        raise HTTPException(status_code=400, detail="No está suscrito a este fondo")

    usuario.fondos.remove(fondo.id)
    usuario.saldo += fondo.monto_minimo
    usuario.save()

    Transaccion.create("cancelacion", fondo_id, usuario_id, fondo.monto_minimo)
    return {"mensaje": "Desvinculación realizada y monto reembolsado"}

def historial(usuario_id: int):
    return Transaccion.get_by_usuario(usuario_id)