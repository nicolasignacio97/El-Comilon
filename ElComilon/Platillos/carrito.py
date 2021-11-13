class carrito:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito
            
    def agregar( self, Platillos):
        id = str(Platillos.idplatillo)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "idplatillo" : Platillos.idplatillo,
                "nombre" : Platillos.nombre,
                "ingredientes" : Platillos.ingredientes,
                "valorunitario" : Platillos.valorunitario,
                "acumulado": Platillos.valorunitario,
                "cantidad": 1,
            }
        else:
            self.carrito[id]["cantidad"] +=1
            self.carrito[id]["acumulado"] += Platillos.valorunitario
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True
    
    def eliminiar(self, Platillos):
        id = str(Platillos.idplatillo)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self,Platillos):
        id = str(Platillos.idplatillo)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -=1
            self.carrito[id]["acumulado"] -= Platillos.valorunitario
            if self.carrito[id]["cantidad"] <= 0 : self.eliminiar(Platillos)
            self.guardar_carrito()
            
    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
