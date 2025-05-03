import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException

from app.controllers.fondo_controller import suscribirse, cancelar, historial

class TestFondosController(unittest.TestCase):

    @patch('app.controllers.fondo_controller.Usuario')
    @patch('app.controllers.fondo_controller.Fondo')
    @patch('app.controllers.fondo_controller.Transaccion')
    @patch('app.controllers.fondo_controller.SNSService')
    def test_suscribirse_exitoso(self, mock_sns, mock_transaccion, mock_fondo_class, mock_usuario_class):
        
        mock_fondo = MagicMock(id=1, nombre='Fondo A', monto_minimo=100000)
        mock_usuario = MagicMock(id=1, saldo=200000, fondos=[])
        mock_fondo_class.get_by_id.return_value = mock_fondo
        mock_usuario_class.get_by_id.return_value = mock_usuario

        result = suscribirse(fondo_id=1, usuario_id=1, metodo_notificacion='email')

        self.assertEqual(result, {"mensaje": "Suscripción realizada"})
        self.assertEqual(mock_usuario.saldo, 100000)
        self.assertIn(1, mock_usuario.fondos)

        mock_usuario.save.assert_called_once()
        mock_transaccion.create.assert_called_once()
        mock_sns.enviar_notificacion.assert_called_once()


    @patch('app.controllers.fondo_controller.Usuario')
    @patch('app.controllers.fondo_controller.Fondo')
    def test_suscribirse_saldo_insuficiente(self, mock_fondo_class, mock_usuario_class):

        mock_fondo = MagicMock(id=2, nombre='Fondo B', monto_minimo=300000)
        mock_usuario = MagicMock(id=1, saldo=200000, fondos=[])
        mock_fondo_class.get_by_id.return_value = mock_fondo
        mock_usuario_class.get_by_id.return_value = mock_usuario

        with self.assertRaises(HTTPException) as context:
            suscribirse(fondo_id=2, usuario_id=1, metodo_notificacion='sms')

        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("No tiene saldo disponible", context.exception.detail)


    @patch('app.controllers.fondo_controller.Usuario')
    @patch('app.controllers.fondo_controller.Fondo')
    @patch('app.controllers.fondo_controller.Transaccion')
    def test_cancelar_exitoso(self, mock_transaccion, mock_fondo_class, mock_usuario_class):

        mock_fondo = MagicMock(id=1, nombre='Fondo A', monto_minimo=100000)
        mock_usuario = MagicMock(id=1, saldo=100000, fondos=[1])
        mock_fondo_class.get_by_id.return_value = mock_fondo
        mock_usuario_class.get_by_id.return_value = mock_usuario

        result = cancelar(fondo_id=1, usuario_id=1)

        self.assertEqual(result, {"mensaje": "Desvinculación realizada y monto reembolsado"})
        self.assertEqual(mock_usuario.saldo, 200000)
        self.assertNotIn(1, mock_usuario.fondos)

        mock_usuario.save.assert_called_once()
        mock_transaccion.create.assert_called_once()


    @patch('app.controllers.fondo_controller.Transaccion')
    def test_historial(self, mock_transaccion):

        mock_transaccion.get_by_usuario.return_value = [
            {"tipo": "apertura", "fondo_id": 1, "monto": 100000}
        ]

        result = historial(usuario_id=1)

        self.assertEqual(result, [{"tipo": "apertura", "fondo_id": 1, "monto": 100000}])
        
        mock_transaccion.get_by_usuario.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()