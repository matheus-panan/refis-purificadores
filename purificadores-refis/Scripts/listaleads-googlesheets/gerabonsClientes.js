function separaClientes(clientesBons, clientesMedios, clientesRuins)
{
  var clientesBOM = embaralharArray(clientesBons)
  var clientesMEDIO = embaralharArray(clientesMedios)
  var clientesRUIM = embaralharArray(clientesRuins)
  //console.log("Clientes BONS: " + clientesBOM.length)
  var lista1 = clientesBOM.slice(0, 7);
  var lista2 = clientesBOM.slice(7, 14);
  var lista3 = clientesMEDIO.slice(0, 25)
  var lista4 = clientesMEDIO.slice(25, 50)
  var lista5 = clientesRUIM.slice(0, 8)
  var lista6 = clientesRUIM.slice(8, 16)
  var listaGabrielly = lista1.concat(lista3, lista5)
  var listaMaria = lista2.concat(lista4, lista6)
  console.log("Lista Gabrielly: "+ listaGabrielly.length)
  console.log("Lista Maria: " + listaMaria.length)
  var listatotal = listaMaria.concat(listaGabrielly)
  //console.log("Clientes bons: "+ clientesBons.length +"\nClientes médios: "+ clientesMedios.length +"\nClientes Ruins: "+ clientesRuins.length)
  return listatotal
}