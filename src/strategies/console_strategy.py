from typing import List, Dict
from src.interfaces.output_strategy import OutputStrategy


class ConsoleStrategy(OutputStrategy):

    def output(self, data: List[Dict[str, str]]) -> None:
        print("-" * 90)
        print(
            f"{'Продукт':<25} | {'Тип покриття':<18} | "
            f"{'Країна':<15} | {'Ризик':<10} | {'Премія (€)':<10}"
        )
        print("-" * 90)

        for row in data:
            product_name = row.get("product_name", "N/A")
            coverage_type = row.get("coverage_type", "N/A")
            destination = row.get("destination_country", "N/A")
            risk_level = row.get("risk_level", "N/A")
            premium = row.get("premium_eur", "N/A")

            print(
                f"{product_name:<25} | {coverage_type:<18} | "
                f"{destination:<15} | {risk_level:<10} | {premium:<10}"
            )

        print("-" * 90)
        print(f"[ConsoleStrategy] Виведено {len(data)} записів")
