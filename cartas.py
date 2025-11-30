# cartas.py
PenalidadesGlobal =[]
##### Funciones Penalidades ####
def Penalizacion(penalidad: dict,estado):
    for key,valor in penalidad.items():
        estado[key] = valor

def PenalidadTurnos(penalidad: dict ,PenalidadesLista: list,indice: int ,estado):
    if not isinstance(penalidad, list):
        for key,valor in penalidad.items():
            if key in estado:
                if key == "Carta":
                    print(f"Carta: {valor}")
                elif estado[key] == 0:
                    PenalidadesLista[indice][1] = False
                    
                elif estado[key] > 0:
                    estado[key] -= 1
                
def EliminarPenalidad(PenalidadLista: list):
    if PenalidadLista[0][1] == False:
        PenalidadLista.clear()
    else:
        pass
    
################################

##### Penalidad por cartas #####


# Carta 3 
Penalidad_3 = []
def PenalidadCarta3_1(estado):
    
    if estado["VirusInventarioNoVisible_VirusActivo"] > 1:
        if isinstance(estado["Inventario"],int) and isinstance(estado["Insumos disponibles"],int):
            estado["GuardadoValoresAuxiliarVirus"] = (estado["Inventario"],estado["Insumos disponibles"])

        estado["Inventario"] = "No disponible por virus"
        estado["Insumos disponibles"] = "No disponible por virus"
        
    elif estado["VirusInventarioNoVisible_VirusActivo"] == 1:
        estado["Inventario"] = estado["GuardadoValoresAuxiliarVirus"][0]
        estado["Insumos disponibles"] = estado["GuardadoValoresAuxiliarVirus"][1]
        estado["GuardadoValoresAuxiliarVirus"]= "Nada que guardar"
    return estado
def PenalidadCarta3_2(estado):
    if estado["VirusInventarioNoVisible_VirusActivo"] > 0:
        estado["Prohibir Produccion"] = True
        estado["Prohibir Compras"] = True
    elif estado["VirusInventarioNoVisible_VirusActivo"] == 0:
        estado["Prohibir Produccion"] = False
        estado["Prohibir Compras"] = False
    return estado


# Carta 6
Penalidad_6 = []
def PenalidadCarta6(estado):
    estado["DemandaExtraTemporal"] *= 0.5
    return estado

# Carta 9
Penalidad_9 = []
def PenalidadCarta9(estado):
    if estado["Huelga"] >2:
        estado["Prohibir Produccion"] = True
    elif estado["Huelga"] == 1:
        estado["Prohibir Produccion"] = False
    return estado
# Carta 12
Penalidad_12 = []
def PenalidadCarta12(estado):
    estado["Unidades vendidas"] *= 0.5
    estado["Pedidos por atender"] *= 0.5
    estado["Caja disponible"] *= 0.5
    return estado

# Carta 13
Penalidad_13 = []
def PenalidadCarta13(estado):
    print("Penalidad falla en el etiquetado")
    return estado

# Carta 14
Penalidad_14 = []
def PenalidadCarta14(estado):
    if estado["Retraso Importacion"] > 0:
        estado["Prohibir Importaciones"] = True
    elif estado["Retraso Importacion"] == 0:
        estado["Prohibir Importaciones"]= False
    return estado

# Carta 15
Penalidad_15 = []
def PenalidadCarta15(estado):
    if estado["Proveedores Huelga"] > 0:
        estado["Prohibir Compras"] = True
    elif estado["Proveedores Huelga"] == 0:
        estado["Prohibir Compras"] = False
    return estado

# Carta 18
Penalidad_18 = []
def PenalidadCarta18(estado):
    estado["Unidades vendidas"] *= 0.5
    return estado

# Carta 21
Penalidad_21 = []
def PenalidadCarta21(estado):
    if estado["Mal Clima"] > 0:
        estado["Prohibir Produccion"] = True
    elif estado["Mal Clima"] == 0:
        estado["Prohibir Produccion"] = False
    return estado

# Carta 22
Penalidad_22 = []
def PenalidadCarta22(estado):
    if estado["Licencia vencida"] > 0:
        estado["Prohibir Produccion"] = True
    elif estado["Licencia vencida"] == 0:
        estado["Prohibir Produccion"] = False
    return estado

