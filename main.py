# main.py

import pygame
import os

import acciones
import cartas
import estado

# -------------------------------- Constantes --------------------------------
CELL_SIZE = 64
GRID_WIDTH = 10
GRID_HEIGHT = 8

AREA_NAMES = {
    1: "I. Produccion",
    2: "II. Recursos Humanos",
    3: "III. Marketing",
    4: "IV. Compras",
    5: "V. Finanzas"
}

SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH + 200
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT + 60 + 120

# ------------------------------ Inicializacion ------------------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulador de Planta con Kiwitos")
font = pygame.font.SysFont(None, 28)
input_font = pygame.font.SysFont(None, 36)

# ---------------------------- Cargar imagenes de fondo ----------------------------
fondo_images = {}
for i in range(1, 6):
    ruta = f"img/fondo{i}.png"
    try:
        fondo_images[i] = pygame.image.load(ruta)
    except Exception:
        surf = pygame.Surface((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT))
        surf.fill((200, 200, 200))
        fondo_images[i] = surf

# ---------------------------- Cargar placeholders de eventos ----------------------------
# Carta numero fuera de rango (>40 o <1)
try:
    evento_img_inexistente = pygame.image.load("img/Eventos/evento_inexistente.png")
except Exception:
    evento_img_inexistente = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - 80))
    evento_img_inexistente.fill((230, 230, 230))

# Carta valida pero falta PNG
try:
    evento_img_sin_carta = pygame.image.load("img/Eventos/evento_sin_carta.png")
except Exception:
    evento_img_sin_carta = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - 80))
    evento_img_sin_carta.fill((210, 210, 210))

# ---------------------------- Botones y rectangulos ----------------------------
boton_izquierda   = pygame.Rect(20, SCREEN_HEIGHT // 2 - 20, 40, 40)
boton_derecha     = pygame.Rect(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 - 20, 40, 40)
boton_cambiar     = pygame.Rect(0, 0, 140, 40)
boton_tomar_carta = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT - 60, 140, 40)
boton_estado      = pygame.Rect(30, SCREEN_HEIGHT - 60, 260, 40)


# ------------------------- Variables de control y estado -------------------------
current_area       = 1
estado_empresa     = estado.calcular_estado_inicial()

ACCIONES_POR_AREA = {
    1: [
        ("Producir", acciones.produccion_producir),
        ("Producir por encargo", acciones.produccion_pedido_encargo),
        ("Mejorar proceso", acciones.produccion_mejorar_proceso),
        ("Mantenimiento maquinaria", acciones.produccion_mantenimiento_maquinaria),
        ("Comprar nueva maquina", acciones.produccion_comprar_nueva_maquina),
        ("No hacer nada", acciones.produccion_no_hacer_nada),
    ],
    2: [
        ("Contratar personal permanente", acciones.rh_contratar_personal_permanente),
        ("Contratar personal temporal",    acciones.rh_contratar_personal_temporal),
        ("Implementar incentivos",         acciones.rh_implementar_incentivos),
        ("Medicion clima laboral",         acciones.rh_medicion_clima),
        ("Capacitar en seguridad",         acciones.rh_capacitar_seguridad),
        ("Subir sueldos",                  acciones.rh_subir_sueldos),
        ("No hacer nada",                  acciones.rh_no_hacer_nada),
    ],
    3: [
        ("Lanzar campaña", acciones.marketing_lanzar_campania),
        ("Invertir en branding", acciones.marketing_invertir_branding),
        ("Estudio de mercado", acciones.marketing_estudio_mercado),
        ("Abrir e-commerce", acciones.marketing_abrir_ecommerce),
        ("Co-branding", acciones.marketing_co_branding),
        ("No hacer nada", acciones.marketing_no_hacer_nada),
    ],
    4: [
        ("Comprar insumos nacionales", acciones.compras_comprar_insumos_nacionales),
        ("Comprar insumos importados", acciones.compras_comprar_insumos_importados),
        ("Comprar insumos premium",    acciones.compras_comprar_insumos_importados_premium),
        ("Vender excedentes de insumos", acciones.compras_vender_excedentes_insumos),
        ("Negociar precio",            acciones.compras_negociar_precio),
        ("Negociar credito",           acciones.compras_negociar_credito),
        ("No hacer nada",              acciones.compras_no_hacer_nada),
    ],
    5: [
        ("Pagar proveedores", acciones.finanzas_pagar_proveedores),
        ("Pagar deuda",        acciones.finanzas_pagar_deuda),
        ("Solicitar prestamo", acciones.finanzas_solicitar_prestamo),
        ("Crear fondo emerg.", acciones.finanzas_crear_fondo_emergencia),
        ("No hacer nada",      acciones.finanzas_no_hacer_nada),
    ]
}

