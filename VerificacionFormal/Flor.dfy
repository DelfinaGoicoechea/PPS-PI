/*
Modela formalmente el comportamiento de la flor interactiva en el entorno de realidad virtual.
La flor debe abrirse si está siendo mirada desde una distancia menor o igual a un valor máximo.
Debe cerrarse automáticamente si deja de ser mirada.
Este modelo incluye estado interno, condiciones lógicas y verificación de trancisiones de estado.
*/

datatype EstadoFlor = Abierta | Cerrada

// Constante configurable: distancia máxima para activar apertura
const maxGazeDistance: real := 6.0

// Determina si la flor está siendo mirada correctamente
predicate EstaSiendoMirada(distancia: real, florObjetivo: bool)
    requires distancia >= 0.0
{
    distancia <= maxGazeDistance && florObjetivo
}

// Clase que representa una flor con estado interno
class Flor {
  var estado: EstadoFlor

  method ActualizarEstado(distancia: real, florObjetivo: bool)
    requires distancia >= 0.0
    modifies this
    ensures EstaSiendoMirada(distancia, florObjetivo) ==> estado == Abierta
    ensures !EstaSiendoMirada(distancia, florObjetivo) ==> estado == Cerrada
  {
    if EstaSiendoMirada(distancia, florObjetivo) {
      estado := Abierta;
    } else {
      estado := Cerrada;
    }
  }
}