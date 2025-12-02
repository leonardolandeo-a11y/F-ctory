#### Importacion modulo cartas ####
from cartas import PenalidadTurnos,EliminarPenalidad
from cartas import PenalidadesGlobal,Penalidad_3,Penalidad_6,Penalidad_9,Penalidad_12,Penalidad_13,Penalidad_14,Penalidad_15,Penalidad_18,Penalidad_21,Penalidad_22,Penalidad_24,Penalidad_26,Penalidad_28,Penalidad_30,Penalidad_34,Penalidad_37,Penalidad_38,Penalidad_39,Penalidad_40
import pandas as pd
# Penalidad por cartas
from cartas import PenalidadCarta3_1,PenalidadCarta3_2,PenalidadCarta6,PenalidadCarta9,PenalidadCarta12,PenalidadCarta13,PenalidadCarta14,PenalidadCarta15,PenalidadCarta18,PenalidadCarta21,PenalidadCarta22, PenalidadCarta24,PenalidadCarta26,PenalidadCarta28,PenalidadCarta30,PenalidadCarta34,PenalidadCarta37,PenalidadCarta38,PenalidadCarta39,PenalidadCarta40


def calcular_estado_inicial():
    """
    Inicializa el diccionario `estado` con los indicadores clave de la empresa,
    incluyendo todos los flags y contadores que luego se referencian en
    calcular_estado_final().
    """
    empleados = 4
    costo_emp = 2000
    precio_venta = 4.5
    return {
        # Indicadores financieros y operativos
        "Caja disponible":                   50000,
        "Inventario":                        0,
        "Pedidos por atender":               0,
        "Unidades vendidas":                 0,
        "Insumos disponibles":               100,
        "Cantidad de empleados":             empleados,
        "Costo por empleado":                costo_emp,
        "Sueldos por pagar":                 empleados * costo_emp,
        "Deuda pendiente":                   20000,
        "Reputacion del mercado":            "Nivel 3",
        "Multas e indemnizaciones":          0,
        "Maquinas (total/activas/dañadas)": "5/5/0",
        "Precio venta":                     precio_venta,
        # Meses Pasados
        "Meses": 0,

        # Banderas de prohibicion y seguro
        "Prohibir Produccion":               False,
        "Prohibir Compras":                  False,
        "Prohibir Importaciones":            False,
        "Fondo emergencia":                  False,

        # Contadores y flags temporales
        "TurnosProduccionExtra":             0,
        "DemandaExtraTemporal":              50000,
        "EmpleadosTemporales":               0,
        "MejoraProceso":                     False,
        "BrandingActivo":                    False,
        "MantenimientoHecho":                False,
        "EcommerceActivo":                   False,
        "InventarioMesAnterior":             0
    }

