class MissionManager:
    def __init__(self):
        self.stats = {
            "planted": 0,
            "harvested": 0,
            "fertilizers_used": 0,
            "beds_bought": 0,
            "sold_items": 0,
            "money_earned": 0,
            "balance": 0,
        }

        self.missions = [
            ("Первый росток", "Посадите первое растение", "planted", 1),
            ("Огородник", "Посадите 10 растений", "planted", 10),
            ("Фермер", "Посадите 50 растений", "planted", 50),
            ("Аграрный магнат", "Посадите 200 растений", "planted", 200),

            ("Первый урожай", "Соберите первое растение", "harvested", 1),
            ("Жатва", "Соберите 25 растений", "harvested", 25),
            ("Комбайн", "Соберите 100 растений", "harvested", 100),

            ("Химик-любитель", "Используйте 5 удобрений", "fertilizers_used", 5),
            ("Химик", "Используйте 25 удобрений", "fertilizers_used", 25),
            ("Химик-профи", "Используйте 100 удобрений", "fertilizers_used", 100),

            ("Маленький огород", "Купите первую грядку", "beds_bought", 1),
            ("Расширение территории", "Купите 5 грядок", "beds_bought", 5),

            ("Первая продажа", "Продайте любое растение", "sold_items", 1),
            ("Мелкий торговец", "Заработайте 50 монет", "money_earned", 50),
            ("Купец", "Заработайте 200 монет", "money_earned", 200),

            ("Золотые руки", "Достигните баланса 500 монет", "balance", 500),
        ]

        self.completed = set()

    def inc(self, key, value=1):
        self.stats[key] += value

    def set_balance(self, value):
        self.stats["balance"] = value

    def get_status(self):
        result = []
        for name, desc, key, need in self.missions:
            cur = self.stats[key]
            done = cur >= need
            if done:
                self.completed.add(name)
            result.append((name, desc, cur, need, done))
        return result