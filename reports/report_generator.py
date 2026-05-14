from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

from db.database import get_logs_by_date_range
from utils.config import REPORTS_DIR, APP_NAME


def _safe_text(value):
    if value is None:
        return "-"

    value = str(value)

    if not value.strip():
        return "-"

    return value


def _short_text(value, max_length=45):
    value = _safe_text(value)

    if len(value) > max_length:
        return value[:max_length] + "..."

    return value


def generate_access_report(start_date, end_date):
    """
    Genera un reporte PDF de accesos por rango de fecha.

    start_date y end_date deben venir en formato:
    YYYY-MM-DD
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    logs = get_logs_by_date_range(start_date, end_date)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reporte_accesos_{start_date}_a_{end_date}_{timestamp}.pdf"
    output_path = REPORTS_DIR / filename

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=landscape(letter),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph(f"<b>{APP_NAME} - Reporte de Accesos</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    info = Paragraph(
        f"""
        <b>Rango de fechas:</b> {start_date} a {end_date}<br/>
        <b>Generado:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br/>
        <b>Total de registros:</b> {len(logs)}
        """,
        styles["Normal"],
    )
    elements.append(info)
    elements.append(Spacer(1, 18))

    data = [
        [
            "Fecha",
            "Hora",
            "Placa",
            "Estado",
            "Motivo",
            "Conf. IA",
            "Distancia",
            "Imagen",
        ]
    ]

    authorized_count = 0
    denied_count = 0
    no_vehicle_count = 0
    unknown_plate_count = 0

    for log in logs:
        status = log["access_status"]

        if status == "AUTORIZADO":
            authorized_count += 1
        elif status == "NO_AUTORIZADO":
            denied_count += 1
        elif status == "SIN_VEHICULO":
            no_vehicle_count += 1
        elif status == "PLACA_NO_RECONOCIDA":
            unknown_plate_count += 1

        confidence = log["vehicle_confidence"]
        if confidence is not None:
            confidence = f"{float(confidence):.2f}"
        else:
            confidence = "-"

        distance = log["distance_cm"]
        if distance is not None:
            distance = f"{float(distance):.1f} cm"
        else:
            distance = "-"

        image_path = log["image_path"]
        if image_path:
            image_path = Path(image_path).name
        else:
            image_path = "-"

        data.append(
            [
                _safe_text(log["event_date"]),
                _safe_text(log["event_time"]),
                _safe_text(log["plate_detected"]),
                _safe_text(status),
                _short_text(log["reason"], 40),
                confidence,
                distance,
                _short_text(image_path, 30),
            ]
        )

    table = Table(
        data,
        colWidths=[65, 55, 80, 105, 210, 60, 70, 150],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 8),
                ("FONTSIZE", (0, 1), (-1, -1), 7),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")]),
            ]
        )
    )

    elements.append(table)
    elements.append(Spacer(1, 20))

    summary = Paragraph(
        f"""
        <b>Resumen del reporte</b><br/><br/>
        Ingresos autorizados: {authorized_count}<br/>
        Intentos no autorizados: {denied_count}<br/>
        Eventos sin vehículo válido: {no_vehicle_count}<br/>
        Placas no reconocidas: {unknown_plate_count}<br/>
        Total de registros: {len(logs)}
        """,
        styles["Normal"],
    )

    elements.append(summary)

    doc.build(elements)

    return output_path