def calcular_estado_final(estado):
   """
   Aplica las formulas de calculo al final de cada turno (mes) en el siguiente orden:
   """
   # 1) Venta automatica
   estado["Inventario"] = estado["Inventario"]
   estado["Unidades vendidas"] = estado["Unidades vendidas"]
   estado["Caja disponible"] = estado["Caja disponible"]

   # 2) Actualizacion de pedidos por atender
   estado["Pedidos por atender"] = estado["Pedidos por atender"]
   estado["Reputacion del mercado"] = estado["Reputacion del mercado"]

   # 3) Pago de la nomina del mes actual
   estado["Sueldos por pagar"] = estado["Sueldos por pagar"]
   estado["Caja disponible"] = estado["Caja disponible"]

   # 4) Generacion de la nomina del proximo mes
   estado["Sueldos por pagar"] = estado["Sueldos por pagar"]

   # 5) Anular multas, accidentes, y demas cartas del caos
   estado["Prohibir Produccion"] = estado["Prohibir Produccion"]

   # 6) Produccion en automatico
   estado["Inventario"] = estado["Inventario"]

   # 7) Actualizacion de flags temporales y decremento de contadores
   estado["TurnosProduccionExtra"] = estado["TurnosProduccionExtra"]
   if "VentaExcedentesActivos" in estado:
      if estado["VentaExcedentesActivos"] > 0:
            estado["VentaExcedentesActivos"] -= 1

   # 8) Perdida de inventario:
   estado["Inventario"] = estado["Inventario"]

   # Contador atrás basado en la acción creada (compras_vender_excedentes_insumos) --Marco--
   if estado["Inventario"] == estado["InventarioMesAnterior"]:
      cuantoscaducan = max(1, int(estado["Insumos disponibles"] * 0.10)) if estado["Insumos disponibles"] > 0 else 0
      if estado["Insumos disponibles"] >= 10:
         if "VentaExcedentesActivos" in estado and estado["VentaExcedentesActivos"] > 0:
            preciov = cuantoscaducan * 0.30
            estado["Caja disponible"] += preciov
      else:
         estado["VentaExcedentesActivos"] = 0
      estado["Insumos disponibles"] -= cuantoscaducan
      if estado["Insumos disponibles"] < 0:
            estado["Insumos disponibles"] = 0

   # Codigo Ambiente laboral Faborable (rh_medicion_clima)
   if "AmbienteLaboralFavorableTiempo" in estado and "AmbienteLaboralFavorable" in estado:
      if estado["AmbienteLaboralFavorableTiempo"] > 0:
         estado["AmbienteLaboralFavorableTiempo"] -= 1
         for key in ["Huelgas", "BajoRendimiento", "ErroresEmpleados", "ErroresLogísticos", "FugasDeTalento"]:
            if key in estado and estado[key] > 0:
               estado[key] -= 1
      elif estado["AmbienteLaboralFavorableTiempo"] == 0:
         estado["AmbienteLaboralFavorable"] = False
         
   # Cartas simples sin penalidades
   
   # Carta 4
   if "Incendio Pendiente" in estado:
      if estado["Incendio Pendiente"] == True:
         estado["Inventario"] = 0
         estado["Incendio Pendiente"] = False
   
   
   # Automatizacion de cartas con penalidades
   
   # Carta 3
   if len(Penalidad_3) != 0: 
      if Penalidad_3[0][1] == True: 
         PenalidadTurnos(Penalidad_3[0][0],Penalidad_3,0, estado) 
         PenalidadCarta3_1(estado)
         PenalidadCarta3_2(estado)
         EliminarPenalidad(Penalidad_3)
   
   # Carta 6
   if len(Penalidad_6) != 0:
      if Penalidad_6[0][1] == True:
         PenalidadTurnos(Penalidad_6[0][0], Penalidad_6,0,estado)
         PenalidadCarta6(estado)
         EliminarPenalidad(Penalidad_6)

   # Carta 9
   if len(Penalidad_9) != 0:
      if Penalidad_9[0][1] == True:
         PenalidadTurnos(Penalidad_9[0][0],Penalidad_9,0,estado)
         PenalidadCarta9(estado)
         EliminarPenalidad(Penalidad_9)

   # Carta 12
   if len(Penalidad_12) != 0:
      if Penalidad_12[0][1] == True:
            PenalidadTurnos(Penalidad_12[0][0],Penalidad_12,0, estado)
            PenalidadCarta12(estado)
            EliminarPenalidad(Penalidad_12)

   # Carta 13
   if len(Penalidad_13) != 0:
      if  Penalidad_13[0][1] == True:
         PenalidadTurnos(Penalidad_13[0][0],Penalidad_13,0,estado)
         PenalidadCarta13(estado)
         EliminarPenalidad(Penalidad_13)
   # Carta 14
   if len(Penalidad_14) != 0:
      if  Penalidad_14[0][1] == True:
         PenalidadTurnos(Penalidad_14[0][0],Penalidad_14,0,estado)
         PenalidadCarta14(estado)
         EliminarPenalidad(Penalidad_14)
   # Carta 15
   if len(Penalidad_15) != 0:
      if  Penalidad_15[0][1] == True:
         PenalidadTurnos(Penalidad_15[0][0],Penalidad_15,0,estado)
         PenalidadCarta15(estado)
         EliminarPenalidad(Penalidad_15)
   # Carta 18
   if len(Penalidad_18) != 0:
      if Penalidad_18[0][1] == True:
         PenalidadTurnos(Penalidad_18[0][0],Penalidad_18,0,estado)
         PenalidadCarta18(estado)
         EliminarPenalidad(Penalidad_18)
   # Carta 21
   if len(Penalidad_21) != 0:
      if  Penalidad_21[0][1] == True:
         PenalidadTurnos(Penalidad_21[0][0],Penalidad_21,0,estado)
         PenalidadCarta21(estado)
         EliminarPenalidad(Penalidad_21)
   
   # Carta 22
   if len(Penalidad_22) != 0:
      if  Penalidad_22[0][1] == True:
         PenalidadTurnos(Penalidad_22[0][0],Penalidad_22,0,estado)
         PenalidadCarta22(estado)
         EliminarPenalidad(Penalidad_22)
   
   # Carta 24
   if len(Penalidad_24) != 0:
      if  Penalidad_24[0][1] == True:
         PenalidadTurnos(Penalidad_24[0][0],Penalidad_24,0,estado)
         PenalidadCarta24(estado)
         EliminarPenalidad(Penalidad_24)
   
   # Carta 26
   if len(Penalidad_26) != 0:
      if  Penalidad_26[0][1] == True:
         PenalidadTurnos(Penalidad_26[0][0],Penalidad_26,0,estado)
         PenalidadCarta26(estado)
         EliminarPenalidad(Penalidad_26)
   
   # Carta 28
   if len(Penalidad_28) != 0:
      if  Penalidad_28[0][1] == True:
         PenalidadTurnos(Penalidad_28[0][0],Penalidad_28,0,estado)
         PenalidadCarta28(estado)
         EliminarPenalidad(Penalidad_28)
   
   # Carta 30
   if len(Penalidad_30) != 0:
      if  Penalidad_30[0][1]== True:
         PenalidadTurnos(Penalidad_30[0][0],Penalidad_30,0,estado)
         PenalidadCarta30(estado)
         EliminarPenalidad(Penalidad_30)
   
   # Carta 34
   if len(Penalidad_34) != 0:
      if  Penalidad_34[0][1] == True:
         PenalidadTurnos(Penalidad_34[0][0],Penalidad_34,0,estado)
         PenalidadCarta34(estado)
         EliminarPenalidad(Penalidad_34)
         
   # Carta 37
   if len(Penalidad_37) != 0:
      if  Penalidad_37[0][1] == True:
         PenalidadTurnos(Penalidad_37[0][0],Penalidad_37,0,estado)
         PenalidadCarta37(estado)
         EliminarPenalidad(Penalidad_37)
   
   # Carta 38
   if len(Penalidad_38) != 0:
      if  Penalidad_38[0][1] == True:
         PenalidadTurnos(Penalidad_38[0][0],Penalidad_38,0,estado)
         PenalidadCarta38(estado)
         EliminarPenalidad(Penalidad_38)

   # Carta 39
   if len(Penalidad_39) != 0:
      if  Penalidad_39[0][1] == True:
         PenalidadTurnos(Penalidad_39[0][0],Penalidad_39,0,estado)
         PenalidadCarta39(estado)
         EliminarPenalidad(Penalidad_39)
   
   # Carta 40
   if len(Penalidad_40) != 0:
      if  Penalidad_40[0][1] == True:
         PenalidadTurnos(Penalidad_40[0][0],Penalidad_40,0,estado)
         PenalidadCarta40(estado)
         EliminarPenalidad(Penalidad_40)
            
   Estado = pd.DataFrame.from_dict(estado, orient="index", columns=["valor"])
   print(Estado)
   print(PenalidadesGlobal)
   print("Penalidad 3:",Penalidad_3)
   print("Penalidad 6:",Penalidad_6)
   print("Penalidad 9:",Penalidad_9)
   print("Penalidad 12:",Penalidad_12)
   print("Penalidad 13:",Penalidad_13)
   print("Penalidad 14:",Penalidad_14)
   print("Penalidad 15:",Penalidad_15)
   print("Penalidad 18:",Penalidad_18)
   print("Penalidad 21:",Penalidad_21)
   print("Penalidad 22:",Penalidad_22)
   print("Penalidad 24:",Penalidad_24)
   print("Penalidad 26:",Penalidad_26)
   print("Penalidad 28:",Penalidad_28)
   print("Penalidad 30:",Penalidad_30)
   print("Penalidad 34:",Penalidad_34)
   print("Penalidad 37:",Penalidad_37)
   print("Penalidad 38:",Penalidad_38)
   print("Penalidad 39:",Penalidad_39)
   print("Penalidad 40:",Penalidad_40)

   return estado