# Carta 24
Penalidad_24 = []
def PenalidadCarta24(estado):
    
    if estado["Bloqueo logistico"]> 0:
        estado["Unidades vendidas"] = estado["GuardadoValoresAuxiliarBloqueoLogistico"][0]
        estado["Caja disponible"] = estado["GuardadoValoresAuxiliarBloqueoLogistico"][2]
        estado["Pedidos por atender"] = estado["GuardadoValoresAuxiliarBloqueoLogistico"][1]
        estado["Inventario"] = estado["GuardadoValoresAuxiliarBloqueoLogistico"][3]
    elif estado["Bloqueo logistico"] == 0:
        print("Penalidad24 acabada")
    return estado

# Carta 26
Penalidad_26 = []
def PenalidadCarta26(estado):
    if estado["Nuevo Competidor"] != 3:
        Resto = estado["Caja disponible"] - 5000
        if Resto < 0:
            estado["Caja disponible"]= 0
            estado["Deuda pendiente"] = abs(Resto)
        else:
            estado["Caja disponible"] = Resto
        
        estado["Unidades vendidas"] = max(0, int(estado["Unidades vendidas"] - (estado["Unidades vendidas"]*0.4)))
    return estado

# Carta 28
Penalidad_28 = []
def PenalidadCarta28(estado):
    estado["Costo por empleado"] = estado["Costo por empleado"] + (estado["Costo por empleado"] * 0.1)
    estado["Sueldos por pagar"] = estado["Cantidad de empleados"] * estado["Costo por empleado"]
    
    return estado

# Carta 30
Penalidad_30 = []
def PenalidadCarta30(estado):
    estado["Unidades vendidas"] =0
    if estado["Huelga Nacional"]>0:
        estado["Prohibir Produccion"] = True
    elif estado["Huelga Nacional"] == 0:
        estado["Prohibir Produccion"] = False
    return estado

# Carta 34
Penalidad_34 = []
def PenalidadCarta34(estado):
    estado["Unidades vendidas"] = max(0, estado["Unidades vendidas"] - (estado["Unidades vendidas"]*0.25))
    return estado

# Carta 37
Penalidad_37 = []
def PenalidadCarta37(estado):
    if estado["Trabajador Accidente"] > 0:
        estado["Cantidad de empleados"] -= 1
    elif estado["Trabajador Accidente"] == 0:
        estado["Cantidad de empleados"] += 1
    return estado

# Carta 38
Penalidad_38 = []
def PenalidadCarta38(estado):
    if estado["Derrame quimico"]>0:
        estado["Prohibir Produccion"] = True
    elif estado["Derrame quimico"] == 0:
        estado["Prohibir Produccion"] = False
    return estado

# Carta 39
Penalidad_39 = []
def PenalidadCarta39(estado):
    if estado["Virus Contagioso"] > 0: 
        estado["Cantidad de empleados"] = 0
    elif estado["Virus Contagioso"] == 0:
        print(estado["GuardadoValoresAuxiliarVirusContagioso"])
        estado["Cantidad de empleados"] = estado["GuardadoValoresAuxiliarVirusContagioso"]
    return estado

# Carta 40
Penalidad_40 = []
def PenalidadCarta40(estado):
    if estado["HiringFreeze"]>0:
        estado["Prohibir contrataciones"] = True
    elif estado["HiringFreeze"] == 0:
        estado["Prohibir contrataciones"] = False
    return estado
################################

