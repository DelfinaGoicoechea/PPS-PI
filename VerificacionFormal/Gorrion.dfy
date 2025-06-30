/*
Modela formalmente el comportamiento del gorrión interactivo en el entorno de realidad virtual.
El gorrión reacciona al ingreso del usuario en una zona y cambia su estado en consecuencia.
*/

datatype EstadoGorrion = Inactivo | Cantando | Interactivo

class Gorrion {
  var estado: EstadoGorrion
  var usuarioEnZona: bool

  constructor ()
    ensures estado == Inactivo && !usuarioEnZona
  {
    estado := Inactivo;
    usuarioEnZona := false;
  }

  // Método invocado cuando el usuario entra al collider
  method UsuarioEntraEnZona()
    requires !usuarioEnZona
    modifies this
    ensures usuarioEnZona
    ensures estado == Cantando
  {
    usuarioEnZona := true;
    estado := Cantando;
  }

  // Método invocado cuando el canto termina
  method FinCanto()
    requires estado == Cantando && usuarioEnZona
    modifies this
    ensures estado == Interactivo
  {
    estado := Interactivo;
  }

  // Método invocado cuando el usuario sale del collider
  method UsuarioSaleDeZona()
    requires usuarioEnZona
    modifies this
    ensures !usuarioEnZona
    ensures estado == Inactivo
  {
    usuarioEnZona := false;
    estado := Inactivo;
  }

  // Verificación formal:
  // si el usuario no está en la zona, el gorrión nunca puede estar en estado Cantando ni Interactivo
  predicate EstadoValido()
    reads this
  {
    usuarioEnZona ==> (estado == Cantando || estado == Interactivo) && !usuarioEnZona ==> estado == Inactivo
  }
}