/*
Modela formalmente el comportamiento de la música de fondo en el entorno de realidad virtual.
La música debe estar a su máximo volumen si el usuario se está desplazando por el entorno.
Debe adoptar un volumen más bajo si el gorrión está cantando.
Se establece en un volumen mínimo si el usuario está quieto.
*/

class SonidoAmbiental {
  var usuarioQuieto: bool
  var gorrionCantando: bool
  var volumen: real

  // Volúmenes establecidos como constantes
  const VOLUMEN_MAX: real := 1.0
  const VOLUMEN_MIN: real := 0.2
  const VOLUMEN_GORRION: real := 0.05

  constructor ()
    ensures usuarioQuieto
    ensures !gorrionCantando
    ensures volumen == VOLUMEN_MIN
  {
    usuarioQuieto := true;
    gorrionCantando := false;
    volumen := VOLUMEN_MIN;
  }

  // Actualiza el estado del gorrión
  method SetGorrionCantando(canta: bool)
    modifies this
    ensures gorrionCantando == canta
  {
    gorrionCantando := canta;
  }

  // Actualiza el estado del usuario
  method SetUsuarioQuieto(quieto: bool)
    modifies this
    ensures usuarioQuieto == quieto
  {
    usuarioQuieto := quieto;
  }

  // Aplica la lógica de ajuste de volumen
  method ActualizarVolumen()
    modifies this
    ensures gorrionCantando ==> volumen == VOLUMEN_GORRION
    ensures !gorrionCantando && usuarioQuieto ==> volumen == VOLUMEN_MIN
    ensures !gorrionCantando && !usuarioQuieto ==> volumen == VOLUMEN_MAX
  {
    if gorrionCantando {
      volumen := VOLUMEN_GORRION;
    } else if usuarioQuieto {
      volumen := VOLUMEN_MIN;
    } else {
      volumen := VOLUMEN_MAX;
    }

    // El volumen debe estar en un rango válido
    assert 0.0 <= volumen <= VOLUMEN_MAX;
  }
}