from datetime import datetime

from db.database import init_db
from reports.report_generator import generate_access_report


def main():
    init_db()

    today = datetime.now().strftime("%Y-%m-%d")

    print("Generando reporte PDF...")
    print(f"Fecha inicial: {today}")
    print(f"Fecha final: {today}")

    report_path = generate_access_report(today, today)

    print(f"Reporte generado correctamente:")
    print(report_path)


if __name__ == "__main__":
    main()