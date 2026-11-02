# ==========================================================
# 1 - VERIFICAÇÃO DE COLISÕES
# ==========================================================

def verificar_colisao(caminhao, obstaculos):
    """Retorna True quando o caminhão atinge algum obstáculo."""

    # Percorre todos os obstáculos existentes
    for obstaculo in obstaculos:

        # Retângulo utilizado no desenho e na movimentação
        area_obstaculo = obstaculo["rect"]

        # Mantém compatibilidade com obstáculos antigos sem "tipo"
        tipo = obstaculo.get("tipo", "carro")

        if tipo == "buraco":
            # A borda visual do buraco não provoca colisão.
            # O núcleo perigoso corresponde a 70% de sua área.
            area_colisao = area_obstaculo.inflate(
                -round(area_obstaculo.width * 0.30),
                -round(area_obstaculo.height * 0.30)
            )
        else:
            # Carros e motos utilizam o próprio retângulo.
            area_colisao = area_obstaculo

        if caminhao.colliderect(area_colisao):
            return True

    return False
