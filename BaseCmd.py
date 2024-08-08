import subprocess


class NiktoHelper:
    NIKTO_CMD = ['nikto', '-h', 'https://test-stand.gb.ru/', '-ssl', '-Tuning', '4']

    def run_nikto(self):
        """Запуск команды Nikto и возврат вывода."""
        result = subprocess.run(self.NIKTO_CMD, capture_output=True, text=True)
        return result.stdout
