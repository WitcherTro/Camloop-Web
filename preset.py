class Preset:
    def __init__(self, filename):
        self.filename = filename

    def delete_last(self):
        with open(self.filename, 'r') as f:
            lines = f.read().splitlines()

        # Check if there are at least two lines to delete (a preset and a sleep time)
        if len(lines) >= 2:
            # Delete the last two lines (the last preset and sleep time)
            lines = lines[:-2]

            with open(self.filename, 'w') as f:
                for line in lines:
                    f.write(f'{line}\n')