def aplicar_carta(numero: int , estado : dict):
    # Carta 1: Dia tranquilo:
    # No ocurre nada malo.
    if numero == 1:
        return estado
    
    
    # Terminado
    # Carta 2: Falla critica en maquinaria:
    # Pierdes 2 maquinas activas permanentemente (hasta hacer mantenimiento)
    elif numero == 2:
        Maquinas = estado["Maquinas (total/activas/dañadas)"].split("/")
        for i,elementos in enumerate(Maquinas):
            Maquinas[i] = int(elementos)
        Maquinas[1] -= 2
        Maquinas[2]+= 2
        if Maquinas[1] <= 0:
            Maquinas[1] = 0
        if Maquinas[0] <= 0:
            Maquinas[0] = 0
        estado["Maquinas (total/activas/dañadas)"] = f"{Maquinas[0]}/{Maquinas[1]}/{Maquinas[2]}"
        return estado

    # Terminado
    # Carta 3: Virus informatico:
    # Se pierde visibilidad del inventario y de los insumos por 1 turno
    # No puedes producir porque no sabes cuantos insumos hay.
    # No puedes vender porque no sabes cuanto invnetario hay.
    # Los clientes se enteraron y bajo la reputacion 1 nivel
    # Duración: 2 turnos
    elif numero == 3:
        Nivel = estado["Reputacion del mercado"].split()
        Nivel[1] = int(Nivel[1]) -1
        estado["Reputacion del mercado"] = f"Nivel {Nivel[1]}"
        Penalidades3 = {"Carta": 3,"VirusInventarioNoVisible_VirusActivo":3}
        Penalidad_3.append([Penalidades3,True])
        PenalidadesGlobal.append([Penalidades3,True])
        Penalizacion(Penalidades3,estado)
        PenalidadCarta3_1(estado)
        PenalidadCarta3_2(estado)

        return estado



    # Terminado
    # Carta 4: Incendio en almacen
    #   - Se pierde el inventario total (al final del mes, despues de haber producido y vendido)
    elif numero == 4:
        estado["Incendio Pendiente"] = True
        return estado


    # Terminado
    # Carta 5: Auditoria desfavorable
    #   - Aumentan las multas e indemnizaciones en +5000.
    # Los clientes se enteraron y bajo la reputacion 1 nivel
    elif numero == 5:
        estado["Multas e indemnizaciones"] += 5000
        Nivel = estado["Reputacion del mercado"].split(" ")
        estado["Reputacion del mercado"] = f"Nivel {max(0,int(Nivel[1]) -1)}"
        return estado


    # Terminado
    # Carta 6: Producto retirado del mercado
    #   - Reputacion se reduce 2 niveles.
    #   - Tuvimos que reponer mercaderia equivalente a la demanda actual (elimina el inventario equivalente a la demanda)
    #   - Luego, la demanda actual se reduce en 50%
    # Duración: 2 turnos
    elif numero == 6:
        Nivel = estado["Reputacion del mercado"].split(" ")
        estado["Reputacion del mercado"] = f"Nivel {max(0,int(Nivel[1]) -2)}"
        estado["Inventario"] = 0
        Penalidades6 = {"Carta":6, "Demanda Actual Reducida": 2}
        Penalidad_6.append([Penalidades6,True])
        PenalidadesGlobal.append([Penalidades6,True])
        Penalizacion(Penalidades6,estado)
        PenalidadCarta6(estado)
        return estado


    # Terminado
    # Carta 7: Robo de insumos
    #   - Pierdes 30% de insumos disponibles.
    elif numero == 7:
        estado["Insumos disponibles"]= max(0,estado["Insumos disponibles"] - estado["Insumos disponibles"] * 0.3)
        
        return estado


    # Terminado
    # Carta 8: Fuga de talento clave
    #   - Tras la fuga de talento, operarios sin experiencia manipularon y dañaron una maquina
    #   - Pierdes 1 maquina activa (pasa a dañada).
    #   - Pierdes 1 empleado.
    elif numero == 8:
        if "AmbienteLaboralFavorable" in estado:
            if estado["AmbienteLaboralFavorable"] == True:
                print("Se evito la fuga de talento por el excelente ambiente laboral")
                pass
        else:
            Maquinas = estado["Maquinas (total/activas/dañadas)"].split("/")
            if Maquinas[1] != 0:
                Maquinas[1] -= 1
                Maquinas[2] +=1
            else:
                print("No hay maquinas activas")
            
            estado["Maquinas (total/activas/dañadas)"] = f"{Maquinas[0]}/{Maquinas[1]}/{Maquinas[2]}"
            estado["Cantidad de empleados"] = max(0,estado["Cantidad de empleados"]-1)
        return estado


    # Terminado
    # Carta 9: Huelga por ambiente laboral
    #   - La proxima ronda no se produce.
    #   - Los clientes se enteran de la huelga y baja la reputación 3 niveles
    # Duración: 2 turnos
    elif numero == 9:
        if "AmbienteLaboralFavorable" in estado:
            if estado["AmbienteLaboralFavorable"]== True:
                #Sin Huelgas
                print("Ambiente favorable no hay huelgas")
                pass
        else:
            Reputacion = estado["Reputacion del mercado"].split(" ")
            estado["Reputacion del mercado"] = f"Nivel {max(0,int(Reputacion[1])-3)}"
            Penalidades9 = {"Carta": 9, "Huelga":3}
            Penalidad_9.append([Penalidades9,True])
            PenalidadesGlobal.append([Penalidades9,True])
            Penalizacion(Penalidades9,estado)
            PenalidadCarta9(estado)
        return estado


    # Terminado
    # Carta 10: Hacker secuestra datos
    #   - Pierdes 5,000 de caja (si no alcanza, la diferencia se convierte en deuda al 12%)
    #   - Reputacion baja 2 niveles
    #   - Te aplican una multa de 5,000 soles por malas practicas de seguridad de la informacion
    elif numero == 10:
        caja = estado["Caja disponible"] - 5000
        if caja <= 0:
            PorcentajeDeuda = abs(caja) * 0.12
            caja = 0
            estado["Deuda pendiente"] += PorcentajeDeuda
        estado["Caja disponible"] = caja
        return estado


    # Terminado
    # Carta 11: Multa ambiental
    #   - Aumentan “Multas e indemnizaciones” en +5000.
    #   - Reputacion del mercado −1 nivel.
    elif numero == 11:
        estado["Multas e indemnizaciones"] += 5000
        Nivel = estado["Reputacion del mercado"].split(" ")
        estado["Reputacion del mercado"] = f"Nivel {max(0,int(Nivel[1])-1)}"
        return estado


    # Terminado
    # Carta 12: Boicot de clientes
    #   - Ventas de esta semana reducidas al 50%:
    # Duración: 2 turnos
    elif numero == 12:
        Penalidades12 = {"Carta": 12,"Reduccion Ventas":2}
        Penalidad_12.append([Penalidades12,True])
        PenalidadesGlobal.append([Penalidades12,True])
        Penalizacion(Penalidades12,estado)
        PenalidadCarta12(estado)
        return estado


    # Terminado
    # Carta 13: Error de etiquetado
    #   - Devuelven todas las unidades vendidas el turno actual y el turno anterior
    #     • Debes devolver el dinero obtenido por dichas ventas
    #     • Además, gastas 15,000 soles en la logística inversa
    # Duración: 3 turnos
    elif numero == 13:
        if "AmbienteLaboralFavorable" in estado:
            if estado["AmbienteLaboralFavorable"] == True:
                print("Existe un ambiente laboral favorable y se evitaron los errores de etiquetado")
                pass
        else:
            UnidadesActuales = estado["Unidades vendidas"]
            UnidadesAnteriores = estado["InventarioMesAnterior"]
            estado["Inventario"] += (UnidadesActuales + UnidadesAnteriores)
            DineroDevolver = (UnidadesActuales + UnidadesAnteriores)* estado["Precio venta"]
            Resto = estado["Caja disponible"]-DineroDevolver - 15000
            if Resto < 0:
                estado["Caja disponible"] = 0
                estado["Deuda pendiente"] += abs(Resto)
            else:
                estado["Caja disponible"] = Resto
            estado["Unidades vendidas"] = 0
            estado["InventarioMesAnterior"] = 0
            
            Penalidades13 = {"Carta": 13, "Error etiquetado": 4}
            Penalidad_13.append([Penalidades13,True])
            PenalidadesGlobal.append([Penalidades13,True])
            Penalizacion(Penalidades13,estado)
            PenalidadCarta13(estado)
        return estado


    # Terminado
    # Carta 14: Retraso en importacion
    #   - Prohibir insumos importados las siguientes 3 rondas:
    elif numero == 14:
        estado["Prohibir Importaciones"] = True
        Penalidades14 = {"Carta": 14, "Retraso Importacion": 4}
        Penalidad_14.append([Penalidades14,True])
        PenalidadesGlobal.append([Penalidades14,True])
        Penalizacion(Penalidades14,estado)
        PenalidadCarta14(estado)
        return estado



    # Terminado
    # Carta 15: Proveedores en huelga
    #   - Prohibir compras nacionales las siguientes 4 rondas:
    elif numero == 15:
        estado["Prohibir Compras"] = True 
        Penalidades15 = {"Carta": 15, "Proveedores Huelga": 4}
        Penalidad_15.append([Penalidades15,True])
        PenalidadesGlobal.append([Penalidades15,True])
        Penalizacion(Penalidades15,estado)
        PenalidadCarta15(estado)
        return estado

    # Terminado
    # Carta 16: Estafa financiera
    #   - Pierdes 8,000 de caja
    elif numero == 16:
        Resto = estado["Caja disponible"] - 8000
        
        if Resto < 0:
            estado["Caja disponible"] = 0
            estado["Deuda pendiente"] += abs(Resto)
        else:
            estado["Caja disponible"] = Resto
        return estado

    # Terminado
    # Carta 17: Rumor de corrupcion
    #   - Reputacion del mercado −2 niveles.
    elif numero == 17:
        Nivel = estado["Reputacion del mercado"].split(" ")
        estado["Reputacion del mercado"] = f"Nivel {max(0,int(Nivel[1])-2)}"
        return estado
    
    # Terminado
    # Carta 18: Plaga en planta
    #   - Produccion a la mitad este turno
    # Duración: 3 turnos
    elif numero == 18:
        Penalidades18 = {"Carta":18, "PlagaPlanta":3}
        Penalidad_18.append([Penalidades18,True])
        PenalidadesGlobal.append([Penalidades18,True])
        Penalizacion(Penalidades18,estado)
        PenalidadCarta18(estado)
        return estado

    # Terminado
    # Carta 19: Cliente corproativo VIP cancela pedido
    #   - Peirdes un tercio de los “Pedidos por atender”.
    elif numero == 19:
        if estado["Pedidos por atender"] <= 0:
            estado["Pedidos por atender"] = 0
        else:
            Tercio = int(estado["Pedidos por atender"]* (1/3))
            estado["Pedidos por atender"] = max(0,estado["Pedidos por atender"] - Tercio)
        return estado

    # Terminada
    # Carta 20: Producto defectuoso viral
    #   - Reputacion del mercado −3 niveles.
    elif numero == 20:
        Nivel = estado["Reputacion del mercado"].split(" ")
        estado["Reputacion del mercado"] = f"Nivel {max(0,int(Nivel[1])-3)}"
        return estado
    
    # Terminado 
    # Carta 21: Mal clima: inundacion
    #   - No se produce la siguiente ronda:
    # Duración: 2 turnos
    elif numero == 21:
        estado["Prohibir Produccion"] = True
        Penalidades21 = {"Carta":21,"Mal Clima":3}
        Penalidad_21.append([Penalidades21,True])
        PenalidadesGlobal.append([Penalidades21,True])
        Penalizacion(Penalidades21,estado)
        PenalidadCarta21(estado)
        
        return estado

    # Terminado
    # Carta 22: Licencia vencida
    #   - Multas +30,000.
    #   - Prohibir produccion la siguiente ronda.
    elif numero == 22:
        estado["Multas e indemnizaciones"] += 30000
        Penalidades22 = {"Carta":22,"Licencia vencida":2}
        Penalidad_22.append([Penalidades22,True])
        PenalidadesGlobal.append([Penalidades22,True])
        Penalizacion(Penalidades22,estado)
        PenalidadCarta22(estado)
        return estado

    # Terminado
    # Carta 23: Fake news en redes
    #   - Reputacion del mercado −2 niveles.
    elif numero == 23:
        Nivel = estado["Reputacion del mercado"].split(" ")
        estado["Reputacion del mercado"] = f"Nivel {max(0,int(Nivel[1])-2)}"
        return estado

    # Terminado
    # Carta 24: Bloqueo logistico
    #   - No se venden unidades
    # Duración: 2 turnos
    elif numero == 24:
        estado["GuardadoValoresAuxiliarBloqueoLogistico"] = (estado["Unidades vendidas"],estado["Pedidos por atender"],estado["Caja disponible"],estado["Inventario"])
        Penalidades24 = {"Carta":24, "Bloqueo logistico":3}
        Penalidad_24.append([Penalidades24,True])
        PenalidadesGlobal.append([Penalidades24,True])
        Penalizacion(Penalidades24,estado)
        PenalidadCarta24(estado)
    
        return estado

    # Terminado
    # Carta 25: Demanda judicial
    #   - Multas e indemnizaciones +15,000.
    elif numero == 25:
        estado["Multas e indemnizaciones"] += 15000
        return estado

    # Terminado
    # Carta 26: Nuevo competidor agresivo
    #   - Ventas −40%:
    #   - Debemos pagar 5,000 por almacén
    # Duración: 3 turnos

    elif numero == 26:
        Penalidades26 = {"Carta":26, "Nuevo Competidor": 3}
        Penalidad_26.append([Penalidades26,True])
        PenalidadesGlobal.append([Penalidades26,True])
        Penalizacion(Penalidades26,estado)
        PenalidadCarta26(estado)
        
        return estado

    # Terminado
    # Carta 27: Robo interno
    #   - Caja se reduce en 10,000.
    elif numero == 27:
        Resto = estado["Caja disponible"]- 10000
        if Resto < 0:
            estado["Caja disponible"] = 0
            estado["Deuda pendiente"] += abs(Resto)
        else:
            estado["Caja disponible"] = 0
        return estado

    # Terminado
    # Carta 28: Crisis economica
    #   - Todos los costos +10% por los siguientes 5 turnos:
    elif numero == 28:
        Penalidades28 = {"Carta":28, "Crisis Economica": 5}
        Penalidad_28.append([Penalidades28,True])
        PenalidadesGlobal.append([Penalidades28,True])
        Penalizacion(Penalidades28,estado)
        PenalidadCarta28(estado)
        
        return estado

    # Terminado
    # Carta 29: Fuga de datos
    #   - Reputacion del mercado −2 nivel.
    #   - Ventas de este mes se reducen en un 75%
    elif numero == 29:
        Reputacion = estado["Reputacion del mercado"].split(" ")
        estado["Reputacion del mercado"] = f"Nivel {max(0,int(Reputacion[1])-2)}"
        estado["Unidades vendidas"] = int(estado["Unidades vendidas"] * 0.25)
        
        return estado

    # Terminado
    # Carta 30: Huelga nacional
    #   - No ventas ni produccion
    #   - Debemos pagar 10,000 por almacén
    # Duración: 3 turnos
    elif numero == 30:
        Resto = estado["Caja disponible"] - 10000
        if Resto < 0:
            estado["Caja disponible"] = 0
            estado["Deuda pendiente"] = abs(Resto)
        else:
            estado["Caja disponible"] = Resto
            
        Penalidades30 = {"Carta":30,"Huelga Nacional":3}
        Penalidad_30.append([Penalidades30,True])
        PenalidadesGlobal.append([Penalidades30,True])
        Penalizacion(Penalidades30,estado)
        PenalidadCarta30(estado)
        return estado

    # Terminado
    # Carta 31: Rechazo de exportacion
    #   - Inventario acumulado (no se vende este mes).
    #   - Debemos pagar 10,000 por almacén
    elif numero == 31:
        estado["Unidades vendidas"] = 0
        estado["Multas e indemnizaciones"] += 10000
        
        return estado

    # Terminado
    # Carta 32: Error contable
    #   - Caja −7000.
    elif numero == 32:
        Resto = estado["Caja disponible"] - 7000
        if Resto < 0:
            estado["Caja disponible"] = 0
            estado["Deuda pendiente"] += abs(Resto)
        else:
            estado["Caja disponible"] = Resto
        return estado

    # Terminado
    # Carta 33: Error en codigo de barras
    #   - No se venden productos este mes:
    #   - reputación baja 2 niveles
    elif numero == 33:
        Reputacion = estado["Reputacion del mercado"].split(" ")
        estado["Reputacion del mercado"] = f"Nivel {max(0,int(Reputacion[1])-2)}"
        estado["Unidades vendidas"] = 0
        return estado

    # Terminado
    # Carta 34: Mal diseño del empaque
    #   - Ventas −25%
    #   - reputación baja 2 niveles
    # Duración: 2 turnos
    elif numero == 34:
        Reputacion = estado["Reputacion del mercado"].split(" ")
        estado["Reputacion del mercado"] = f"Nivel {max(0,int(Reputacion[1])-2)}"
        Penalidades34 = {"Carta":34,"Mal diseño empaque": 2}
        Penalidad_34.append([Penalidades34,True])
        PenalidadesGlobal.append([Penalidades34,True])
        Penalizacion(Penalidades34,estado)
        PenalidadCarta34(estado)
        return estado

    # Terminado
    # Carta 35: Cliente se intoxica
    #   - Reputacion del mercado −3 niveles.
    #   - Multas +30,000.
    elif numero == 35:
        Reputacion = estado["Reputacion del mercado"].split(" ")
        estado["Reputacion del mercado"] = f"Nivel {max(0,int(Reputacion[1])-3)}"
        estado["Multas e indemnizaciones"] += 30000
        return estado

    # Terminado
    # Carta 36: Fraude en prestamo
    #   - Caja −15,000.
    #   - Deuda pendiente +15,000.
    #   - reputación baja 2 niveles
    elif numero == 36:
        Reputacion = estado["Reputacion del mercado"].split(" ")
        estado["Reputacion del mercado"] = f"Nivel {max(0,int(Reputacion[1])-2)}"
        
        Resto = estado["Caja disponible"]- 15000
        if Resto <0:
            estado["Deuda pendiente"] += (abs(Resto) +15000)
        else:
            estado["Caja disponible"] = Resto
            estado["Deuda pendiente"] += 15000
        return estado

    # Terminado
    # Carta 37: Trabajador se accidenta
    #   - Multas +4000.
    #   - Produccion −50% este mes
    #   - Temporalmente -1 trabajador por 2 turnos
    elif numero == 37:
        estado["Multas e indemnizaciones"] += 4000
        estado["Unidades vendidas"] *= 0.5
        Penalidades37 = {"Cartas":37,"Trabajador Accidente": 2}
        Penalidad_37.append([Penalidades37,True])
        PenalidadesGlobal.append([Penalidades37,True])
        Penalizacion(Penalidades37,estado)
        PenalidadCarta37(estado)
        return estado

    # Terminado
    # Carta 38: Derrame quimico
    #   - Inventario e Insumos = 0
    #   - No puedes producir durante este mes y el siguiente
    elif numero == 38:
        estado["Inventario"] = 0
        estado["Insumos disponibles"] = 0
        Penalidades38 = {"Carta":38, "Derrame quimico": 2}
        Penalidad_38.append([Penalidades38,True])
        PenalidadesGlobal.append([Penalidades38,True])
        Penalizacion(Penalidades38,estado)
        PenalidadCarta38(estado)
        return estado

    # Terminado
    # Carta 39: Virus contagioso
    #   Todos los empleados se quedaron en su casa por un mes
    #   No se vende ni se produce
    elif numero == 39:
        estado["GuardadoValoresAuxiliarVirusContagioso"] = estado["Cantidad de empleados"]
        estado["Unidades vendidas"] = 0
        estado["Cantidad de empleados"] = 0
        Penalidades39 = {"Carta":39,"Virus Contagioso": 1}
        Penalidad_39.append([Penalidades39,True])
        PenalidadesGlobal.append([Penalidades39,True])
        Penalizacion(Penalidades39,estado)
        PenalidadCarta39(estado)
        return estado

    # Terminado
    # Carta 40: Hiring Freeze
    #   No puedes contratar empleados nuevos
    # Duración: 5 turnos
    elif numero == 40:
        estado["Prohibir contrataciones"] = True
        Penalidades40 = {"Carta":40, "HiringFreeze":5}
        Penalidad_40.append([Penalidades40,True])
        PenalidadesGlobal.append([Penalidades40,True])
        Penalizacion(Penalidades40,estado)
        PenalidadCarta40(estado)
        return estado

    # Si el numero no coincide con ninguna carta:
    #    se considera Dia tranquilo (sin cambios).
    else:
        return estado