accion_seleccionada = {
    area: ACCIONES_POR_AREA[area][-1]
    for area in range(1, 6)
}

mostrando_panel_acciones = False
area_panel_abierto       = None
mostrando_input_carta    = False
input_text_carta         = ""
mensaje_input_carta      = "Ingresa numero de carta:"
mostrando_evento         = False
mostrando_estado         = False
cursor_visible           = True
cursor_timer             = 0
input_text_acciones      = ""

# ------- NUEVO: guardamos aqui el numero de carta elegido -------
card_to_show             = None
# -----------------------------------------------------------------

# ----------------------------- Funciones auxiliares -----------------------------
def draw_estado_empresa():
    line_height = 28
    # Mostrar solo las primeras 17 entradas
    items = list(estado_empresa.items())[:17]
    num_lines   = len(items) + 1  # +1 para el titulo
    top_m       = 20
    bot_m       = 20
    panel_h     = top_m + num_lines * line_height + bot_m + 40
    panel_w     = 600
    panel       = pygame.Rect(0, 0, panel_w, panel_h)
    panel.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    pygame.draw.rect(screen, (255, 255, 255), panel)
    pygame.draw.rect(screen, (0, 0, 0), panel, 3)

    title = input_font.render("Estado de la Empresa", True, (0, 0, 0))
    screen.blit(title, (panel.centerx - title.get_width() // 2, panel.top + 5))

    y = panel.top + top_m + 20
    for key, val in items:
        if key.startswith("Prohibir "):
            disp_key = "Prohibicion de " + key[len("Prohibir "):]
        else:
            disp_key = key
        if isinstance(val, bool):
            disp_val = "Si" if val else "No"
        else:
            disp_val = val
        line = font.render(f"{disp_key}: {disp_val}", True, (0, 0, 0))
        screen.blit(line, (panel.left + 20, y))
        y += line_height

    size = 30
    cerrar = pygame.Rect(panel.right - size - 8, panel.top + 8, size, size)
    pygame.draw.rect(screen, (200, 200, 200), cerrar)
    pygame.draw.rect(screen, (0, 0, 0), cerrar, 2)
    pygame.draw.line(screen, (0, 0, 0),
                     (cerrar.left + 6, cerrar.top + 6),
                     (cerrar.right - 6, cerrar.bottom - 6), 2)
    pygame.draw.line(screen, (0, 0, 0),
                     (cerrar.left + 6, cerrar.bottom - 6),
                     (cerrar.right - 6, cerrar.top + 6), 2)
    return cerrar

def dibujar_panel_acciones(area):
    opciones = ACCIONES_POR_AREA[area]
    ancho    = 600
    alto     = 60 + len(opciones) * 48 + 80
    panel    = pygame.Rect(0, 0, ancho, alto)
    panel.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, (255, 255, 255), panel)
    pygame.draw.rect(screen, (0, 0, 0), panel, 3)
    title = input_font.render(f"Seleccione accion para {AREA_NAMES[area]}", True, (0, 0, 0))
    screen.blit(title, (panel.centerx - title.get_width() // 2, panel.top + 10))
    y0 = panel.top + 50
    for i, (txt, _) in enumerate(opciones, 1):
        line = font.render(f"{i}. {txt}", True, (0, 0, 0))
        screen.blit(line, (panel.left + 20, y0 + (i - 1) * 48))
    caja = pygame.Rect(panel.left + 20, panel.bottom - 90, ancho - 240, 40)
    pygame.draw.rect(screen, (230, 230, 230), caja)
    pygame.draw.rect(screen, (0, 0, 0), caja, 2)
    txt_surf = input_font.render(input_text_acciones, True, (0, 0, 0))
    screen.blit(txt_surf, (caja.x + 10, caja.y + 5))
    if cursor_visible:
        cx = caja.x + 10 + txt_surf.get_width() + 2
        cy = caja.y + 5
        ch = txt_surf.get_height()
        pygame.draw.line(screen, (0, 0, 0), (cx, cy), (cx, cy + ch), 2)
    btn_ok = pygame.Rect(panel.right - 120, panel.bottom - 90, 100, 40)
    pygame.draw.rect(screen, (180, 180, 180), btn_ok)
    pygame.draw.rect(screen, (0, 0, 0), btn_ok, 2)
    screen.blit(font.render("OK", True, (0, 0, 0)), (btn_ok.x + 30, btn_ok.y + 10))
    return caja, btn_ok

def dibujar_panel_carta():
    panel = pygame.Rect(0, 0, 400, 160)
    panel.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, (255, 255, 255), panel)
    pygame.draw.rect(screen, (0, 0, 0), panel, 3)
    msg = input_font.render(mensaje_input_carta, True, (0, 0, 0))
    screen.blit(msg, (panel.centerx - msg.get_width() // 2, panel.top + 20))
    caja = pygame.Rect(panel.left + 20, panel.top + 80, 200, 40)
    pygame.draw.rect(screen, (230, 230, 230), caja)
    pygame.draw.rect(screen, (0, 0, 0), caja, 2)
    txt_s = input_font.render(input_text_carta, True, (0, 0, 0))
    screen.blit(txt_s, (caja.x + 10, caja.y + 5))
    if cursor_visible:
        cx = caja.x + 10 + txt_s.get_width() + 2
        cy = caja.y + 5
        ch = txt_s.get_height()
        pygame.draw.line(screen, (0, 0, 0), (cx, cy), (cx, cy + ch), 2)
    btn_ok = pygame.Rect(panel.right - 120, panel.top + 80, 100, 40)
    pygame.draw.rect(screen, (180, 180, 180), btn_ok)
    pygame.draw.rect(screen, (0, 0, 0), btn_ok, 2)
    screen.blit(font.render("OK", True, (0, 0, 0)), (btn_ok.x + 30, btn_ok.y + 10))
    return caja, btn_ok

def dibujar_evento():
    evento_area = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 80)
    n = card_to_show

    # 1) fuera de rango o invalido → inexistente
    if not isinstance(n, int) or not (1 <= n <= 40):
        imagen = evento_img_inexistente

    else:
        ruta = os.path.join("img", "Eventos", f"evento_carta_{n}.png")
        if os.path.isfile(ruta):
            try:
                imagen = pygame.image.load(ruta)
            except pygame.error:
                imagen = evento_img_sin_carta
        else:
            # carta valida pero sin PNG
            imagen = evento_img_sin_carta

    scaled = pygame.transform.scale(imagen, (evento_area.width, evento_area.height))
    screen.blit(scaled, evento_area)

    pygame.draw.rect(screen, (200, 200, 200), boton_tomar_carta)
    pygame.draw.rect(screen, (0, 0, 0), boton_tomar_carta, 2)
    txt_cont = font.render("Continuar", True, (0, 0, 0))
    screen.blit(txt_cont, (boton_tomar_carta.x + 15, boton_tomar_carta.y + 8))

def draw():
    screen.fill((240, 240, 240))
    screen.blit(fondo_images[current_area], (100, 60))

    encabezado = f"{AREA_NAMES[current_area]}: {accion_seleccionada[current_area][0]}"
    screen.blit(font.render(encabezado, True, (0, 0, 0)), (20, 20))

    boton_cambiar.topleft = (SCREEN_WIDTH - 160, 16)
    pygame.draw.rect(screen, (180, 180, 180), boton_cambiar)
    pygame.draw.rect(screen, (0, 0, 0), boton_cambiar, 2)
    screen.blit(font.render("Cambiar", True, (0, 0, 0)), (boton_cambiar.x + 20, boton_cambiar.y + 8))

    pygame.draw.rect(screen, (180, 180, 180), boton_izquierda)
    pygame.draw.rect(screen, (0, 0, 0), boton_izquierda, 2)
    screen.blit(font.render("<", True, (0, 0, 0)), (boton_izquierda.x + 12, boton_izquierda.y + 8))

    pygame.draw.rect(screen, (180, 180, 180), boton_derecha)
    pygame.draw.rect(screen, (0, 0, 0), boton_derecha, 2)
    screen.blit(font.render(">", True, (0, 0, 0)), (boton_derecha.x + 12, boton_derecha.y + 8))

    pygame.draw.rect(screen, (180, 180, 180), boton_estado)
    pygame.draw.rect(screen, (0, 0, 0), boton_estado, 2)
    screen.blit(font.render("Estado de la Empresa", True, (0, 0, 0)), (boton_estado.x + 10, boton_estado.y + 8))

    pygame.draw.rect(screen, (180, 180, 180), boton_tomar_carta)
    pygame.draw.rect(screen, (0, 0, 0), boton_tomar_carta, 2)
    screen.blit(font.render("Tomar carta", True, (0, 0, 0)), (boton_tomar_carta.x + 15, boton_tomar_carta.y + 8))

    if mostrando_panel_acciones and area_panel_abierto is not None:
        dibujar_panel_acciones(area_panel_abierto)

    if mostrando_input_carta:
        dibujar_panel_carta()

    if mostrando_evento:
        dibujar_evento()

    if mostrando_estado:
        cerrar = draw_estado_empresa()
        pygame.display.flip()
        return cerrar

    pygame.display.flip()

# ------------------------------ Bucle principal ------------------------------
clock = pygame.time.Clock()
running = True

while running:
    cerrar_btn = draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            # --- Estado de la empresa ---
            if boton_estado.collidepoint(event.pos):
                mostrando_estado = True
                continue

            if mostrando_estado:
                # cerrar cuadro de estado
                if cerrar_btn and cerrar_btn.collidepoint(event.pos):
                    mostrando_estado = False

            # --- Evento activo (pantalla grande) ---
            elif mostrando_evento:
                if boton_tomar_carta.collidepoint(event.pos):
                    mostrando_evento  = False
                    estado_empresa    = estado.calcular_estado_final(estado_empresa)
                    card_to_show      = None   # limpiamos el numero

            # --- Panel de seleccion de acciones ---
            elif mostrando_panel_acciones and area_panel_abierto is not None:
                caja_acc, ok_acc = dibujar_panel_acciones(area_panel_abierto)
                if ok_acc.collidepoint(event.pos):
                    try:
                        opt = int(input_text_acciones.strip())
                    except ValueError:
                        opt = -1
                    ops = ACCIONES_POR_AREA[area_panel_abierto]
                    if 1 <= opt <= len(ops):
                        txt, fn = ops[opt - 1]
                    else:
                        txt, fn = ops[-1]
                    accion_seleccionada[area_panel_abierto] = (txt, fn)
                    mostrando_panel_acciones = False
                    area_panel_abierto = None
                    input_text_acciones = ""

            # --- Panel de ingreso de carta ---
            elif mostrando_input_carta:
                caja_c, ok_c = dibujar_panel_carta()
                if ok_c.collidepoint(event.pos):
                    try:
                        num = int(input_text_carta.strip())
                    except ValueError:
                        num = None
                    card_to_show         = num
                    estado_empresa       = cartas.aplicar_carta(num, estado_empresa)
                    mostrando_input_carta = False
                    mostrando_evento     = True
                    estado_empresa["Meses"] +=1
                    # NO limpiamos input_text_carta aqui

            else:
                # Navegar areas
                if boton_izquierda.collidepoint(event.pos):
                    current_area = max(1, current_area - 1)
                    continue
                if boton_derecha.collidepoint(event.pos):
                    current_area = min(5, current_area + 1)
                    continue
                # Abrir panel de acciones
                if boton_cambiar.collidepoint(event.pos):
                    mostrando_panel_acciones = True
                    area_panel_abierto = current_area
                    input_text_acciones = ""
                    continue
                # Ejecutar acciones y luego pedir carta
                if boton_tomar_carta.collidepoint(event.pos):
                    for aid in range(1, 6):
                        _, fn = accion_seleccionada[aid]
                        estado_empresa = fn(estado_empresa)
                    mostrando_input_carta = True
                    input_text_carta = ""
                    continue

        elif event.type == pygame.KEYDOWN:
            if mostrando_panel_acciones and area_panel_abierto is not None:
                if event.key == pygame.K_BACKSPACE:
                    input_text_acciones = input_text_acciones[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    if len(input_text_acciones) < 2 and event.unicode.isprintable():
                        input_text_acciones += event.unicode

            elif mostrando_input_carta:
                if event.key == pygame.K_BACKSPACE:
                    input_text_carta = input_text_carta[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    if len(input_text_carta) < 3 and event.unicode.isprintable():
                        input_text_carta += event.unicode

    cursor_timer += 1
    if cursor_timer >= 30:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    clock.tick(30)

pygame.quit()
